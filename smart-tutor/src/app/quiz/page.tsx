"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import QuizForm, { Question } from "@/components/QuizForm";

interface GradingResult {
  score: number;
  total: number;
  results: {
    question_id: number;
    user_answer: number;
    correct_answer: number;
    is_correct: boolean;
  }[];
}

export default function QuizPage() {
  const router = useRouter();
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/auth");
    }
  }, [router]);

  const [topic, setTopic] = useState("");
  const [level, setLevel] = useState("Beginner");
  const [loading, setLoading] = useState(false);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [correctAnswers, setCorrectAnswers] = useState<Record<number, number>>({});
  
  const [loadingGrading, setLoadingGrading] = useState(false);
  const [gradingResult, setGradingResult] = useState<GradingResult | null>(null);
  const [statusText, setStatusText] = useState("");

  const handleGenerateQuiz = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setLoading(true);
    setQuestions([]);
    setCorrectAnswers({});
    setGradingResult(null);
    setStatusText(`Invoking Quiz Verifier Agent for verified ${level} quiz...`);

    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`${API_BASE_URL}/quiz/generate`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          topic: topic.trim(),
          count: 10,
          level: level,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        
        const answersMap: Record<number, number> = {};
        const questionsList: Question[] = [];
        
        data.questions.forEach((q: any) => {
          questionsList.push({
            id: q.id,
            text: q.text,
            options: q.options,
            explanation: q.explanation,
          });
          answersMap[q.id] = q.answer;
        });

        setQuestions(questionsList);
        setCorrectAnswers(answersMap);
      } else {
        setStatusText("Failed to generate quiz. Verify backend server is alive.");
      }
    } catch (err) {
      setStatusText("Error contacting server. Please run the backend API.");
    } finally {
      setLoading(false);
    }
  };

  const handleQuizSubmit = async (answers: Record<number, number>) => {
    setLoadingGrading(true);
    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`${API_BASE_URL}/quiz/submit`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          topic: topic,
          answers: answers,
          correct_answers: correctAnswers,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setGradingResult(data);
      }
    } catch (err) {
      alert("Failed to submit answers.");
    } finally {
      setLoadingGrading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-10">
      {/* Header */}
      <div className="space-y-3">
        <h1 className="text-5xl font-black tracking-tight bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">
          Dynamic Quizzes
        </h1>
        <p className="text-zinc-400 max-w-2xl text-base leading-relaxed">
          Provide any subject, and the system will compile custom multiple-choice questions to test your depth of understanding.
        </p>
      </div>

      {/* Search/Generate bar */}
      <div className="bg-[#0e1122]/60 border border-zinc-800/40 backdrop-blur-xl rounded-2xl p-6 shadow-[0_4px_30px_rgba(0,0,0,0.4)]">
        <form onSubmit={handleGenerateQuiz} className="flex flex-col md:flex-row gap-4">
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g. Docker Volumes, Quantum Superposition, React Hooks life-cycle..."
            className="flex-1 px-4 py-3.5 bg-zinc-950/60 border border-zinc-800 focus:border-cyan-500/50 rounded-xl outline-none text-zinc-100 placeholder-zinc-500 focus:ring-2 focus:ring-cyan-500/10 transition duration-200 text-sm"
          />
          <select
            value={level}
            onChange={(e) => setLevel(e.target.value)}
            className="px-4 py-3.5 bg-zinc-950/60 border border-zinc-800 focus:border-cyan-500/50 rounded-xl outline-none text-zinc-300 focus:ring-2 focus:ring-cyan-500/10 transition duration-200 text-sm"
          >
            <option value="Beginner">Beginner</option>
            <option value="Intermediate">Intermediate</option>
            <option value="Advanced">Advanced</option>
          </select>
          <button
            type="submit"
            disabled={loading || !topic.trim()}
            className="px-8 py-3.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 disabled:from-zinc-800 disabled:to-zinc-800 text-white font-bold rounded-xl transition duration-200 shadow-[0_0_15px_rgba(6,182,212,0.2)] hover:shadow-[0_0_25px_rgba(6,182,212,0.4)] disabled:shadow-none cursor-pointer disabled:cursor-not-allowed text-sm"
          >
            {loading ? "Generating..." : "Generate Quiz"}
          </button>
        </form>
      </div>

      {/* Loading Status */}
      {loading && (
        <div className="flex flex-col items-center justify-center p-16 bg-[#0e1122]/40 border border-zinc-800/40 rounded-2xl shadow-xl space-y-6">
          <div className="relative w-16 h-16">
            <div className="absolute inset-0 border-4 border-cyan-500/20 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
          </div>
          <p className="text-zinc-300 font-semibold text-center text-sm animate-pulse tracking-wide">{statusText}</p>
        </div>
      )}

      {/* Quiz Display */}
      {questions.length > 0 && !gradingResult && (
        <div className="space-y-6">
          <h2 className="text-2xl font-extrabold text-white tracking-wide">Topic: {topic}</h2>
          <QuizForm
            questions={questions}
            onSubmit={handleQuizSubmit}
            loadingGrading={loadingGrading}
          />
        </div>
      )}

      {/* Grading results display */}
      {gradingResult && (
        <div className="space-y-8">
          <div className="bg-gradient-to-br from-green-500/10 via-emerald-500/5 to-transparent border border-green-500/25 rounded-2xl p-10 text-center space-y-4 shadow-md">
            <span className="text-5xl animate-bounce inline-block">🏆</span>
            <h2 className="text-3xl font-black text-white">Quiz Completed!</h2>
            <p className="text-3xl font-extrabold text-green-400">
              Score: {gradingResult.score} / {gradingResult.total} ({Math.round((gradingResult.score / gradingResult.total) * 100)}%)
            </p>
            <button
              onClick={() => {
                setQuestions([]);
                setGradingResult(null);
                setTopic("");
              }}
              className="mt-6 px-8 py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-450 hover:to-emerald-500 text-white font-bold rounded-xl transition duration-150 shadow-[0_0_15px_rgba(34,197,94,0.2)] hover:shadow-[0_0_25px_rgba(34,197,94,0.4)] cursor-pointer text-sm"
            >
              Take Another Quiz
            </button>
          </div>

          {/* Detailed results analysis */}
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-zinc-200 tracking-wide">Results Analysis</h3>
            {questions.map((q) => {
              const res = gradingResult.results.find((r) => String(r.question_id) === String(q.id));
              if (!res) return null;
              return (
                <div
                  key={q.id}
                  className={`p-6 rounded-xl border ${
                    res.is_correct
                      ? "border-green-500/20 bg-green-500/5"
                      : "border-red-500/20 bg-red-500/5"
                  } space-y-4 shadow-sm`}
                >
                  <p className="font-bold text-zinc-100 flex items-start gap-3">
                    <span className="text-lg shrink-0">{res.is_correct ? "✅" : "❌"}</span>
                    {q.text}
                  </p>
                  <div className="text-sm space-y-2 text-zinc-300 pl-8">
                    <p className="flex items-center gap-2">
                      <span>Your choice:</span>
                      <span className={res.is_correct ? "text-green-400 font-bold" : "text-red-400 font-bold"}>
                        {q.options[res.user_answer]}
                      </span>
                    </p>
                    {!res.is_correct && (
                      <p className="flex items-center gap-2 text-zinc-400">
                        <span>Correct answer:</span>
                        <span className="text-green-450 font-bold">{q.options[res.correct_answer]}</span>
                      </p>
                    )}
                    {q.explanation && (
                      <div className="mt-4 p-4 rounded-lg bg-zinc-950/40 border border-zinc-800/60 space-y-1">
                        <span className="text-xs font-semibold text-zinc-500 uppercase tracking-wider block text-cyan-400">Explanation:</span>
                        <p className="text-sm text-zinc-350 leading-relaxed whitespace-pre-line">{q.explanation}</p>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
