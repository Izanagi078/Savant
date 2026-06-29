"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  HomeIcon,
  BookOpenIcon,
  ClipboardIcon,
  ChartBarIcon,
  SparklesIcon,
} from "@heroicons/react/24/outline";

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);
  const pathname = usePathname();

  const links = [
    { href: "/", label: "Workspace", icon: HomeIcon },
    { href: "/quiz", label: "Quizzes", icon: ClipboardIcon },
    { href: "/performance", label: "Analytics", icon: ChartBarIcon },
  ];

  return (
    <aside
      className={`flex flex-col bg-[#070913] text-zinc-300 h-full border-r border-zinc-800/40 transition-all duration-300 select-none ${
        isOpen ? "w-64" : "w-18"
      }`}
    >
      {/* Brand Header */}
      <div className="flex items-center gap-3 p-5 border-b border-zinc-800/40 overflow-hidden">
        <SparklesIcon className="h-6 w-6 text-cyan-400 shrink-0 animate-pulse" />
        {isOpen && (
          <span className="font-extrabold tracking-wider bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent text-lg">
            SmartTutor
          </span>
        )}
      </div>

      {/* Nav Section */}
      <nav className="flex-1 py-6 flex flex-col gap-2 px-3">
        {links.map((link) => {
          const Icon = link.icon;
          const isActive = pathname === link.href;
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group relative ${
                isActive
                  ? "bg-gradient-to-r from-cyan-500/10 to-blue-500/10 text-cyan-400 border-l-2 border-cyan-400 shadow-[0_0_15px_rgba(6,182,212,0.05)]"
                  : "hover:bg-zinc-800/30 hover:text-zinc-100"
              }`}
            >
              <Icon
                className={`h-5 w-5 shrink-0 transition-transform group-hover:scale-105 ${
                  isActive ? "text-cyan-400" : "text-zinc-500 group-hover:text-zinc-300"
                }`}
              />
              {isOpen && <span className="text-sm font-medium">{link.label}</span>}
              
              {/* Tooltip for collapsed state */}
              {!isOpen && (
                <div className="absolute left-20 scale-0 group-hover:scale-100 bg-zinc-950 text-xs text-zinc-200 px-3 py-1.5 rounded-lg border border-zinc-800 transition-all duration-150 shadow-md shadow-black/80 z-50 pointer-events-none whitespace-nowrap">
                  {link.label}
                </div>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Collapser Toggle Footer */}
      <div className="p-4 border-t border-zinc-800/40">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-center p-2 rounded-lg bg-zinc-900/40 border border-zinc-800/40 hover:bg-zinc-800/40 text-zinc-400 hover:text-zinc-200 transition cursor-pointer text-xs font-semibold"
        >
          {isOpen ? "◀ Collapse" : "▶"}
        </button>
      </div>
    </aside>
  );
}
