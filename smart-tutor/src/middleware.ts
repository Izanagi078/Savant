import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("access_token")?.value;
  const { pathname } = request.nextUrl;

  // Paths requiring authentication
  const protectedPaths = ["/", "/quiz", "/performance", "/profile"];

  // If path is protected and token is missing, redirect to /auth
  if (protectedPaths.includes(pathname) && !token) {
    return NextResponse.redirect(new URL("/auth", request.url));
  }

  // If user is authenticated and attempts to access /auth, redirect to workspace home page
  if (pathname === "/auth" && token) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/",
    "/auth",
    "/quiz",
    "/performance",
    "/profile"
  ]
};
