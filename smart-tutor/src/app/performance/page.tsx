// app/performance/page.tsx
"use client";

import PerformanceChart from "@/components/PerformanceChart";

export default function PerformancePage() {
  return (
    <main className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Performance Overview</h1>
      <PerformanceChart />
    </main>
  );
}
