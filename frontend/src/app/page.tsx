import { BackendStatus } from "@/components/backend-status";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#f7f8fb] text-[#14213d]">
      <section className="mx-auto flex w-full max-w-6xl flex-col gap-10 px-6 py-10 sm:px-8 lg:px-10">
        <header className="flex flex-col gap-4 border-b border-[#d9e2ec] pb-8 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.16em] text-[#4f6f52]">
              PTScope
            </p>
            <h1 className="mt-3 text-4xl font-semibold leading-tight text-[#14213d] sm:text-5xl">
              Inteligencia territorial para Portugal
            </h1>
          </div>
          <BackendStatus />
        </header>

        <div className="grid gap-5 md:grid-cols-3">
          <section className="rounded-lg border border-[#d9e2ec] bg-white p-5 shadow-sm">
            <h2 className="text-sm font-semibold uppercase tracking-[0.12em] text-[#4f6f52]">
              Backend
            </h2>
            <p className="mt-3 text-2xl font-semibold">FastAPI</p>
            <p className="mt-2 text-sm leading-6 text-[#52667a]">
              API territorial disponivel em Docker na porta 8000.
            </p>
          </section>

          <section className="rounded-lg border border-[#d9e2ec] bg-white p-5 shadow-sm">
            <h2 className="text-sm font-semibold uppercase tracking-[0.12em] text-[#4f6f52]">
              Frontend
            </h2>
            <p className="mt-3 text-2xl font-semibold">Next.js</p>
            <p className="mt-2 text-sm leading-6 text-[#52667a]">
              App Router, TypeScript, Tailwind CSS e Turbopack.
            </p>
          </section>

          <section className="rounded-lg border border-[#d9e2ec] bg-white p-5 shadow-sm">
            <h2 className="text-sm font-semibold uppercase tracking-[0.12em] text-[#4f6f52]">
              Docker
            </h2>
            <p className="mt-3 text-2xl font-semibold">Compose</p>
            <p className="mt-2 text-sm leading-6 text-[#52667a]">
              Ambiente local com hot reload e imagem standalone para producao.
            </p>
          </section>
        </div>
      </section>
    </main>
  );
}
