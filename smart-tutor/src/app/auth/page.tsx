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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !password) {
      setError("Please fill in all required fields.");
      return;
    }

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      if (isLogin) {
        // Sign In
        const res = await fetch(`${API_BASE_URL}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: email.trim(), password }),
        });

        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.detail || "Authentication failed. Double check your password.");
        }

        // Save token and user details in localStorage
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("user", JSON.stringify(data.user));

        // Redirect to workspace
        router.push("/");
      } else {
        // Sign Up
        const res = await fetch(`${API_BASE_URL}/auth/signup`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: email.trim(),
            password,
            full_name: fullName.trim() || null,
          }),
        });

        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.detail || "Registration failed. Email might already exist.");
        }

        setSuccess("Account created successfully! Switching to Login...");
        setTimeout(() => {
          setIsLogin(true);
          setPassword("");
        }, 1500);
      }
    } catch (err: any) {
      setError(err.message || "Something went wrong. Please check your network connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-[#0a0c16]">
      {/* Background Decorative Blobs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl -z-10 animate-pulse"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl -z-10 animate-pulse delay-1000"></div>

      <div className="w-full max-w-md bg-[#0e1122]/60 border border-zinc-800/40 backdrop-blur-xl rounded-2xl p-8 shadow-[0_8px_32px_rgba(0,0,0,0.5)] space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-black tracking-tight bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">
            SmartTutor
          </h1>
          <p className="text-zinc-400 text-xs tracking-wide">
            {isLogin
              ? "Access your learning pathway and expert assistant"
              : "Create an account to start building custom courses"}
          </p>
        </div>

        {/* Tab Selector */}
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
            Create Account
          </button>
        </div>

        {/* Status Alerts */}
        {error && (
          <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-semibold rounded-xl text-center">
            {error}
          </div>
        )}
        {success && (
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold rounded-xl text-center">
            {success}
          </div>
        )}

        {/* Auth Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {!isLogin && (
            <div className="space-y-1.5">
              <label className="block text-4xs font-extrabold uppercase tracking-widest text-cyan-400/80">
                Full Name
              </label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="John Doe"
                className="w-full px-4 py-3 bg-zinc-950/60 border border-zinc-800 focus:border-cyan-500/50 rounded-xl outline-none text-zinc-100 placeholder-zinc-600 focus:ring-2 focus:ring-cyan-500/10 transition text-xs"
              />
            </div>
          )}

          <div className="space-y-1.5">
            <label className="block text-4xs font-extrabold uppercase tracking-widest text-cyan-400/80">
              Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@example.com"
              required
              className="w-full px-4 py-3 bg-zinc-950/60 border border-zinc-800 focus:border-cyan-500/50 rounded-xl outline-none text-zinc-100 placeholder-zinc-600 focus:ring-2 focus:ring-cyan-500/10 transition text-xs"
            />
          </div>

          <div className="space-y-1.5">
            <label className="block text-4xs font-extrabold uppercase tracking-widest text-cyan-400/80">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              className="w-full px-4 py-3 bg-zinc-950/60 border border-zinc-800 focus:border-cyan-500/50 rounded-xl outline-none text-zinc-100 placeholder-zinc-600 focus:ring-2 focus:ring-cyan-500/10 transition text-xs"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 mt-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold rounded-xl transition duration-200 shadow-[0_0_15px_rgba(6,182,212,0.15)] hover:shadow-[0_0_25px_rgba(6,182,212,0.3)] disabled:opacity-50 disabled:shadow-none cursor-pointer text-xs"
          >
            {loading
              ? "Signing in..."
              : isLogin
              ? "Sign In to Pathway"
              : "Register Account"}
          </button>
        </form>
      </div>
    </div>
  );
}
