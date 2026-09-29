"use client";

import { useEffect, useState } from "react";

type BackendHealthState =
  | { status: "loading" }
  | { status: "online"; detail: string }
  | { status: "offline"; detail: string };

export function BackendStatus() {
  const [health, setHealth] = useState<BackendHealthState>({
    status: "loading",
  });

  useEffect(() => {
    let mounted = true;

    async function loadHealth() {
      try {
        const response = await fetch("/api/backend/health", {
          cache: "no-store",
        });
        const payload = await response.json();

        if (!mounted) {
          return;
        }

        if (!response.ok || !payload.ok) {
          setHealth({
            status: "offline",
            detail: payload.error ?? "API indisponivel",
          });
          return;
        }

        setHealth({
          status: "online",
          detail: payload.data?.status ?? "operacional",
        });
      } catch {
        if (mounted) {
          setHealth({ status: "offline", detail: "sem ligacao" });
        }
      }
    }

    loadHealth();

    return () => {
      mounted = false;
    };
  }, []);

  const isOnline = health.status === "online";
  const detail = health.status === "loading" ? "a verificar" : health.detail;

  return (
    <div className="flex min-w-36 items-center gap-2.5 border border-white/15 bg-white/[0.06] px-3 py-2">
      <span
        className={`h-2.5 w-2.5 shrink-0 rounded-full ${
          isOnline
            ? "bg-[#72d3a7]"
            : health.status === "loading"
              ? "bg-[#e2b75f]"
              : "bg-[#ef8f8f]"
        }`}
        aria-hidden="true"
      />
      <div>
        <p className="text-[0.65rem] font-semibold uppercase text-[#b9d3c9]">
          API
        </p>
        <p className="text-xs font-medium text-white">{detail}</p>
      </div>
    </div>
  );
}
