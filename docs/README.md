# PTScope Wiki

## Visão geral

PTScope é uma plataforma pública de inteligência territorial para Portugal.
Esta base documenta a Fase 0 do backend: uma API FastAPI mínima, sem base de
dados, autenticação, frontend ou integrações externas.

## Backend

O backend vive em `backend/` e separa responsabilidades de forma simples:

- `routes`: endpoints HTTP.
- `services`: integrações externas futuras.
- `schemas`: modelos de dados Pydantic.

## API

Quando o backend estiver a correr, a documentação Swagger fica disponível em:

- `http://127.0.0.1:8000/docs`

Endpoints iniciais:

- `GET /`
- `GET /api/v1/health`
- `GET /api/v1/municipios/{nome}`

## Próximos passos

A integração com GEO API PT deve ser implementada numa fase posterior em
`backend/app/services/geoapi.py`.
