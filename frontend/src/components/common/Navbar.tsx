import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="border-b px-6 py-4 flex gap-6 items-center">
      <Link
        href="/"
        className="font-bold text-xl"
      >
        EAIKA
      </Link>

      <Link href="/dashboard">
        Dashboard
      </Link>

      <Link href="/chat">
        Chat
      </Link>

      <Link href="/upload">
        Upload
      </Link>

      <Link href="/login">
        Login
      </Link>

      <Link href="/register">
        Register
      </Link>
    </nav>
  );
}
