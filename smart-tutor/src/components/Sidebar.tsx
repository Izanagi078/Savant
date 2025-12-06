"use client";

import { useState } from "react";
import Link from "next/link";
import {
  HomeIcon,
  BookOpenIcon,
  ClipboardIcon,
  ChartBarIcon,
} from "@heroicons/react/24/outline";

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <aside
      className={`flex flex-col bg-blue-700 text-white h-full transition-all duration-300 ${
        isOpen ? "w-64" : "w-16"
      }`}
    >
      {/* Toggle button */}
      <div className="p-4 shrink-0">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="focus:outline-none"
        >
          {isOpen ? "<" : ">"}
        </button>
      </div>

      {/* Scrollable nav area */}
      <nav className="flex-1 overflow-y-auto flex flex-col gap-4 mt-2">
        <Link href="/" className="flex items-center gap-2 px-4 py-2 hover:bg-blue-600">
          <HomeIcon className="h-6 w-6" />
          {isOpen && <span>Home</span>}
        </Link>
        <Link href="/content" className="flex items-center gap-2 px-4 py-2 hover:bg-blue-600">
          <BookOpenIcon className="h-6 w-6" />
          {isOpen && <span>Content</span>}
        </Link>
        <Link href="/quiz" className="flex items-center gap-2 px-4 py-2 hover:bg-blue-600">
          <ClipboardIcon className="h-6 w-6" />
          {isOpen && <span>Quiz</span>}
        </Link>
        <Link href="/performance" className="flex items-center gap-2 px-4 py-2 hover:bg-blue-600">
          <ChartBarIcon className="h-6 w-6" />
          {isOpen && <span>Performance</span>}
        </Link>
      </nav>
    </aside>
  );
}
