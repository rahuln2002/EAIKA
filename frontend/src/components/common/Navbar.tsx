import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="p-4 border-b flex gap-4">
      <Link href="/dashboard">
        Dashboard
      </Link>

      <Link href="/chat">
        Chat
      </Link>

      <Link href="/upload">
        Upload
      </Link>

      <Link href="/register">
        Register
      </Link>
    </nav>
  );
}
