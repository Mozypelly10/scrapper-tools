# output.py - Handles saving scraped results

import json
import csv
import os
from datetime import datetime


def save_results(data, filename="results", format="json"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = filename + "_" + timestamp + "." + format

    if format == "json":
        _save_json(data, output_file)
    elif format == "csv":
        _save_csv(data, output_file)
    else:
        print("[!] Unknown format. Defaulting to JSON.")
        output_file = filename + "_" + timestamp + ".json"
        _save_json(data, output_file)

    print("[+] Results saved to: " + output_file)
    return output_file


def _save_json(data, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def _save_csv(data, filepath):
    if not data:
        print("[!] No data to save.")
        return

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        if isinstance(data[0], dict):
            headers = list(data[0].keys())
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        else:
            writer = csv.writer(f)
            writer.writerow(["extracted_text"])
            for item in data:
                writer.writerow([item])


def log_history(url, mode, result_count, output_file):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "url": url,
        "mode": mode,
        "results_found": result_count,
        "saved_to": output_file
    }

    history_file = "history.log"
    with open(history_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")


def show_history():
    history_file = "history.log"

    if not os.path.exists(history_file):
        print("[!] No history found yet.")
        return

    print("\n--- Scrape History ---\n")
    with open(history_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if not lines:
            print("[!] History is empty.")
            return
        for line in lines:
            entry = json.loads(line.strip())
            print("[" + entry["timestamp"] + "] " + entry["url"])
            print("    Mode     : " + entry["mode"])
            print("    Results  : " + str(entry["results_found"]))
            print("    Saved to : " + entry["saved_to"])
            print()
