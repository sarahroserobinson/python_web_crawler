# Python Web Crawler

This project is a Python-based web crawler that:

- Crawls a site up to a specified depth
- Respects `robots.txt`
- Extracts and records page titles
- Exports visited pages to `.csv` or `.json`
- Generates dynamic filenames using the site domain and crawl date
- Allows the user to specify the crawl depth and output format

---

## Getting Started

### Requirements

- Python 3.8+
- `requests`
- `beautifulsoup4`

Install dependencies (if needed):

```bash
pip install requests beautifulsoup4
```

### How to Run
```
from crawler import Crawl

crawler = Crawl(
    robot_url="https://example.com/robots.txt",
    start_url="https://example.com",
    max_depth=2,
    format="json"  # or "csv"
)

crawler.run()
```

### Features
- Respects robots.txt rules
- Automatically avoids mailto, javascript, and anchor links
- Configurable crawl depth
- Output format: CSV or JSON
- Polite crawling with a 1-second delay between requests
- Dynamic filename generation based on domain + date