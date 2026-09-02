from django.core.management.base import BaseCommand
from api.models import Listing
from collectors.the_cannon import scrape_the_cannon
from collectors.places4students import scrape_places4students
from datetime import date
import re


class Command(BaseCommand):
    help = "Scrape rental listings and save them to database"

    def handle(self, *args, **kwargs):
        listings = []

        cannon = scrape_the_cannon()
        places = scrape_places4students()

        print("The Cannon found:", len(cannon))
        print("Places4Students found:", len(places))

        listings.extend(cannon)
        listings.extend(places)

        for item in listings:
            price_text = str(item.get("Price", "0")).replace(",", "")
            price_match = re.search(r"\d+", price_text)
            price = int(price_match.group()) if price_match else 0

            Listing.objects.update_or_create(
                link=item.get("Link"),
                defaults={
                    "scraper": item.get("Source", ""),
                    "status": "Active",
                    "address": item.get("Title", "Unknown Address"),
                    "price": price,
                    "description": item.get("Description", ""),
                    "date_posted": date.today(),
                    "date_available": date.today(),
                    "bedroom_count": int(item.get("Bedrooms")) if str(item.get("Bedrooms")).isdigit() else None,
                    "bathroom_count": int(float(item.get("Bathrooms"))) if item.get("Bathrooms") not in ["N/A", None, ""] else None,
                    "utilities": item.get("Utilities Included", False),
                }
            )

        print(f"Saved {len(listings)} listings")