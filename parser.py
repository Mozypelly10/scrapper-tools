# parser.py - Handles HTML parsing logic

from bs4 import BeautifulSoup


def parse_html(html, tag=None, class_name=None, id_name=None, transactions=False):
    soup = BeautifulSoup(html, "lxml")
    results = []

    if transactions or _looks_like_transactions(soup):
        return extract_transactions(soup)

    if id_name:
        element = soup.find(id=id_name)
        if element:
            text = element.get_text(strip=True)
            if text:
                results.append(text)

    elif class_name:
        elements = soup.find_all(tag or True, class_=class_name)
        for el in elements:
            text = el.get_text(strip=True)
            if text:
                results.append(text)

    elif tag:
        elements = soup.find_all(tag)
        for el in elements:
            text = el.get_text(strip=True)
            if text:
                results.append(text)

    else:
        text = soup.get_text(strip=True)
        if text:
            results.append(text)

    return results


def _looks_like_transactions(soup):
    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")
        if len(rows) > 2:
            return True

    transaction_keywords = [
        "transaction", "history", "bet", "stake", "odds",
        "payout", "debit", "credit", "balance", "order",
        "amount", "status", "date", "result"
    ]

    page_text = soup.get_text().lower()
    matches = sum(1 for keyword in transaction_keywords if keyword in page_text)

    if matches >= 3:
        all_divs = soup.find_all("div", class_=True)
        class_counts = {}
        for div in all_divs:
            for cls in div.get("class", []):
                class_counts[cls] = class_counts.get(cls, 0) + 1

        if any(count >= 3 for count in class_counts.values()):
            return True

    return False


def extract_transactions(soup):
    results = []

    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")
        if not rows:
            continue

        headers = [th.get_text(strip=True) for th in rows[0].find_all(["th", "td"])]

        for row in rows[1:]:
            cells = [td.get_text(strip=True) for td in row.find_all("td")]
            if cells:
                if headers and len(headers) == len(cells):
                    results.append(dict(zip(headers, cells)))
                else:
                    results.append({"row": cells})

    if not results:
        all_divs = soup.find_all("div", class_=True)
        class_counts = {}
        for div in all_divs:
            for cls in div.get("class", []):
                class_counts[cls] = class_counts.get(cls, 0) + 1

        if class_counts:
            top_class = max(class_counts, key=class_counts.get)
            if class_counts[top_class] >= 3:
                record_divs = soup.find_all("div", class_=top_class)
                for div in record_divs:
                    text = div.get_text(separator=" | ", strip=True)
                    if text:
                        results.append({"record": text})

    return results
