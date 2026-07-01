"use client";

import { usePathname } from "next/navigation";
import Sidebar from "./Sidebar";

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isAuthPage = pathname === "/auth";

  if (isAuthPage) {
    return (
      <main className="flex-1 min-h-screen bg-[#070913] overflow-y-auto">
        {children}
      </main>
    );
  }

  return (
    <>
      <Sidebar />
      <main className="flex-1 bg-[#0A0C16] p-8 overflow-y-auto scrollbar-thin scrollbar-thumb-zinc-800">
        {children}
      </main>
    </>
  );
}
