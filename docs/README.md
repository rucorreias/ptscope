# PTScope Wiki

## Visão geral

PTScope é uma plataforma pública de inteligência territorial para Portugal.
Esta base documenta o backend inicial: uma API FastAPI mínima, sem base de
dados, autenticação ou frontend.

## Backend

O backend vive em `backend/` e separa responsabilidades de forma simples:

- `routes`: endpoints HTTP.
- `services`: integrações externas, incluindo a GEO API PT.
- `schemas`: modelos de dados Pydantic.

## API

Quando o backend estiver a correr, a documentação Swagger fica disponível em:

- `http://127.0.0.1:8000/docs`

Endpoints iniciais:

- `GET /`
- `GET /api/v1/health`
- `GET /api/v1/municipios/{nome}`

## Integrações

A integração com a GEO API PT está implementada em
`backend/app/services/geoapi.py` e fornece dados municipais normalizados.
