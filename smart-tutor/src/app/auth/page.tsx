"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function AuthPage() {
  const router = useRouter();
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");

  // Clear states on tab switch
  useEffect(() => {
    setError("");
    setSuccess("");
  }, [isLogin]);

  // Client-side email validation helper
  const isValidEmail = (emailStr: string) => {
    const pattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
    return pattern.test(emailStr);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    const emailTrim = email.trim();
    if (!emailTrim || !password) {
      setError("Please fill in all required fields.");
      return;
    }

    if (!isValidEmail(emailTrim)) {
      setError("Please enter a valid email address.");
      return;
    }

    if (!isLogin && !fullName.trim()) {
      setError("Please enter your display name.");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters long.");
      return;
    }

    setLoading(true);

    try {
      if (isLogin) {
        const res = await fetch(`${API_BASE_URL}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: emailTrim, password }),
        });

        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.detail || "Authentication failed. Check your credentials.");
        }

        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("user", JSON.stringify(data.user));

        router.push("/");
      } else {
        const res = await fetch(`${API_BASE_URL}/auth/signup`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({
            email: emailTrim,
            password,
            full_name: fullName.trim(),
          }),
        });

        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.detail || "Registration failed. Ensure password meets strength criteria.");
        }

        setSuccess("Account created successfully! Switching to Login...");
        setTimeout(() => {
          setIsLogin(true);
          setPassword("");
        }, 1500);
      }
    } catch (err: any) {
      setError(err.message || "An unexpected network connection issue occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen w-screen grid grid-cols-1 lg:grid-cols-12 bg-[#070913] relative overflow-hidden select-none font-sans">
      {/* LEFT COLUMN: Problem-Solution Onboarding Info (7 columns, overflow-hidden to prevent scrollbar) */}
      <div className="hidden lg:flex lg:col-span-7 xl:col-span-7 flex-col justify-between p-8 relative border-r border-zinc-800/30 bg-gradient-to-br from-[#090b16] via-[#070913] to-[#04060c] overflow-hidden h-full">
        {/* Glow Effects */}
        <div className="absolute top-1/4 left-1/3 w-[500px] h-[500px] bg-cyan-500/5 rounded-full blur-[120px] -z-10"></div>
        <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-indigo-500/5 rounded-full blur-[100px] -z-10"></div>

        {/* Brand Header */}
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl shadow-lg shadow-cyan-500/10">
            <svg className="w-5 h-5 text-[#070913]" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2.5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 21l8.904-4.473L21 9l-3.187-3.187L9.813 15.904z" />
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m12.728 12.728l-.707.707" />
            </svg>
          </div>
          <span className="font-extrabold tracking-wider text-xl text-zinc-100 bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
            Savant
          </span>
        </div>

        {/* Concise introduction text */}
        <div className="my-2 space-y-2 max-w-xl">
          <h1 className="text-3xl xl:text-4xl font-black tracking-tight leading-tight text-zinc-100">
            Own Your Learning. <br/>
            <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">
              Savant Does the Rest.
            </span>
          </h1>
          <p className="text-zinc-400 text-xs leading-relaxed max-w-lg">
            Savant structures any learning objective into a guided pathway with verified materials and expert AI tutor support.
          </p>
        </div>

        {/* Clean, Concise Problem/Solution Cards (Fits low-height viewports) */}
        <div className="space-y-3 mt-auto">
          {/* Card 1 */}
          <div className="p-3.5 bg-[#0e1122]/50 border border-zinc-800/50 rounded-xl space-y-1.5 backdrop-blur-md">
            <div className="flex items-center gap-2">
              <span className="px-1.5 py-0.5 text-[8px] font-black bg-red-500/10 text-red-400 border border-red-500/20 rounded tracking-wider uppercase">Problem</span>
              <span className="text-xs font-bold text-zinc-200">Stuck on complex topics?</span>
            </div>
            <div className="flex items-center gap-2 pt-1 border-t border-zinc-800/10">
              <span className="px-1.5 py-0.5 text-[8px] font-black bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 rounded tracking-wider uppercase">Solve</span>
              <p className="text-zinc-400 text-xs">Savant generates custom paths with vetted guides and videos.</p>
            </div>
          </div>

          {/* Card 2 */}
          <div className="p-3.5 bg-[#0e1122]/50 border border-zinc-800/50 rounded-xl space-y-1.5 backdrop-blur-md">
            <div className="flex items-center gap-2">
              <span className="px-1.5 py-0.5 text-[8px] font-black bg-red-500/10 text-red-400 border border-red-500/20 rounded tracking-wider uppercase">Problem</span>
              <span className="text-xs font-bold text-zinc-200">Confused by formulas or code?</span>
            </div>
            <div className="flex items-center gap-2 pt-1 border-t border-zinc-800/10">
              <span className="px-1.5 py-0.5 text-[8px] font-black bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 rounded tracking-wider uppercase">Solve</span>
              <p className="text-zinc-400 text-xs">Your personal AI tutor clarifies queries and concepts step-by-step.</p>
            </div>
          </div>

          {/* Card 3 */}
          <div className="p-3.5 bg-[#0e1122]/50 border border-zinc-800/50 rounded-xl space-y-1.5 backdrop-blur-md">
            <div className="flex items-center gap-2">
              <span className="px-1.5 py-0.5 text-[8px] font-black bg-red-500/10 text-red-400 border border-red-500/20 rounded tracking-wider uppercase">Problem</span>
              <span className="text-xs font-bold text-zinc-200">Tutorials don't guarantee retention?</span>
            </div>
            <div className="flex items-center gap-2 pt-1 border-t border-zinc-800/10">
              <span className="px-1.5 py-0.5 text-[8px] font-black bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 rounded tracking-wider uppercase">Solve</span>
              <p className="text-zinc-400 text-xs">Practice with quizzes providing full mathematical explanations.</p>
            </div>
          </div>
        </div>
      </div>

      {/* RIGHT COLUMN: Centered, Compact Authentication Portal (5 columns, overflow-hidden to prevent scrollbar) */}
      <div className="lg:col-span-5 xl:col-span-5 flex items-center justify-center p-6 bg-[#090b16]/40 backdrop-blur-md relative overflow-hidden h-full">
        {/* Glow behind the auth card */}
        <div className="absolute w-[350px] h-[350px] bg-cyan-500/10 rounded-full blur-[90px] -z-10"></div>

        {/* Compact Authentication Card */}
        <div className="w-full max-w-md space-y-4 bg-[#0e1122]/60 border border-zinc-800/50 backdrop-blur-xl p-6 rounded-2xl shadow-[0_8px_32px_rgba(0,0,0,0.6)]">
          {/* Header */}
          <div className="space-y-1">
            <h2 className="text-2xl font-black tracking-tight bg-gradient-to-r from-cyan-400 to-indigo-400 bg-clip-text text-transparent">
              {isLogin ? "Welcome Back" : "Create Account"}
            </h2>
            <p className="text-zinc-400 text-[11px] tracking-wider uppercase font-semibold">
              {isLogin ? "Sign in to access your study pathways" : "Sign up to create your personalized courses"}
            </p>
          </div>

          {/* Form Tabs */}
          <div className="flex bg-zinc-950/60 p-1 rounded-xl border border-zinc-800/60">
            <button
              onClick={() => setIsLogin(true)}
              className={`flex-1 py-2 text-xs font-bold rounded-lg transition duration-200 cursor-pointer ${
                isLogin
                  ? "bg-gradient-to-r from-cyan-500/10 to-blue-600/10 border border-cyan-500/20 text-cyan-300 shadow-sm"
                  : "text-zinc-500 hover:text-zinc-300"
              }`}
            >
              Sign In
            </button>
            <button
              onClick={() => setIsLogin(false)}
              className={`flex-1 py-2 text-xs font-bold rounded-lg transition duration-200 cursor-pointer ${
                !isLogin
                  ? "bg-gradient-to-r from-cyan-500/10 to-blue-600/10 border border-cyan-500/20 text-cyan-300 shadow-sm"
                  : "text-zinc-500 hover:text-zinc-300"
              }`}
            >
              Register
            </button>
          </div>

          {/* Error / Success Alerts */}
          {error && (
            <div className="p-2.5 bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-semibold rounded-xl text-center">
              {error}
            </div>
          )}
          {success && (
            <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold rounded-xl text-center">
              {success}
            </div>
          )}

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="space-y-3">
            {!isLogin && (
              <div className="space-y-1">
                <label className="block text-[10px] font-extrabold uppercase tracking-widest text-cyan-400/80">
                  Full Name
                </label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="John Doe"
                  className="w-full px-3 py-2.5 bg-zinc-950/60 border border-zinc-800/80 focus:border-cyan-500/50 rounded-xl outline-none text-zinc-100 placeholder-zinc-650 focus:ring-2 focus:ring-cyan-500/5 transition text-xs"
                />
              </div>
            )}

            <div className="space-y-1">
              <label className="block text-[10px] font-extrabold uppercase tracking-widest text-cyan-400/80">
                Email Address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@domain.com"
                required
                className="w-full px-3 py-2.5 bg-zinc-950/60 border border-zinc-800/80 focus:border-cyan-500/50 rounded-xl outline-none text-zinc-100 placeholder-zinc-650 focus:ring-2 focus:ring-cyan-500/5 transition text-xs"
              />
            </div>

            <div className="space-y-1">
              <label className="block text-[10px] font-extrabold uppercase tracking-widest text-cyan-400/80">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full px-3 py-2.5 bg-zinc-950/60 border border-zinc-800/80 focus:border-cyan-500/50 rounded-xl outline-none text-zinc-100 placeholder-zinc-650 focus:ring-2 focus:ring-cyan-500/5 transition text-xs"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 mt-4 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold rounded-xl transition duration-200 shadow-[0_0_15px_rgba(6,182,212,0.1)] disabled:opacity-50 disabled:shadow-none cursor-pointer text-xs"
            >
              {loading ? "Authorizing..." : isLogin ? "Sign In" : "Register"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
