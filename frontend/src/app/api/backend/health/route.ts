import { NextResponse } from "next/server";

const DEFAULT_BACKEND_URL = "http://127.0.0.1:8000";

function getBackendBaseUrl() {
  return (process.env.BACKEND_INTERNAL_URL ?? DEFAULT_BACKEND_URL).replace(
    /\/$/,
    "",
  );
}

export async function GET() {
  try {
    const response = await fetch(`${getBackendBaseUrl()}/api/v1/health`, {
      cache: "no-store",
      signal: AbortSignal.timeout(2500),
    });
    const data = await response.json();

    return NextResponse.json({ ok: response.ok, data }, { status: response.status });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Backend unavailable";

    return NextResponse.json(
      { ok: false, error: message },
      { status: 503 },
    );
  }
}
