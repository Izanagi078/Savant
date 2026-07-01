import type { Metadata } from "next";
import MainLayout from "@/components/MainLayout";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "Savant",
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
        <MainLayout>{children}</MainLayout>
      </body>
    </html>
  );
}
