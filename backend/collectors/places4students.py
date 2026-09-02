# scrapers/places4students.py

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_URL = "https://www.places4students.com"

LISTINGS_URL = (
    "https://www.places4students.com/"
    "schools/198/listings/properties"
)


def get_property_links():
    try:
        page = requests.get(
            LISTINGS_URL,
            headers=HEADERS,
            timeout=10
        )

        page.raise_for_status()

    except requests.RequestException as e:
        print(f"Could not load Places4Students listings page: {e}")
        return []

    soup = BeautifulSoup(page.text, "html.parser")

    property_links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/schools/198/listings/properties/" in href:
            full_url = urljoin(BASE_URL, href)
            property_links.add(full_url)

    return list(property_links)


def scrape_places4students():
    data = []

    property_urls = get_property_links()

    print(f"Found {len(property_urls)} Places4Students listings")

    for url in property_urls:
        print(f"Scraping Places4Students: {url}")

        try:
            page = requests.get(
                url,
                headers=HEADERS,
                timeout=10
            )

            # Skip dead listings
            if page.status_code != 200:
                print(
                    f"Skipping dead listing "
                    f"({page.status_code}): {url}"
                )
                continue

        except requests.RequestException as e:
            print(f"Could not check listing: {url}")
            print(e)
            continue

        soup = BeautifulSoup(page.text, "html.parser")

        title_tag = soup.find(
            "meta",
            property="og:title"
        )

        desc_tag = soup.find(
            "meta",
            property="og:description"
        )

        image_tag = soup.find(
            "meta",
            property="og:image"
        )

        title = (
            title_tag.get("content", "").strip()
            if title_tag
            else ""
        )

        desc = (
            desc_tag.get("content", "").strip()
            if desc_tag
            else ""
        )

        image = (
            image_tag.get("content", "").strip()
            if image_tag
            else ""
        )

        # If the page returned 200 but has no useful listing data,
        # it may still be an invalid/expired page.
        if not title and not desc:
            print(f"Skipping invalid listing: {url}")
            continue

        price = re.search(
            r'\$[\d,]+',
            f"{title} {desc}"
        )

        bedrooms = re.search(
            r'(\d+)\s*bed(room)?s?',
            desc,
            re.I
        )

        bathrooms = re.search(
            r'(\d+(\.\d+)?)\s*bath(room)?s?',
            desc,
            re.I
        )

        utilities = bool(
            re.search(
                r'('
                r'utilities included|'
                r'all utilities paid|'
                r'including utilities|'
                r'utilities and internet'
                r')',
                desc,
                re.I
            )
        )

        item = {
            "Source": "Places4Students",
            "Title": title if title else "N/A",
            "Link": url,
            "Price": price.group(0) if price else "N/A",
            "Posted": "N/A",
            "Description": desc if desc else "N/A",
            "Bedrooms": bedrooms.group(1) if bedrooms else "N/A",
            "Bathrooms": bathrooms.group(1) if bathrooms else "N/A",
            "Utilities Included": utilities,
            "Image": image if image else "N/A"
        }

        data.append(item)

    return data