import "./globals.css";

import Navbar from "@/components/common/Navbar";

import Providers from "./providers";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <Navbar />

          <main>
            {children}
          </main>
        </Providers>
      </body>
    </html>
  );
}
