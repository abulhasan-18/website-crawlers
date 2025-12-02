# 🕷️ Website SEO Crawler (Python)

A lightweight and fast Python-based SEO crawler that scans multiple URLs and extracts essential on-page SEO data. Perfect for auditing websites, validating staging builds, and quickly checking content quality. Just provide a list of URLs — the crawler does the rest.

---

## 🚀 Features

This crawler automatically extracts:

### 🔍 SEO Insights Per URL
- **HTTP Status** (e.g., `200 OK`, `404 Not Found`)
- **Visible Content Word Count**
- **Title**
- **Title Length**
- **Meta Description**
- **Meta Description Length**
- **Has H1** (`Yes` / `No`)
- **H1 Count**
- **First H1 Text**

### 📄 Outputs
- **CSV Report** (`crawl_report.csv`)
- **Pretty Console Table** (formatted using `tabulate`)

### ⚡ Highlights
- No browser automation  
- No API keys  
- Faster and lighter than ScreamingFrog for small audits  
- Extremely easy to modify

---

## 📁 Project Structure

📦 website-seo-crawler
├── crawler.py # Main crawler script
├── urls.txt # Input URL list (one per line)
├── crawl_report.csv # Output SEO report (auto-generated)
└── README.md # Documentation

