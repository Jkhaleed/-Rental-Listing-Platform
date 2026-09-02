import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_URL = "https://thecannon.ca"


def is_valid_listing(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            allow_redirects=True
        )

        print(f"CHECKING: {url}")
        print(f"STATUS: {response.status_code}")

        return response.status_code == 200

    except requests.RequestException as e:
        print(f"ERROR checking {url}: {e}")
        return False


def scrape_the_cannon():
    current_page = 1
    data = []

    while True:
        print(f"Scraping The Cannon page {current_page}")

        url = f"https://thecannon.ca/housing/page/{current_page}/"

        try:
            page = requests.get(
                url,
                headers=HEADERS,
                timeout=10
            )

            page.raise_for_status()

        except requests.RequestException as e:
            print(f"Could not load page {current_page}: {e}")
            break

        soup = BeautifulSoup(page.text, "html.parser")

        all_rentals = soup.find_all(
            "li",
            class_="housing-item"
        )

        if not all_rentals:
            break

        for house in all_rentals:
            title_tag = house.find("h2")

            link_tag = (
                title_tag.find("a")
                if title_tag
                else None
            )

            if not link_tag or not link_tag.has_attr("href"):
                continue

            listing_url = urljoin(
                BASE_URL,
                link_tag["href"]
            )

            # IMPORTANT:
            # Do not add the listing unless the page exists.
            if not is_valid_listing(listing_url):
                print(f"SKIPPING DEAD LISTING: {listing_url}")
                continue

            price_tag = house.find(
                "li",
                class_="price"
            )

            posted_tag = house.find(
                "li",
                class_="post-date"
            )

            description_tag = house.find(
                "div",
                class_="description"
            )

            desc = (
                description_tag.text.strip()
                if description_tag
                else "N/A"
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
                    r'(utilities included|all utilities paid)',
                    desc,
                    re.I
                )
            )

            item = {
                "Source": "The Cannon",
                "Title": link_tag.text.strip(),
                "Link": listing_url,
                "Price": (
                    price_tag.find("dd").text.strip()
                    if price_tag and price_tag.find("dd")
                    else "N/A"
                ),
                "Posted": (
                    posted_tag.find("dd").text.strip()
                    if posted_tag and posted_tag.find("dd")
                    else "N/A"
                ),
                "Description": desc,
                "Bedrooms": (
                    bedrooms.group(1)
                    if bedrooms
                    else "N/A"
                ),
                "Bathrooms": (
                    bathrooms.group(1)
                    if bathrooms
                    else "N/A"
                ),
                "Utilities Included": utilities
            }

            data.append(item)

        current_page += 1

    return data