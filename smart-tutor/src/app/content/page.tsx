// app/content/page.tsx
"use client";

import ContentCard from "@/components/ContentCard";

export default function ContentPage() {
  return (
    <main className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Learning Content</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ContentCard
          title="Introduction to Algebra"
          description="Learn the basics of algebra including variables, equations, and functions."
          image="https://source.unsplash.com/random/400x200?math"
        />
        <ContentCard
          title="Geometry Essentials"
          description="Explore shapes, angles, and theorems with interactive lessons."
          image="https://source.unsplash.com/random/400x200?geometry"
        />
        <ContentCard
          title="Statistics Fundamentals"
          description="Understand data, probability, and statistical methods."
          image="https://source.unsplash.com/random/400x200?statistics"
        />
      </div>
    </main>
  );
}
