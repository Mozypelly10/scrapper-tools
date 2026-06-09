# config.py - Default settings for the scraper

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

REQUEST_TIMEOUT = 10  # seconds

REQUEST_DELAY = 1  # seconds between requests

DEFAULT_OUTPUT_FORMAT = "json"  # options: json, csv

DEFAULT_OUTPUT_FILE = "results"  # filename without extension