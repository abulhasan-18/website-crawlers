import argparse
import re
import csv
from pathlib import Path
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate


COLUMNS = [
    "URL",
    "Status",
    "No. of content words",
    "Title",
    "Title length",
    "Meta description",
]


def load_urls(file_path: Path) -> list[str]:
    if not file_path.exists():
        raise FileNotFoundError(f"URL file not found: {file_path}")

    urls: list[str] = []
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)

    return urls


def clean_text(value: str) -> str:
    """
    Make CSV/Sheets-safe:
    - remove line breaks
    - remove double quotes (common reason Sheets gets confused)
    - normalize whitespace
    """
    if not value:
        return ""

    value = value.replace("\n", " ").replace("\r", " ")
    value = value.replace('"', "")   # important
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def fetch_html(url: str, timeout: int = 15) -> tuple[str | None, str]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.encoding = resp.encoding or "utf-8"
        status_str = f"{resp.status_code} {resp.reason}"

        if resp.status_code == 200:
            return resp.text, status_str
        return None, status_str

    except requests.RequestException as e:
        return None, f"ERROR: {e}"


def extract_visible_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "header", "footer", "svg"]):
        tag.decompose()
    text = soup.get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return text


def analyze_html(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    # Title
    title_text = ""
    if soup.title and soup.title.string:
        title_text = clean_text(soup.title.string)

    # Meta description
    meta_desc = ""
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    if meta_desc_tag and meta_desc_tag.get("content"):
        meta_desc = clean_text(meta_desc_tag.get("content"))

    # Word count
    visible_text = extract_visible_text(html)
    word_count = len(visible_text.split()) if visible_text else 0

    return {
        "No. of content words": word_count,
        "Title": title_text,
        "Title length": len(title_text),
        "Meta description": meta_desc,
    }


def crawl_urls(urls: list[str]) -> pd.DataFrame:
    rows = []

    for url in urls:
        print(f"[INFO] Crawling: {url}")
        html, status = fetch_html(url)

        if html is None:
            rows.append({
                "URL": url,
                "Status": status,
                "No. of content words": 0,
                "Title": "",
                "Title length": 0,
                "Meta description": "",
            })
            continue

        row = {"URL": url, "Status": status}
        row.update(analyze_html(html))
        rows.append(row)

    df = pd.DataFrame(rows)
    return df[COLUMNS]  # enforce ONLY 6 columns + correct order


def generate_filename() -> str:
    # Windows-safe: ":" not allowed in filenames, so use "-"
    # Example: crawl-report-02-12-2025 10-15 AM.csv
    ts = datetime.now().strftime("%d-%m-%Y %I-%M %p")
    return f"crawl-report-{ts}.csv"


def main():
    parser = argparse.ArgumentParser(
        description="Website crawler → outputs 6 columns (Sheets-safe) CSV"
    )
    parser.add_argument(
        "-i", "--input", type=str, default="urls.txt",
        help="Path to input file containing URLs (one per line). Default: urls.txt"
    )
    parser.add_argument(
        "-o", "--out-dir", type=str, default=".",
        help="Output directory. Default: current folder"
    )
    args = parser.parse_args()

    urls = load_urls(Path(args.input))
    if not urls:
        print("No URLs found in input file.")
        return

    df = crawl_urls(urls)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / generate_filename()

    # CSV written in a way Google Sheets won't break columns
    df.to_csv(
        out_file,
        index=False,
        encoding="utf-8-sig",
        quoting=csv.QUOTE_ALL
    )

    print(f"\n[INFO] Saved CSV report to: {out_file.resolve()}")

    print("\n=== Crawl Report ===")
    print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))


if __name__ == "__main__":
    main()
