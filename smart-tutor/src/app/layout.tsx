import type { Metadata } from "next";
import Sidebar from "@/components/Sidebar";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "Smart Tutor",
  description: "Personalized Course Builder and Tutor",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="flex h-screen bg-[#070913] text-zinc-100 antialiased overflow-hidden" suppressHydrationWarning>
        {/* Sidebar fills full height */}
        <Sidebar />
        {/* Main content area shifts right */}
        <main className="flex-1 bg-[#0A0C16] p-8 overflow-y-auto scrollbar-thin scrollbar-thumb-zinc-800">
          {children}
        </main>
      </body>
    </html>
  );
}
