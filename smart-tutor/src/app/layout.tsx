import type { Metadata } from "next";
import Sidebar from "@/components/Sidebar";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "Smart Tutor",
  description: "AI-Powered Course Builder",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex h-screen">
        {/* Sidebar fills full height */}
        <Sidebar />
        {/* Main content area shifts right */}
        <main className="flex-1 bg-gray-50 p-6 overflow-y-auto">
          {children}
        </main>
      </body>
    </html>
  );
}
