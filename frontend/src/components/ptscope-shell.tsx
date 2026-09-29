import Link from "next/link";
import type { ReactNode } from "react";

import { BackendStatus } from "@/components/backend-status";

type View = "map" | "dashboards";

const navigation: Array<{ href: string; label: string; view: View }> = [
  { href: "/", label: "Map", view: "map" },
  { href: "/dashboards", label: "Dashboards", view: "dashboards" },
];

interface PTScopeShellProps {
  activeView: View;
  children: ReactNode;
}

export function PTScopeShell({ activeView, children }: PTScopeShellProps) {
  return (
    <main className="flex min-h-screen flex-col bg-[#f2f5f3] text-[#18332d]">
      <header className="border-b border-[#254a40] bg-[#173b32] text-white">
        <div className="flex min-h-16 flex-wrap items-center gap-x-5 gap-y-3 px-4 py-3 sm:px-6 lg:px-7">
          <Link href="/" className="shrink-0" aria-label="PTScope, ir para o mapa">
            <span className="block text-lg font-semibold leading-none">PTScope</span>
            <span className="mt-1 block text-[0.68rem] font-medium uppercase text-[#b9d3c9]">
              Portugal em contexto
            </span>
          </Link>

          <nav
            className="order-3 flex w-full items-center gap-1 sm:order-none sm:w-auto"
            aria-label="Navegação principal"
          >
            {navigation.map((item) => {
              const isActive = item.view === activeView;

              return (
                <Link
                  key={item.view}
                  href={item.href}
                  aria-current={isActive ? "page" : undefined}
                  className={`flex-1 border-b-2 px-4 py-2 text-center text-sm font-medium transition-colors sm:flex-none ${
                    isActive
                      ? "border-[#8fd1b5] text-white"
                      : "border-transparent text-[#c7d9d2] hover:border-[#688f80] hover:text-white"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>

          <div className="ml-auto">
            <BackendStatus />
          </div>
        </div>
      </header>

      <div className="flex flex-1 flex-col md:min-h-0 md:flex-row">
        <aside className="border-b border-[#d4dedb] bg-[#e8eeeb] px-4 py-4 md:w-56 md:shrink-0 md:border-r md:border-b-0 lg:w-60 lg:px-5">
          {activeView === "map" ? <MapSidebar /> : <DashboardsSidebar />}
        </aside>

        <div className="flex min-w-0 flex-1 flex-col">{children}</div>
      </div>
    </main>
  );
}

function MapSidebar() {
  return (
    <div className="grid gap-4 sm:grid-cols-2 md:block">
      <div>
        <p className="text-xs font-semibold uppercase text-[#527166]">Camadas</p>
        <div className="mt-3 flex items-start gap-3">
          <span
            className="mt-1 h-3 w-3 shrink-0 border border-[#92aaa2] bg-[#dfe8e4]"
            aria-hidden="true"
          />
          <div>
            <p className="text-sm font-medium text-[#18332d]">Mapa base</p>
            <p className="mt-0.5 text-xs leading-5 text-[#64756f]">
              OpenFreeMap · OpenStreetMap
            </p>
          </div>
        </div>
      </div>

      <div className="border-t border-[#cbd8d3] pt-4 sm:border-t-0 sm:border-l sm:pt-0 sm:pl-4 md:mt-5 md:border-t md:border-l-0 md:pt-5 md:pl-0">
        <p className="text-xs font-semibold uppercase text-[#527166]">Território</p>
        <p className="mt-2 text-sm font-medium text-[#3d554e]">Camada por integrar</p>
        <p className="mt-1 text-xs leading-5 text-[#64756f]">
          Aguarda geometria oficial validada e versionada.
        </p>
      </div>
    </div>
  );
}

function DashboardsSidebar() {
  return (
    <div>
      <label
        htmlFor="theme"
        className="text-xs font-semibold uppercase text-[#527166]"
      >
        Tema
      </label>
      <select
        id="theme"
        name="theme"
        defaultValue="demography"
        className="mt-2 w-full border border-[#b9cac4] bg-white px-3 py-2.5 text-sm font-medium text-[#18332d] outline-none focus:border-[#2c6255] focus:ring-2 focus:ring-[#2c6255]/20"
      >
        <option value="demography">Demography</option>
      </select>
      <div className="mt-4 border-t border-[#cbd8d3] pt-4">
        <p className="text-xs font-semibold uppercase text-[#527166]">Estado</p>
        <p className="mt-2 text-sm font-medium text-[#3d554e]">Planeado</p>
        <p className="mt-1 text-xs leading-5 text-[#64756f]">
          Sem indicadores demográficos integrados nesta fase.
        </p>
      </div>
    </div>
  );
}
