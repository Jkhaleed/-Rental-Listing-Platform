import pandas as pd

from collectors.the_cannon import scrape_the_cannon
from collectors.places4students import scrape_places4students


def main():
    all_listings = []

    print("Starting The Cannon scraper...")
    all_listings.extend(scrape_the_cannon())

    print("\nStarting Places4Students scraper...")
    all_listings.extend(scrape_places4students())

    df = pd.DataFrame(all_listings)

    if not df.empty:
        df.drop_duplicates(subset=["Link"], inplace=True)

    df.to_csv("houses.csv", index=False)

    print(f"\nSaved {len(df)} listings to houses.csv")


if __name__ == "__main__":
    main()