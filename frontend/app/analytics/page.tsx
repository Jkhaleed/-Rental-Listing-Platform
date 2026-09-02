type Listing = {
  id: string;
  scraper: string;
  status: string;
  price: number;
  address: string;
  bedroom_count: number | null;
  bathroom_count: number | null;
  utilities: boolean | null;
};

type ApiResponse = {
  count: number;
  results: Listing[];
};

export default async function AnalyticsPage() {
  const res = await fetch("http://127.0.0.1:8000/api/listings/?status=All", {
    cache: "no-store",
  });

  const data: ApiResponse = await res.json();
  const listings = data.results ?? [];

  const validPrices = listings
    .map((listing) => listing.price)
    .filter((price) => price > 0);

  const totalListings = listings.length;

  const averagePrice =
    validPrices.length > 0
      ? Math.round(validPrices.reduce((sum, price) => sum + price, 0) / validPrices.length)
      : 0;

  const cheapest = listings.reduce(
    (min, listing) =>
      listing.price > 0 && listing.price < min.price ? listing : min,
    listings[0]
  );

  const mostExpensive = listings.reduce(
    (max, listing) =>
      listing.price > max.price ? listing : max,
    listings[0]
  );

  const utilitiesIncluded = listings.filter(
    (listing) => listing.utilities === true
  ).length;

  const listingsBySource = listings.reduce<Record<string, number>>(
    (acc, listing) => {
      const source = listing.scraper || "Unknown";
      acc[source] = (acc[source] || 0) + 1;
      return acc;
    },
    {}
  );

  const averageByBedroom = listings.reduce<Record<string, { total: number; count: number }>>(
    (acc, listing) => {
      if (!listing.bedroom_count || listing.price <= 0) return acc;

      const key = `${listing.bedroom_count} Bedroom`;

      if (!acc[key]) {
        acc[key] = { total: 0, count: 0 };
      }

      acc[key].total += listing.price;
      acc[key].count += 1;

      return acc;
    },
    {}
  );

  return (
    <main className="min-h-screen p-8">
      <h1 className="text-3xl font-bold mb-6">Rental Market Analytics</h1>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="border rounded-xl p-5 shadow-sm">
          <p className="text-gray-500">Total Listings</p>
          <h2 className="text-2xl font-bold">{totalListings}</h2>
        </div>

        <div className="border rounded-xl p-5 shadow-sm">
          <p className="text-gray-500">Average Price</p>
          <h2 className="text-2xl font-bold">${averagePrice}</h2>
        </div>

        <div className="border rounded-xl p-5 shadow-sm">
          <p className="text-gray-500">Cheapest</p>
          <h2 className="text-2xl font-bold">
            ${cheapest?.price ?? 0}
          </h2>
        </div>

        <div className="border rounded-xl p-5 shadow-sm">
          <p className="text-gray-500">Most Expensive</p>
          <h2 className="text-2xl font-bold">
            ${mostExpensive?.price ?? 0}
          </h2>
        </div>
      </div>

      <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="border rounded-xl p-5 shadow-sm">
          <h2 className="text-xl font-semibold mb-4">Listings by Source</h2>

          {Object.entries(listingsBySource).map(([source, count]) => (
            <div key={source} className="flex justify-between border-b py-2">
              <span>{source}</span>
              <span className="font-semibold">{count}</span>
            </div>
          ))}
        </div>

        <div className="border rounded-xl p-5 shadow-sm">
          <h2 className="text-xl font-semibold mb-4">
            Average Price by Bedroom
          </h2>

          {Object.entries(averageByBedroom).map(([bedroom, value]) => (
            <div key={bedroom} className="flex justify-between border-b py-2">
              <span>{bedroom}</span>
              <span className="font-semibold">
                ${Math.round(value.total / value.count)}
              </span>
            </div>
          ))}
        </div>

        <div className="border rounded-xl p-5 shadow-sm">
          <h2 className="text-xl font-semibold mb-4">Utilities Included</h2>

          <p className="text-2xl font-bold">{utilitiesIncluded}</p>
          <p className="text-gray-500">
            out of {totalListings} listings
          </p>
        </div>
      </section>
    </main>
  );
}