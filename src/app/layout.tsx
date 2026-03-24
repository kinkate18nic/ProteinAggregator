import type { Metadata, Viewport } from "next";
import "./globals.css";

export const viewport: Viewport = {
  themeColor: "#111827",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export const metadata: Metadata = {
  title: "ProteinDB - Indian Protein Scorer",
  description: "Find the best cost-per-verified-gram of protein in India.",
  appleWebApp: {
    capable: true,
    title: "ProteinDB",
    statusBarStyle: "black-translucent",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-50 antialiased font-sans selection:bg-indigo-500/30">
        {children}
      </body>
    </html>
  );
}
