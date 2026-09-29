import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PTScope",
  description: "Inteligencia territorial publica para Portugal.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="pt" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
