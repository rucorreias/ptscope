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
    <div className="flex min-w-48 items-center gap-3 rounded-lg border border-[#d9e2ec] bg-white px-4 py-3 shadow-sm">
      <span
        className={`h-2.5 w-2.5 rounded-full ${
          isOnline
            ? "bg-[#2f855a]"
            : health.status === "loading"
              ? "bg-[#d69e2e]"
              : "bg-[#c53030]"
        }`}
        aria-hidden="true"
      />
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.12em] text-[#52667a]">
          API
        </p>
        <p className="text-sm font-medium text-[#14213d]">{detail}</p>
      </div>
    </div>
  );
}
