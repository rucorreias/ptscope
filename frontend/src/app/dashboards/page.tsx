import { PTScopeShell } from "@/components/ptscope-shell";

export default function DashboardsPage() {
  return (
    <PTScopeShell activeView="dashboards">
      <section className="flex min-h-0 flex-1 flex-col" aria-labelledby="dashboards-title">
        <header className="border-b border-[#dbe3e0] bg-white px-5 py-4 lg:px-7">
          <p className="text-xs font-semibold uppercase text-[#527166]">
            Análise temática
          </p>
          <h1
            id="dashboards-title"
            className="mt-1 text-2xl font-semibold text-[#18332d]"
          >
            Dashboards
          </h1>
        </header>

        <div className="flex flex-1 items-center justify-center px-5 py-12">
          <div className="max-w-lg text-center">
            <span className="mx-auto flex h-12 w-12 items-center justify-center rounded-full border border-[#cbd8d3] bg-white text-lg font-semibold text-[#2c6255]">
              D
            </span>
            <h2 className="mt-5 text-xl font-semibold text-[#18332d]">
              Demography está em preparação
            </h2>
            <p className="mt-3 text-sm leading-6 text-[#5c6f69]">
              Os indicadores do INE ainda não foram integrados nem associados a
              uma versão geográfica validada. Esta área ficará vazia até existirem
              valores, períodos, unidades e proveniência verificáveis.
            </p>
          </div>
        </div>
      </section>
    </PTScopeShell>
  );
}
