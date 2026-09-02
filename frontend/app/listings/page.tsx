type Listing = {
  id: string;
  link: string;
  scraper: string;
  status: string;
  price: number;
  address: string;
  description: string;
  date_posted: string;
  date_available: string;
  category_type: string;
  bedroom_count: number | null;
  bathroom_count: number | null;
  utilities: boolean | null;
};

type ListingResponse = {
  count: number;
  next: string | null;
  previous: string | null;
  results: Listing[];
};

export default async function ListingsPage() {
  const res = await fetch("http://127.0.0.1:8000/api/listings/", {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch listings");
  }

  const data: ListingResponse = await res.json();

  const listings = data.results;

  return (
    <main className="min-h-screen p-8">
      <h1 className="text-3xl font-bold mb-2">
        Guelph Rental Listings
      </h1>

      <p className="mb-6 text-gray-500">
        {data.count} listings found
      </p>

      <div className="grid gap-4">
        {listings.map((listing) => (
          <div
            key={listing.id}
            className="border rounded-xl p-5 shadow-sm"
          >
            <h2 className="text-xl font-semibold">
              {listing.address}
            </h2>

            <p className="font-bold text-lg text-green-700">
              ${listing.price}
            </p>

            <p className="text-gray-700 mt-2">
              {listing.description}
            </p>

            <div className="mt-3 space-y-1 text-sm">
              <p>
                Bedrooms: {listing.bedroom_count ?? "N/A"}
              </p>

              <p>
                Bathrooms: {listing.bathroom_count ?? "N/A"}
              </p>

              <p>
                Utilities:{" "}
                {listing.utilities
                  ? "Included"
                  : "Not Included"}
              </p>

              <p>Source: {listing.scraper}</p>
            </div>

            <a
              href={listing.link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline mt-3 inline-block"
            >
              View Original Listing
            </a>
          </div>
        ))}
      </div>
    </main>
  );
}