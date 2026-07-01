export function getApiBaseUrl(): string {
  if (typeof window !== "undefined") {
    const hostname = window.location.hostname;
    // Local development fallback
    if (hostname === "localhost" || hostname === "127.0.0.1") {
      return "http://localhost:8000";
    }
  }
  // Production fallback to the Render backend URL
  return process.env.NEXT_PUBLIC_API_URL || "https://savant-oqtv.onrender.com";
}
