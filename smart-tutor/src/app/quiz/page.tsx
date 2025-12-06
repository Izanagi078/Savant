// app/quiz/page.tsx
"use client";

import QuizForm from "@/components/QuizForm";

export default function QuizPage() {
  return (
    <main className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Quiz Time</h1>
      <QuizForm />
    </main>
  );
}
