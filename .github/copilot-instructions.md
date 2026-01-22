# Website SEO Crawler - AI Coding Agent Instructions

## Project Overview

This is a lightweight, dependency-minimal SEO crawler that audits websites by extracting essential on-page SEO metrics (status code, word count, title, meta description, H1 tags) from a list of URLs and exporting results to Excel.

**Core Workflow:**

1. `generate_urls.py` - Creates input file with URLs (one per line, supports `#` comments)
2. `crawler.py` - Fetches HTML, parses metadata, exports timestamped Excel reports to `reports/` directory

## Architecture & Key Patterns

### Core Components

- **`crawler.py` (Main Logic)**
  - `load_urls()` - Reads input file, skips blank lines and comments
  - `fetch_html()` - HTTP GET with Mozilla user-agent, 15s timeout, returns (html, status_str)
  - `extract_visible_text()` - Strips scripts, styles, headers/footers, counts words
  - `analyze_html()` - Extracts title, meta description, word count
  - `crawl_urls()` - Maps URLs → DataFrame with consistent column order
  - Returns pandas DataFrame with fixed `COLUMNS` list for output consistency

- **`generate_urls.py` (Utility)**
  - CLI helper to generate URL lists for batch testing
  - Date range iteration for temporal URL patterns (e.g., `/astrology/YYYY-MM-DD`)
  - Not part of core pipeline, manual execution only

### Data Flow

```
urls.txt (one URL per line)
    ↓
[fetch_html + analyze_html for each URL]
    ↓
pandas DataFrame with 6 columns
    ↓
reports/crawl-report-{timestamp}.xlsx
```

### Critical Design Decisions

- **No browser automation** - Uses `requests` + `BeautifulSoup` for speed; acceptable for SEO audits
- **Text cleaning** - `clean_text()` removes newlines and normalizes whitespace for Excel safety
- **Visible text extraction** - Strips script/style/header/footer tags before word count (more accurate than raw HTML)
- **Timestamp in filenames** - Format: `crawl-report-DD-MM-YYYY HH-MM AM/PM.xlsx` prevents overwrites
- **Always creates `reports/` subdirectory** - Keeps root clean; allows `--out-dir` override

## Developer Workflows

### Running the Crawler

```bash
# Basic usage (reads urls.txt, outputs to reports/)
python crawler.py

# Custom input file
python crawler.py -i custom_urls.txt

# Custom output directory
python crawler.py -o /path/to/output
```

### Generating URLs (for testing)

```bash
python generate_urls.py  # Generates urls.txt with date range URLs
```

### URL File Format

- One URL per line
- Lines starting with `#` are skipped (comments)
- Blank lines ignored
- Leading/trailing whitespace stripped

## Project Conventions & Patterns

- **HTTP Error Handling** - Non-200 responses return None for HTML but capture status string; rows still created with 0 word count
- **Exception Handling** - `requests.RequestException` caught generically, error message included in status column
- **Type Hints** - Used throughout (`str`, `list[str]`, `tuple[...]`, `dict`, `pd.DataFrame`) for code clarity
- **Path Handling** - Uses `pathlib.Path` for cross-platform compatibility
- **Column Consistency** - `COLUMNS` list at top of `crawler.py` defines exact output order; always respected

## Dependencies

```
requests          # HTTP fetching
beautifulsoup4    # HTML parsing
pandas            # DataFrame output
tabulate          # Console formatting (imported but unused in code)
openpyxl          # Excel export engine (required by pandas.to_excel)
```

## Key Files to Reference

- [crawler.py](../crawler.py) - All extraction logic; modify here for new SEO metrics
- [generate_urls.py](../generate_urls.py) - URL generation template
- [urls.txt](../urls.txt) - Input format reference
- [README.md](../README.md) - Feature list and usage examples

## Common Modifications

- **Add new SEO column** - Update `COLUMNS` list, add extraction logic in `analyze_html()`, update row dict in `crawl_urls()`
- **Change timeout** - Modify `timeout` parameter in `fetch_html()` function (default: 15s)
- **Skip URL patterns** - Add logic in `load_urls()` after strip/comment checks
- **Export format** - Replace `df.to_excel()` call; DataFrame structure remains identical
