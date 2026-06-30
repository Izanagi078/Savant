// app/performance/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import PerformanceChart from "@/components/PerformanceChart";

interface Attempt {
  id: number;
  topic: string;
  score: number;
  total: number;
  percentage: number;
  timestamp: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export default function PerformancePage() {
  const router = useRouter();
  const [attempts, setAttempts] = useState<Attempt[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/auth");
      return;
    }

    async function fetchHistory() {
      try {
        const token = localStorage.getItem("token");
        const res = await fetch(`${API_BASE_URL}/performance/history`, {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });
        if (res.ok) {
          const data = await res.json();
          setAttempts(data);
        } else {
          setError("Failed to fetch performance history.");
        }
      } catch (err) {
        setError("Error connecting to the backend API.");
      } finally {
        setLoading(false);
      }
    }
    fetchHistory();
  }, [router]);

  // Aggregate metrics
  const totalAttempts = attempts.length;
  
  const avgScore = totalAttempts > 0 
    ? Math.round(attempts.reduce((sum, a) => sum + a.percentage, 0) / totalAttempts)
    : 0;

  const highestScore = totalAttempts > 0
    ? Math.round(Math.max(...attempts.map((a) => a.percentage)))
    : 0;

  return (
    <div className="max-w-6xl mx-auto space-y-10">
      {/* Header */}
      <div className="space-y-3">
        <h1 className="text-5xl font-black tracking-tight bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">
          Performance Analytics
        </h1>
        <p className="text-zinc-400 max-w-2xl text-base leading-relaxed">
          Monitor your score progressions, analyze details of previous quiz completions, and map your learning velocity over time.
        </p>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center p-24 bg-[#0e1122]/40 border border-zinc-800/40 rounded-2xl shadow-xl space-y-6">
          <div className="relative w-16 h-16">
            <div className="absolute inset-0 border-4 border-cyan-500/20 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
          </div>
          <p className="text-zinc-400 text-sm tracking-wide animate-pulse">Loading analytics database...</p>
        </div>
      ) : error ? (
        <div className="p-8 bg-red-500/5 border border-red-500/20 rounded-2xl text-center space-y-4">
          <span className="text-3xl">⚠️</span>
          <h3 className="text-xl font-bold text-red-400">Database Connection Offline</h3>
          <p className="text-zinc-400 max-w-md mx-auto text-sm">{error}</p>
        </div>
      ) : totalAttempts === 0 ? (
        <div className="p-16 bg-[#0e1122]/40 border border-zinc-800/40 rounded-2xl text-center space-y-6 shadow-xl">
          <span className="text-5xl">📊</span>
          <h3 className="text-2xl font-bold text-white">No Quiz Data Located</h3>
          <p className="text-zinc-400 max-w-md mx-auto text-sm">
            You haven't completed any quizzes yet. Generate and complete a quiz in the workspace to start tracking your scores!
          </p>
          <a
            href="/quiz"
            className="inline-block px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold rounded-xl transition duration-150 shadow-lg text-sm"
          >
            Take Your First Quiz
          </a>
        </div>
      ) : (
        <div className="space-y-8">
          {/* Glassmorphic Metrics Row */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gradient-to-br from-[#0e1122] to-zinc-950 border border-zinc-800/50 rounded-2xl p-6 shadow-lg flex flex-col justify-between">
              <span className="text-zinc-400 text-xs font-semibold uppercase tracking-wider">Total Quizzes Taken</span>
              <div className="mt-4 flex items-baseline justify-between">
                <span className="text-5xl font-black text-white">{totalAttempts}</span>
                <span className="text-cyan-400 text-xs font-bold px-2 py-1 bg-cyan-950/40 border border-cyan-800/35 rounded-lg">Active</span>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-[#0e1122] to-zinc-950 border border-zinc-800/50 rounded-2xl p-6 shadow-lg flex flex-col justify-between">
              <span className="text-zinc-400 text-xs font-semibold uppercase tracking-wider">Average Performance</span>
              <div className="mt-4 flex items-baseline justify-between">
                <span className={`text-5xl font-black ${avgScore >= 70 ? 'text-green-400' : avgScore >= 50 ? 'text-yellow-400' : 'text-red-400'}`}>
                  {avgScore}%
                </span>
                <span className="text-zinc-500 text-xs font-medium">All attempts</span>
              </div>
            </div>

            <div className="bg-gradient-to-br from-[#0e1122] to-zinc-950 border border-zinc-800/50 rounded-2xl p-6 shadow-lg flex flex-col justify-between">
              <span className="text-zinc-400 text-xs font-semibold uppercase tracking-wider">Personal Record</span>
              <div className="mt-4 flex items-baseline justify-between">
                <span className="text-5xl font-black text-emerald-400">{highestScore}%</span>
                <span className="text-emerald-400 text-xs font-bold px-2 py-1 bg-emerald-950/40 border border-emerald-800/35 rounded-lg">Highest</span>
              </div>
            </div>
          </div>

          {/* Performance Chart Card */}
          <div className="bg-[#0e1122]/60 border border-zinc-800/40 backdrop-blur-xl rounded-2xl p-6 shadow-[0_4px_30px_rgba(0,0,0,0.4)] space-y-6">
            <div>
              <h2 className="text-xl font-bold text-white tracking-wide">Progress Chart</h2>
              <p className="text-zinc-500 text-xs">Tracking score percentages chronologically across your attempts.</p>
            </div>
            <PerformanceChart attempts={attempts} />
          </div>

          {/* History log */}
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-white tracking-wide">Quiz Attempt History</h2>
            <div className="bg-[#0e1122]/60 border border-zinc-800/40 rounded-2xl overflow-hidden shadow-lg">
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-zinc-800/40 bg-zinc-950/50 text-zinc-400 text-xs uppercase tracking-wider">
                      <th className="px-6 py-4 font-medium">Date</th>
                      <th className="px-6 py-4 font-medium">Topic</th>
                      <th className="px-6 py-4 font-medium">Score</th>
                      <th className="px-6 py-4 font-medium">Percentage</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-zinc-800/20 text-zinc-300 text-sm">
                    {[...attempts].reverse().map((attempt) => {
                      const dateStr = new Date(attempt.timestamp).toLocaleDateString(undefined, {
                        year: "numeric",
                        month: "short",
                        day: "numeric",
                        hour: "2-digit",
                        minute: "2-digit"
                      });
                      return (
                        <tr key={attempt.id} className="hover:bg-zinc-900/10 transition duration-150">
                          <td className="px-6 py-4 font-medium text-zinc-500">{dateStr}</td>
                          <td className="px-6 py-4 font-bold text-white">{attempt.topic}</td>
                          <td className="px-6 py-4">{attempt.score} / {attempt.total}</td>
                          <td className="px-6 py-4">
                            <span className={`px-2 py-1 rounded-lg text-xs font-bold ${
                              attempt.percentage >= 80 
                                ? 'bg-green-500/10 text-green-400 border border-green-500/20' 
                                : attempt.percentage >= 60 
                                  ? 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20' 
                                  : 'bg-red-500/10 text-red-400 border border-red-500/20'
                            }`}>
                              {Math.round(attempt.percentage)}%
                            </span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
