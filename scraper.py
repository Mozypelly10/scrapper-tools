# scraper.py - Main entry point for the scraper tool

import argparse
import time
import httpx

from config import HEADERS, REQUEST_TIMEOUT, REQUEST_DELAY, DEFAULT_OUTPUT_FORMAT, DEFAULT_OUTPUT_FILE
from parser import parse_html
from output import save_results, log_history, show_history


def fetch_page(url):
    try:
        print("[*] Fetching: " + url)
        with httpx.Client(http2=True, headers=HEADERS, timeout=REQUEST_TIMEOUT, follow_redirects=True, verify=False) as client:
            response = client.get(url)
            response.raise_for_status()
            print("[+] Success - Status: " + str(response.status_code))
            return response.text
    except httpx.HTTPStatusError as e:
        print("[!] HTTP Error: " + str(e))
    except httpx.ConnectError:
        print("[!] Connection failed. Check the URL or your internet.")
    except httpx.TimeoutException:
        print("[!] Request timed out after " + str(REQUEST_TIMEOUT) + " seconds.")
    except Exception as e:
        print("[!] Unexpected error: " + str(e))
    return None


def determine_mode(args):
    if args.transactions:
        return "transactions"
    elif args.id:
        return "id=" + args.id
    elif args.class_name:
        return "class=" + args.class_name
    elif args.tag:
        return "tag=" + args.tag
    else:
        return "full-text"


def main():
    parser = argparse.ArgumentParser(
        description="Custom Web Scraper Tool",
        epilog="Example: python scraper.py --url https://example.com --tag h3 --format json"
    )

    parser.add_argument("--url", type=str, help="Target URL to scrape")
    parser.add_argument("--tag", type=str, help="HTML tag to extract (e.g. h1, p, a)")
    parser.add_argument("--class-name", type=str, dest="class_name", help="HTML class to extract (e.g. price)")
    parser.add_argument("--id", type=str, help="HTML element ID to extract (e.g. main-content)")
    parser.add_argument("--transactions", action="store_true", help="Enable transaction/table extraction mode")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT_FILE, help="Output filename without extension")
    parser.add_argument("--format", type=str, choices=["json", "csv"], default=DEFAULT_OUTPUT_FORMAT, help="Output format: json or csv")
    parser.add_argument("--history", action="store_true", help="Show scrape history")
    parser.add_argument("--delay", type=float, default=REQUEST_DELAY, help="Delay in seconds between requests")

    args = parser.parse_args()

    if args.history:
        show_history()
        return

    if not args.url:
        print("[!] Please provide a URL with --url")
        parser.print_help()
        return

    html = fetch_page(args.url)
    if not html:
        print("[!] Could not retrieve page. Exiting.")
        return

    time.sleep(args.delay)

    mode = determine_mode(args)
    print("[*] Scraping mode: " + mode)

    results = parse_html(
        html,
        tag=args.tag,
        class_name=args.class_name,
        id_name=args.id,
        transactions=args.transactions
    )

    if not results:
        print("[!] No data found with the given parameters.")
        return

    print("[+] Extracted " + str(len(results)) + " result(s)")

    output_file = save_results(results, filename=args.output, format=args.format)

    log_history(args.url, mode, len(results), output_file)


if __name__ == "__main__":
    main()
