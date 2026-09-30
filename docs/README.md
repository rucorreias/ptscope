# Documentação do PTScope

O PTScope está numa fase inicial. O backend FastAPI disponibiliza health check e consulta municipal através da GEO API PT. O frontend Next.js já contém navegação entre mapa e dashboards e um mapa base MapLibre. Ainda não estão integrados limites municipais oficiais nem a série de população do INE.

- [Plano de entregas e issues de v0.1](roadmap.md)
- [Estudos das fontes](data/sources/): contratos externos, exemplos, limitações e questões abertas
- [Modelo conceptual v0.1](architecture/domain-model.md): INE, GEO API PT, observações, geografia e proveniência (rascunho a validar)
- [Decisões de ingestão](architecture/data-ingestion.md): proveniência, valores, dimensões, versões territoriais e decisões pendentes

Os estudos das fontes distinguem o que foi documentado, observado e inferido. Uma decisão interna do PTScope pertence a `docs/architecture/`; uma descoberta sobre a fonte pertence a `docs/data/sources/`.

## Desenvolvimento

O backend fica em `backend/` e separa rotas HTTP, serviços de fonte e schemas Pydantic. A documentação OpenAPI está em `http://127.0.0.1:8000/docs` com o backend em execução. O frontend fica em `frontend/` e apresenta os estados de preparação onde ainda não existem dados integrados.

Para instalação e comandos de execução, consulta o [README principal](../README.md). As tarefas e critérios de conclusão estão nas [issues](https://github.com/rucorreias/ptscope/issues).
