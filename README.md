# Scrapper Tools

A custom command-line web scraping tool built in Python. Extract data from any website by tag, class, ID, or transaction mode. Results are saved to JSON or CSV with full scrape history logging.

## Features

- Scrape by HTML tag, class name, or element ID
- Auto-detect and extract transaction/table data
- Save results to JSON or CSV
- Timestamped output files
- Full scrape history log viewable from terminal

## Installation

Clone the repo and navigate into it, create and activate a virtual environment, then install dependencies with pip install -r requirements.txt.

## Usage

Scrape by tag: python scraper.py --url https://example.com --tag h1

Scrape by class: python scraper.py --url https://example.com --class-name price

Scrape by ID: python scraper.py --url https://example.com --id main-content

Transaction mode: python scraper.py --url https://example.com --transactions --format csv

View scrape history: python scraper.py --history

## Options

--url : Target URL to scrape
--tag : HTML tag to extract
--class-name : HTML class to extract
--id : HTML element ID to extract
--transactions : Enable transaction/table mode
--format : Output format: json or csv
--output : Output filename without extension
--delay : Delay in seconds between requests
--history : Show scrape history

## Author
BBuilt by @Mozypelly10
