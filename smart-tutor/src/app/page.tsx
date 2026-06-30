"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

interface Resource {
  source: string;
  title: string;
  description: string;
  url: string;
}

interface Module {
  title: string;
  description: string;
  key_concepts: string[];
  resources?: Resource[];
}

interface Syllabus {
  title: string;
  description: string;
  modules: Module[];
}

export default function WorkspacePage() {
  const router = useRouter();
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/auth");
    }
  }, [router]);

  const [topic, setTopic] = useState("");
  const [level, setLevel] = useState("beginner");
  const [loading, setLoading] = useState(false);
  const [statusText, setStatusText] = useState("");
  
  const [syllabus, setSyllabus] = useState<Syllabus | null>(null);
  const [activeModuleIndex, setActiveModuleIndex] = useState<number | null>(0);

  // Chat Tutor States
  const [chatInput, setChatInput] = useState("");
  const [chatHistory, setChatHistory] = useState<{ role: string; text: string }[]>([]);
  const [chatLoading, setChatLoading] = useState(false);
  const [currentRequestId, setCurrentRequestId] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setLoading(true);
    setSyllabus(null);
    setChatHistory([]);
    setCurrentRequestId("");
    
    setStatusText("Generating syllabus, fetching target materials, and running Verifier Agent...");

    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`${API_BASE_URL}/content/generate`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          user_id: "user_12345",
          topic: topic.trim(),
          level: level,
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to generate course.");
      }

      const data = await res.json();
      setSyllabus(data.syllabus);
      setCurrentRequestId(data.request_id);
      setLoading(false);

    } catch (error) {
      setLoading(false);
      setStatusText("Failed to initialize course builder. Ensure backend services are running.");
    }
  };

  const handleChatSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim() || !currentRequestId) return;

    const userMessage = chatInput.trim();
    setChatInput("");
    setChatHistory((prev) => [...prev, { role: "user", text: userMessage }]);
    setChatLoading(true);

    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`${API_BASE_URL}/tutor/chat`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          query: userMessage,
          request_id: currentRequestId,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setChatHistory((prev) => [...prev, { role: "tutor", text: data.response }]);
      } else {
        setChatHistory((prev) => [...prev, { role: "tutor", text: "Sorry, I ran into an issue connecting to the tutor brain." }]);
      }
    } catch (err) {
      setChatHistory((prev) => [...prev, { role: "tutor", text: "Failed to send message. Check your connection." }]);
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-10">
      {/* Workspace Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div className="space-y-3">
          <h1 className="text-5xl font-black tracking-tight bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">
            Course Builder
          </h1>
          <p className="text-zinc-400 max-w-2xl text-base leading-relaxed">
            Provide a learning goal. The orchestrator will build a custom syllabus, retrieve targeted learning materials, and activate your personal expert chat tutor.
          </p>
        </div>
        <div>
          <button
            onClick={() => {
              localStorage.removeItem("token");
              localStorage.removeItem("user");
              router.push("/auth");
            }}
            className="px-5 py-2.5 bg-zinc-950/60 border border-zinc-800 hover:border-red-500/30 hover:bg-red-500/5 text-zinc-300 hover:text-red-400 text-xs font-bold rounded-xl transition duration-200 cursor-pointer"
          >
            Sign Out
          </button>
        </div>
      </div>

      {/* Creation form (Glass card) */}
      <div className="bg-[#0e1122]/60 border border-zinc-800/40 backdrop-blur-xl rounded-2xl p-6 shadow-[0_4px_30px_rgba(0,0,0,0.4)]">
        <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-6">
          <div className="flex-1 space-y-2">
            <label className="block text-2xs font-extrabold uppercase tracking-widest text-cyan-400/80">
              Topic or Skill Prompt
            </label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g. Advanced Quantum Mechanics, Kubernetes Orchestrations, Rust Web Frameworks..."
              className="w-full px-4 py-3.5 bg-zinc-950/60 border border-zinc-800 focus:border-cyan-500/50 rounded-xl outline-none text-zinc-100 placeholder-zinc-500 focus:ring-2 focus:ring-cyan-500/10 transition duration-200 text-sm"
            />
          </div>

          <div className="w-full md:w-56 space-y-2">
            <label className="block text-2xs font-extrabold uppercase tracking-widest text-cyan-400/80">
              Target Level
            </label>
            <select
              value={level}
              onChange={(e) => setLevel(e.target.value)}
              className="w-full px-4 py-3.5 bg-zinc-950/60 border border-zinc-800 focus:border-cyan-500/50 rounded-xl outline-none text-zinc-100 focus:ring-2 focus:ring-cyan-500/10 transition duration-200 text-sm cursor-pointer"
            >
              <option value="beginner">Beginner Level</option>
              <option value="intermediate">Intermediate Level</option>
              <option value="advanced">Advanced Level</option>
            </select>
          </div>

          <div className="flex items-end justify-end">
            <button
              type="submit"
              disabled={loading || !topic.trim()}
              className="w-full md:w-auto px-8 py-3.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 disabled:from-zinc-800 disabled:to-zinc-800 text-white font-bold rounded-xl transition duration-200 shadow-[0_0_15px_rgba(6,182,212,0.2)] hover:shadow-[0_0_25px_rgba(6,182,212,0.4)] disabled:shadow-none cursor-pointer disabled:cursor-not-allowed text-sm"
            >
              {loading ? "Generating course..." : "Create Course"}
            </button>
          </div>
        </form>
      </div>

      {/* Loading Overlay State */}
      {loading && (
        <div className="flex flex-col items-center justify-center p-16 bg-[#0e1122]/40 border border-zinc-800/40 rounded-2xl shadow-xl space-y-6">
          <div className="relative w-16 h-16">
            <div className="absolute inset-0 border-4 border-cyan-500/20 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
          </div>
          <p className="text-zinc-300 font-semibold text-center text-sm animate-pulse tracking-wide">
            {statusText}
          </p>
        </div>
      )}

      {/* Results View */}
      {syllabus && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Course Syllabus Column */}
          <div className="lg:col-span-2 space-y-8">
            <div className="bg-gradient-to-br from-cyan-500/10 via-blue-500/5 to-transparent border border-cyan-500/20 rounded-2xl p-6 shadow-md space-y-4">
              <span className="inline-block px-3 py-1 bg-cyan-500/20 border border-cyan-400/30 text-cyan-300 text-2xs font-bold rounded-full uppercase tracking-wider">
                {level} Pathway
              </span>
              <h2 className="text-3xl font-extrabold text-white">{syllabus.title}</h2>
              <p className="text-zinc-400 leading-relaxed text-sm">{syllabus.description}</p>
            </div>

            {/* Modules List */}
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-zinc-100 tracking-wide">Syllabus Directory</h3>
              
              {syllabus.modules.map((mod, idx) => (
                <div
                  key={idx}
                  className="bg-[#0e1122]/40 border border-zinc-800/40 rounded-xl overflow-hidden shadow-sm"
                >
                  <button
                    onClick={() => setActiveModuleIndex(activeModuleIndex === idx ? null : idx)}
                    className="w-full flex items-center justify-between p-5 text-left font-bold text-zinc-200 hover:bg-zinc-800/20 transition cursor-pointer"
                  >
                    <span>{mod.title}</span>
                    <span className="text-cyan-400 font-bold">
                      {activeModuleIndex === idx ? "▼" : "▶"}
                    </span>
                  </button>

                  {activeModuleIndex === idx && (
                    <div className="p-6 border-t border-zinc-800/40 bg-zinc-950/20 space-y-6">
                      <p className="text-zinc-400 text-sm leading-relaxed">
                        {mod.description}
                      </p>
                      
                      {/* Key Concepts */}
                      <div className="space-y-3">
                        <span className="text-2xs font-extrabold uppercase tracking-widest text-cyan-400/80 block">
                          Key Concepts Covered
                        </span>
                        <div className="flex flex-wrap gap-2">
                          {mod.key_concepts.map((concept, cIdx) => (
                            <span
                              key={cIdx}
                              className="px-3 py-1.5 bg-[#141830] border border-cyan-500/10 text-cyan-300 text-xs font-semibold rounded-lg"
                            >
                              {concept}
                            </span>
                          ))}
                        </div>
                      </div>

                      {/* Verified Study Resources inside module */}
                      {mod.resources && mod.resources.length > 0 && (
                        <div className="space-y-4 pt-6 border-t border-zinc-800/40">
                          <span className="text-2xs font-extrabold uppercase tracking-widest text-emerald-400/80 block">
                            Verified Study Materials
                          </span>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {mod.resources.map((res, rIdx) => {
                              const isYoutube = res.source.toLowerCase() === "youtube";
                              const isArxiv = res.source.toLowerCase() === "arxiv";
                              return (
                                <a
                                  key={rIdx}
                                  href={res.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="block p-4 rounded-xl bg-zinc-900/60 border border-zinc-800 hover:border-emerald-500/30 hover:bg-emerald-500/5 transition duration-200 group"
                                >
                                  <div className="flex items-center justify-between mb-2">
                                    <span className={`px-2 py-0.5 rounded text-4xs font-extrabold uppercase tracking-wider ${
                                      isYoutube ? "bg-red-500/10 text-red-400 border border-red-500/20" :
                                      isArxiv ? "bg-blue-500/10 text-blue-400 border border-blue-500/20" :
                                      "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20"
                                    }`}>
                                      {res.source}
                                    </span>
                                    <span className="text-zinc-500 text-3xs font-medium group-hover:text-emerald-400 transition-colors">
                                      View ↗
                                    </span>
                                  </div>
                                  <h5 className="font-bold text-xs text-zinc-200 group-hover:text-emerald-400 transition-colors line-clamp-1">
                                    {res.title}
                                  </h5>
                                  <p className="text-2xs text-zinc-400 line-clamp-2 mt-1.5 leading-relaxed">
                                    {res.description}
                                  </p>
                                </a>
                              );
                            })}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Right Column - Chat Tutor */}
          <div className="space-y-8">
            <div className="bg-gradient-to-b from-[#13172e] to-[#0e1122] border border-cyan-500/20 rounded-2xl p-6 shadow-xl space-y-4">
              <h4 className="font-extrabold flex items-center gap-2 text-sm text-cyan-300 tracking-wider">
                🎓 SMARTTUTOR EXPERT ASSISTANT
              </h4>
              
              <div className="h-96 overflow-y-auto space-y-3 text-xs bg-black/40 rounded-xl p-4 border border-zinc-800/40 scrollbar-thin scrollbar-thumb-zinc-800">
                {chatHistory.length === 0 ? (
                  <div className="h-full flex items-center justify-center text-center p-4">
                    <p className="text-zinc-500 italic text-2xs leading-relaxed">
                      Ask a query regarding concepts in your syllabus modules or referenced study materials!
                    </p>
                  </div>
                ) : (
                  chatHistory.map((chat, idx) => (
                    <div
                      key={idx}
                      className={`p-3 rounded-xl leading-relaxed text-sm ${
                        chat.role === "user"
                          ? "bg-cyan-500/10 text-cyan-300 ml-6 border border-cyan-500/20"
                          : "bg-zinc-800/40 text-zinc-200 mr-6 border border-zinc-800/40"
                      }`}
                    >
                      <span className="font-extrabold uppercase tracking-widest text-3xs text-zinc-500 block mb-1">
                        {chat.role === "user" ? "Student" : "SmartTutor"}
                      </span>
                      {chat.text}
                    </div>
                  ))
                )}
                {chatLoading && (
                  <div className="flex items-center gap-2 text-2xs text-cyan-400 font-semibold animate-pulse p-2">
                    <div className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-bounce"></div>
                    Synthesizing reply...
                  </div>
                )}
              </div>

              <form onSubmit={handleChatSubmit} className="flex gap-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  placeholder="Ask a question about the syllabus..."
                  className="flex-1 bg-zinc-950/80 border border-zinc-800 rounded-xl px-3 py-2.5 text-xs outline-none focus:border-cyan-500/50 text-white placeholder-zinc-500"
                />
                <button
                  type="submit"
                  disabled={chatLoading || !chatInput.trim()}
                  className="px-4 py-2.5 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold rounded-xl transition duration-150 shadow-[0_0_10px_rgba(6,182,212,0.2)] hover:shadow-[0_0_15px_rgba(6,182,212,0.4)] disabled:opacity-50 cursor-pointer"
                >
                  Send
                </button>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
