import { PTScopeShell } from "@/components/ptscope-shell";
import { TerritoryMap } from "@/components/territory-map";

export default function MapPage() {
  return (
    <PTScopeShell activeView="map">
      <section className="flex min-h-0 flex-1 flex-col" aria-labelledby="map-title">
        <header className="flex flex-col gap-3 border-b border-[#dbe3e0] bg-white px-5 py-4 sm:flex-row sm:items-end sm:justify-between lg:px-7">
          <div>
            <p className="text-xs font-semibold uppercase text-[#527166]">
              Exploração territorial
            </p>
            <h1 id="map-title" className="mt-1 text-2xl font-semibold text-[#18332d]">
              Mapa de Portugal
            </h1>
          </div>
          <p className="max-w-xl text-sm leading-5 text-[#5c6f69]">
            Base cartográfica de contexto, sem limites administrativos ou
            indicadores associados.
          </p>
        </header>

        <div className="min-h-[34rem] flex-1 p-3 sm:p-5 lg:p-6">
          <TerritoryMap />
        </div>
      </section>
    </PTScopeShell>
  );
}
