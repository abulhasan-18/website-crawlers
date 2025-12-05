# generate_urls.py
from datetime import date, timedelta

BASE_URL = "http://localhost:3000"
START_DATE = date(2023, 1, 1)
END_DATE = date(2025, 12, 31)  # inclusive
OUT_FILE = "urls.txt"

def daterange(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)

with open(OUT_FILE, "w", encoding="utf-8") as f:
    for d in daterange(START_DATE, END_DATE):
        f.write(f"{BASE_URL}/astrology/{d.isoformat()}\n")

print(f"✅ Wrote URLs to: {OUT_FILE}")
