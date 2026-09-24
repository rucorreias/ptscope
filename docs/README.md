# PTScope Wiki

## Visao geral

PTScope e uma plataforma publica de inteligencia territorial para Portugal.
Esta base documenta a Fase 0 do backend: uma API FastAPI minima, sem base de
dados, autenticacao, frontend ou integracoes externas.

## Backend

O backend vive em `backend/` e separa responsabilidades de forma simples:

- `routes`: endpoints HTTP.
- `services`: integracoes externas futuras.
- `schemas`: modelos de dados Pydantic.

## API

Quando o backend estiver a correr, a documentacao Swagger fica disponivel em:

- `http://127.0.0.1:8000/docs`

Endpoints iniciais:

- `GET /`
- `GET /api/v1/health`
- `GET /api/v1/municipios/{nome}`

## Proximos passos

A integracao com GEO API PT deve ser implementada numa fase posterior em
`backend/app/services/geoapi.py`.
