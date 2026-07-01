"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { getApiBaseUrl } from "@/utils/api";

export default function ProfilePage() {
  const router = useRouter();
  const API_BASE_URL = getApiBaseUrl();

  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  
  const [fetching, setFetching] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Fetch current user profile
  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const res = await fetch(`${API_BASE_URL}/auth/me`, {
          headers: { "Authorization": `Bearer ${token}` }
        });

        if (!res.ok) {
          throw new Error("Failed to fetch user session. Please log in again.");
        }

        const data = await res.json();
        setEmail(data.email);
        setFullName(data.full_name || "");
      } catch (err: any) {
        localStorage.removeItem("user");
        router.push("/auth");
      } finally {
        setFetching(false);
      }
    };

    fetchUserProfile();
  }, [router, API_BASE_URL]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (password && password.length < 8) {
      setError("Password must be at least 8 characters long.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setSubmitting(true);

    try {
      const payload: { full_name?: string; password?: string } = {};

      if (fullName.trim()) {
        payload.full_name = fullName.trim();
      }
      if (password) {
        payload.password = password;
      }

      const token = localStorage.getItem("access_token");
      const res = await fetch(`${API_BASE_URL}/auth/update`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Failed to update profile details.");
      }

      // Update stored user details
      localStorage.setItem("user", JSON.stringify({
        id: data.id,
        email: data.email,
        full_name: data.full_name
      }));

      setSuccess("Profile details updated successfully!");
      setPassword("");
      setConfirmPassword("");
    } catch (err: any) {
      setError(err.message || "An error occurred while updating profile.");
    } finally {
      setSubmitting(false);
    }
  };

  if (fetching) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <div className="w-10 h-10 border-4 border-cyan-500/20 border-t-cyan-400 rounded-full animate-spin"></div>
        <p className="text-zinc-400 text-xs font-semibold uppercase tracking-wider">Loading Profile...</p>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto space-y-8">
      {/* Page Header */}
      <div className="space-y-2">
        <h1 className="text-4xl font-black tracking-tight bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">
          Profile Settings
        </h1>
        <p className="text-zinc-400 text-sm leading-relaxed">
          Update your personalized profile name and password credentials below.
        </p>
      </div>

      {/* Main Settings Card */}
      <div className="bg-[#0e1122]/60 border border-zinc-800/40 backdrop-blur-xl rounded-2xl p-8 shadow-[0_4px_30px_rgba(0,0,0,0.4)] relative overflow-hidden">
        {/* Decorative corner glow */}
        <div className="absolute top-0 right-0 w-[150px] h-[150px] bg-cyan-500/5 rounded-full blur-[40px] pointer-events-none"></div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Email (Read Only) */}
          <div className="space-y-2">
            <label className="block text-2xs font-extrabold uppercase tracking-widest text-cyan-400/80">
              Email Address
            </label>
            <input
              type="email"
              value={email}
              disabled
              className="w-full px-4 py-3.5 bg-zinc-950/40 border border-zinc-800/50 rounded-xl text-zinc-500 cursor-not-allowed text-sm"
            />
            <p className="text-zinc-500 text-[10px]">Your email address is linked to your user identity and cannot be modified.</p>
          </div>

          {/* Full Name */}
          <div className="space-y-2">
            <label className="block text-2xs font-extrabold uppercase tracking-widest text-cyan-400/80">
              Display Name
            </label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Your Full Name"
              required
              className="w-full px-4 py-3.5 bg-zinc-950/60 border border-zinc-800/80 focus:border-cyan-500/50 rounded-xl outline-none text-zinc-100 placeholder-zinc-650 focus:ring-2 focus:ring-cyan-500/10 transition text-sm"
            />
          </div>

          <div className="border-t border-zinc-800/40 my-6"></div>

          {/* Password Header */}
          <div className="space-y-1">
            <h3 className="text-xs font-extrabold uppercase tracking-wider text-zinc-300">Change Password</h3>
            <p className="text-zinc-500 text-[10px]">Leave these fields blank if you do not wish to update your current password.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* New Password */}
            <div className="space-y-2">
              <label className="block text-2xs font-extrabold uppercase tracking-widest text-cyan-400/80">
                New Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3.5 bg-zinc-950/60 border border-zinc-800/80 focus:border-cyan-500/50 rounded-xl outline-none text-zinc-100 placeholder-zinc-650 focus:ring-2 focus:ring-cyan-500/10 transition text-sm"
              />
            </div>

            {/* Confirm Password */}
            <div className="space-y-2">
              <label className="block text-2xs font-extrabold uppercase tracking-widest text-cyan-400/80">
                Confirm Password
              </label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3.5 bg-zinc-950/60 border border-zinc-800/80 focus:border-cyan-500/50 rounded-xl outline-none text-zinc-100 placeholder-zinc-650 focus:ring-2 focus:ring-cyan-500/10 transition text-sm"
              />
            </div>
          </div>

          {/* Error / Success Alerts */}
          {error && (
            <div className="p-3.5 bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-semibold rounded-xl text-center">
              {error}
            </div>
          )}
          {success && (
            <div className="p-3.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold rounded-xl text-center">
              {success}
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-4 items-center justify-end pt-4">
            <button
              type="button"
              onClick={() => router.push("/")}
              className="px-6 py-3.5 border border-zinc-800/60 hover:bg-zinc-800/20 text-zinc-300 hover:text-zinc-100 font-bold rounded-xl transition duration-200 text-sm cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="px-8 py-3.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold rounded-xl transition duration-200 shadow-[0_0_15px_rgba(6,182,212,0.15)] hover:shadow-[0_0_25px_rgba(6,182,212,0.3)] disabled:opacity-50 disabled:shadow-none text-sm cursor-pointer"
            >
              {submitting ? "Updating..." : "Save Changes"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
