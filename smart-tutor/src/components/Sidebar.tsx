"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  HomeIcon,
  ClipboardIcon,
  ChartBarIcon,
  SparklesIcon,
  UserIcon,
  ArrowLeftOnRectangleIcon,
} from "@heroicons/react/24/outline";

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const links = [
    { href: "/", label: "Workspace", icon: HomeIcon },
    { href: "/quiz", label: "Quizzes", icon: ClipboardIcon },
    { href: "/performance", label: "Analytics", icon: ChartBarIcon },
    { href: "/profile", label: "Update Profile", icon: UserIcon },
  ];

  const handleLogout = async () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    router.push("/auth");
  };

  return (
    <aside className="flex flex-col bg-[#070913] text-zinc-300 h-full border-r border-zinc-800/40 w-56 select-none shrink-0">
      {/* Brand Header */}
      <div className="flex items-center gap-3 p-5 border-b border-zinc-800/40 overflow-hidden">
        <SparklesIcon className="h-5 w-5 text-cyan-400 shrink-0 animate-pulse" />
        <span className="font-extrabold tracking-wider bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent text-lg">
          Savant
        </span>
      </div>

      {/* Nav Section */}
      <nav className="flex-1 py-6 flex flex-col gap-2 px-3 overflow-y-auto">
        {links.map((link) => {
          const Icon = link.icon;
          const isActive = pathname === link.href;
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group cursor-pointer ${
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
              <span className="text-sm font-medium">{link.label}</span>
            </Link>
          );
        })}

        {/* Separator */}
        <div className="h-px bg-zinc-800/40 my-2 mx-2"></div>

        {/* Sign Out Button */}
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-red-500/5 hover:text-red-400 text-zinc-500 transition-all duration-200 group w-full text-left cursor-pointer"
        >
          <ArrowLeftOnRectangleIcon
            className="h-5 w-5 shrink-0 transition-transform group-hover:scale-105 text-zinc-500 group-hover:text-red-400"
          />
          <span className="text-sm font-medium">Sign Out</span>
        </button>
      </nav>
    </aside>
  );
}
