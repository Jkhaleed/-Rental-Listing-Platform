import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold">Rental Finder</h1>
      <p className="mt-3 text-gray-600">Find updated rental listings in Guelph.</p>

      <Link
        href="/listings"
        className="mt-6 bg-black text-white px-5 py-3 rounded-xl"
      >
        View Listings
      </Link>
    </main>
  );
}