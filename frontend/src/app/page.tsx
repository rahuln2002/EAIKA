import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center gap-6">
      <h1 className="text-5xl font-bold">
        Enterprise AI Knowledge Assistant
      </h1>

      <p className="text-lg text-gray-600">
        Production-grade RAG AI platform
      </p>

      <div className="flex gap-4">
        <Link
          href="/login"
          className="px-4 py-2 bg-black text-white rounded"
        >
          Login
        </Link>

        <Link
          href="/register"
          className="px-4 py-2 bg-black text-white rounded"
        >
          Register
        </Link>

        <Link
          href="/chat"
          className="px-4 py-2 border rounded"
        >
          Chat
        </Link>

        <Link
          href="/upload"
          className="px-4 py-2 border rounded"
        >
          Upload
        </Link>
      </div>
    </main>
  );
}
