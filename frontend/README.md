# PTScope Frontend

Frontend em Next.js para o PTScope.

## Stack

- Next.js 16 com App Router
- React 19
- TypeScript
- Tailwind CSS 4
- ESLint 9
- Docker com output `standalone`

## Desenvolvimento local

```bash
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000).

O frontend consulta o backend atraves de `/api/backend/health`, que por defeito
encaminha para `http://127.0.0.1:8000`. Para alterar:

```bash
cp .env.example .env.local
```

Depois ajusta `BACKEND_INTERNAL_URL`.

## Docker

A partir da raiz do repositorio:

```bash
docker compose up --build
```

Para construir apenas a imagem de producao do frontend:

```bash
docker build -t ptscope-frontend ./frontend
```

## Validacao

```bash
npm run lint
npm run build
```

`npm run build` usa `next build --webpack` porque o build Turbopack de Next
16.3.7 panica neste ambiente ao processar CSS. O script `npm run build:turbo`
fica disponivel para revalidar Turbopack quando a versao do Next for atualizada.
