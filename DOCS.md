# Scrapper Tools - Full Documentation

## Table of Contents

1. Overview
2. Project Structure
3. Installation
4. Configuration
5. How It Works
6. File Breakdown
7. Usage & Commands
8. Output Formats
9. Transaction Mode
10. Scrape History
11. Error Handling
12. Examples
13. Limitations
14. Future Improvements

---

## 1. Overview

Scrapper Tools is a custom command-line web scraping tool built in Python.
It allows you to extract data from any publicly accessible website using
different scraping modes. Results are saved to JSON or CSV files with
automatic timestamping. Every scrape is logged to a history file for
reference.

This tool was built from scratch without relying on third-party scraping
frameworks like Scrapy. It uses only the core libraries needed:
requests for fetching pages and BeautifulSoup for parsing HTML.

---

## 2. Project Structure

scrapper_tools/
    scraper.py        - Main entry point. Handles CLI arguments and coordinates all modules.
    parser.py         - Handles all HTML parsing logic and scraping modes.
    output.py         - Handles saving results to JSON or CSV and logging history.
    config.py         - Default settings: headers, timeout, delay, output format.
    requirements.txt  - Python dependencies.
    README.md         - Quick start guide.
    DOCS.md           - This file. Full project documentation.
    history.log       - Auto-generated. Stores scrape history logs.

---

## 3. Installation

Step 1 - Clone the repository:
    git clone https://github.com/Mozypelly10/scrapper-tools.git
    cd scrapper-tools

Step 2 - Create a virtual environment:
    python3 -m venv .venv

Step 3 - Activate the virtual environment:
    On Mac/Linux:  source .venv/bin/activate
    On Windows:    .venv\Scripts\activate

Step 4 - Install dependencies:
    pip install -r requirements.txt

Step 5 - Run the tool:
    python scraper.py --url https://example.com --tag h1

---

## 4. Configuration

All default settings are stored in config.py.

HEADERS
    A dictionary containing the User-Agent string sent with every HTTP request.
    By default it mimics a real Chrome browser on Windows to avoid being
    blocked by servers that reject bot requests.

REQUEST_TIMEOUT
    How long in seconds the tool waits for a server to respond before giving up.
    Default is 10 seconds.

REQUEST_DELAY
    How long in seconds the tool waits after fetching a page before processing.
    Default is 1 second. This is a courtesy delay to avoid hammering servers.
    Can be overridden at runtime with the --delay flag.

DEFAULT_OUTPUT_FORMAT
    The default file format for saving results. Default is json.
    Can be overridden at runtime with the --format flag.

DEFAULT_OUTPUT_FILE
    The base name for output files. Default is results.
    Can be overridden at runtime with the --output flag.

---

## 5. How It Works

When you run a scrape command, the tool follows these steps:

Step 1 - Parse arguments
    The CLI reads the flags you passed (URL, tag, class, format, etc.)

Step 2 - Fetch the page
    scraper.py sends an HTTP GET request to the target URL using the
    requests library. The User-Agent header in config.py is sent along
    with the request to mimic a real browser.

Step 3 - Check the response
    If the server returns an error (404, 500, etc.), the tool reports it
    and exits cleanly. If successful, the raw HTML is passed to the parser.

Step 4 - Parse the HTML
    parser.py receives the raw HTML and uses BeautifulSoup to parse it.
    Depending on the flags provided, it extracts data by tag, class, ID,
    or transaction mode.

Step 5 - Save the results
    output.py takes the extracted data and saves it to a timestamped
    JSON or CSV file in the project folder.

Step 6 - Log to history
    A record of the scrape is appended to history.log including the
    timestamp, URL, mode used, number of results, and output filename.

---

## 6. File Breakdown

### scraper.py

This is the main file you run. It does three things:
- Defines all CLI arguments using Python's argparse module
- Coordinates the flow between fetching, parsing, and saving
- Handles the --history flag to display past scrapes

Key functions:
    fetch_page(url)       - Sends HTTP request and returns raw HTML
    determine_mode(args)  - Identifies which scraping mode is active
    main()                - Entry point that ties everything together

### parser.py

This file handles all HTML parsing. It receives raw HTML and returns
a list of extracted data based on the scraping mode selected.

Key functions:
    parse_html()              - Main parsing function. Routes to correct mode.
    _looks_like_transactions() - Auto-detects if page contains transaction data
    extract_transactions()    - Extracts structured data from tables or div lists

### output.py

This file handles all output operations including saving files and logging.

Key functions:
    save_results()   - Saves extracted data to JSON or CSV
    _save_json()     - Writes data to a JSON file
    _save_csv()      - Writes data to a CSV file with proper headers
    log_history()    - Appends a scrape record to history.log
    show_history()   - Reads and prints history.log to the terminal

### config.py

Stores all default settings in one place. Edit this file to change
the tool's default behavior without touching the main code.

---

## 7. Usage & Commands

Basic syntax:
    python scraper.py --url <URL> [OPTIONS]

All available flags:

    --url           Target URL to scrape (required)
    --tag           HTML tag to extract e.g. h1, p, a, li
    --class-name    HTML class attribute to target e.g. price, title
    --id            HTML element ID to target e.g. main-content
    --transactions  Enable transaction/table extraction mode
    --format        Output format: json or csv (default: json)
    --output        Base name for output file (default: results)
    --delay         Seconds to wait between requests (default: 1)
    --history       Display full scrape history and exit

---

## 8. Output Formats

### JSON

Default format. Results are saved as a JSON array. Each item is either
a plain string (for tag/class/ID/full-text mode) or a dictionary
(for transaction mode).

Example output for tag mode:
    [
        "A Light in the Attic",
        "Tipping the Velvet",
        "Soumission"
    ]

Example output for transaction mode:
    [
        {"Date": "2026-01-01", "Description": "Deposit", "Amount": "5000"},
        {"Date": "2026-01-02", "Description": "Withdrawal", "Amount": "1500"}
    ]

### CSV

Results are saved as a CSV file with headers. For plain text results
the header is extracted_text. For transaction mode the headers are
taken from the table headers found on the page.

Output filenames always include a timestamp to prevent overwriting:
    results_20260609_032013.json
    results_20260609_032013.csv

---

## 9. Transaction Mode

Transaction mode is designed to extract structured data from pages that
display records in table or list format. Examples include:

- Betting history pages
- Bank account statements
- Order history on e-commerce sites
- Sports results tables
- Any page with repeating structured records

### Auto-detection

When you run a scrape without the --transactions flag, the tool still
checks the page automatically. It looks for two things:

1. HTML tables with more than 2 rows
2. Transaction-related keywords in the page text combined with
   repeating div class patterns

If either condition is met, transaction mode activates automatically.

### Manual trigger

You can force transaction mode with the --transactions flag:
    python scraper.py --url https://example.com --transactions --format csv

### How it extracts data

For HTML tables:
    It reads the first row as headers and maps each subsequent row
    to those headers creating a clean dictionary per record.

For div-based layouts:
    It finds the most repeated CSS class on the page (which is usually
    the class applied to each record row) and extracts the text from
    each matching div.

---

## 10. Scrape History

Every time you run a scrape, the tool automatically logs it to history.log.
Each log entry contains:

- Timestamp of the scrape
- URL that was scraped
- Mode used (tag, class, id, transactions, full-text)
- Number of results extracted
- Name of the output file saved

To view your full scrape history in the terminal:
    python scraper.py --history

Example output:
    --- Scrape History ---

    [2026-06-09 03:20:13] https://books.toscrape.com
        Mode     : tag=h3
        Results  : 20
        Saved to : results_20260609_032013.json

The history.log file is excluded from git via .gitignore so your
scrape records stay private on your local machine.

---

## 11. Error Handling

The tool handles the following errors gracefully:

HTTP Error
    Server returned an error status like 404 or 500.
    The tool prints the error code and exits without crashing.

Connection Error
    The URL could not be reached. Could be a wrong URL, no internet,
    or the server is down.

Timeout
    The server took too long to respond. Default timeout is 10 seconds.
    Increase it in config.py if needed.

No Results Found
    The tag, class, or ID you specified was not found on the page.
    The tool notifies you and exits without saving an empty file.

Unknown Output Format
    If an unsupported format is passed, the tool defaults to JSON
    and notifies you.

---

## 12. Examples

Scrape all book titles from a bookstore:
    python scraper.py --url https://books.toscrape.com --tag h3 --format json

Scrape all prices by class name:
    python scraper.py --url https://books.toscrape.com --class-name price_color --format csv

Scrape a specific section by ID:
    python scraper.py --url https://example.com --id main-content --format json

Extract a transaction table and save as CSV:
    python scraper.py --url https://datatables.net/examples/basic_init/zero_configuration.html --transactions --format csv

Scrape with a longer delay to be polite to the server:
    python scraper.py --url https://example.com --tag p --delay 3

Save output with a custom filename:
    python scraper.py --url https://example.com --tag a --output links

View scrape history:
    python scraper.py --history

---

## 13. Limitations

- Does not handle JavaScript-rendered pages. Sites that load content
  dynamically with JavaScript will return incomplete or empty results.
  This will be addressed in a future version using Playwright or Selenium.

- Does not handle login-protected pages. Pages behind authentication
  walls require session handling which is not yet implemented.

- Single URL per run. The tool currently scrapes one URL at a time.
  Bulk URL scraping from a list will be added in a future version.

- No proxy support yet. If a site blocks your IP, there is currently
  no built-in proxy rotation. This will be added later.

---

## 14. Future Improvements

- JavaScript rendering support via Playwright
- Login/session handling for authenticated pages
- Bulk URL scraping from a text file
- Proxy rotation to avoid IP blocks
- Scheduled scraping with cron-like intervals
- Email or webhook alerts when scrape completes
- GUI version for non-technical users

---

## Author

Built by Mozypelly - Network Security Engineer & Ethical Hacker
GitHub: https://github.com/Mozypelly10
X: @mozypellyXP

