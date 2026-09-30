# Plano de entregas do PTScope

> Plano de trabalho, não declaração de funcionalidades já publicadas. Estado revisto em 29 de setembro de 2026, a partir do `main` em `f36aa842`. As [issues](https://github.com/rucorreias/ptscope/issues) registam as tarefas e critérios de conclusão.

## Estado atual

O backend FastAPI disponibiliza health check e consulta municipal pela GEO API PT. O frontend Next.js já tem navegação Mapa/Dashboards, barra lateral e um mapa base MapLibre; os limites administrativos e os indicadores demográficos ainda não estão ligados. Existem estudos de GEO API PT, INE, Portal BASE e DGT/SNIG/CAOP em [`docs/data/sources/`](data/sources/). As decisões de ingestão estão em [`docs/architecture/data-ingestion.md`](architecture/data-ingestion.md). O CI atual executa pytest e pylint no backend; a validação do frontend ainda é local.

## v0.1 — Evolução da população por município

**Pergunta do utilizador:** como evoluiu a população residente de um município em todos os períodos que conseguimos verificar e explicar?

Entregar a primeira experiência completa: selecionar município e período, consultar a série histórica verificada, ver geometria municipal recebida da GEO API PT quando as condições de utilização e o contexto estiverem confirmados; associar valores INE ao mapa apenas com correspondência territorial validada e consultar definição, unidade, dimensões, fonte, datas e limitações. Marcar a quebra metodológica de 2020–2021 na série [`0008273`](data/code-dictionary.md#ine-indicator-0008273); não calcular uma taxa transversal à quebra sem regra justificada. Investigar [`0012918`](data/code-dictionary.md#ine-indicator-0012918) como possível extensão recente, mantendo os indicadores separados até demonstrar comparabilidade. Um ano sem valor ou um município sem correspondência não recebe zero nem um polígono escolhido pelo nome.

O [modelo conceptual do domínio](architecture/domain-model.md) é uma entrega explícita de v0.1: descreve indicador, observação, dimensões, período, geografia versionada, correspondência territorial e proveniência. Pode ser esboçado em paralelo com a investigação (#1 e #2), mas os exemplos reais devem validá-lo antes de fechar o contrato da API (#3). Isto não define ainda tabelas, ORM nem uma base de dados.

| Ordem | Entrega verificável | Issue |
| --- | --- | --- |
| 1, em paralelo | Confirmar períodos, categorias, valores e eventuais revisões; estudar a extensão recente | [#1](https://github.com/rucorreias/ptscope/issues/1) |
| 1, em paralelo | Validar referências municipais INE ↔ GEO API PT, incluindo diferenças entre referenciais e casos sem correspondência | [#2](https://github.com/rucorreias/ptscope/issues/2) |
| 2 | Validar o modelo conceptual de domínio com exemplos reais; depois especificar dashboard e contrato da API | [#3](https://github.com/rucorreias/ptscope/issues/3) |
| 3, em paralelo | Implementar adapter INE e endpoint com testes offline | [#4](https://github.com/rucorreias/ptscope/issues/4) |
| 3, em paralelo | Apresentar geometria municipal da GEO API PT com origem e condições de uso identificadas | [#5](https://github.com/rucorreias/ptscope/issues/5) |
| 4 | Ligar o dashboard aos dados e ao mapa apenas para correspondências validadas | [#6](https://github.com/rucorreias/ptscope/issues/6) |
| Ao longo da entrega | Adicionar validação frontend ao CI e fechar a lista de evidências da versão | [#7](https://github.com/rucorreias/ptscope/issues/7) |

**Critério para publicar v0.1:** uma pessoa consegue seguir a evolução municipal verificada, compreender os períodos ausentes e a quebra metodológica, identificar a edição geográfica e rastrear o valor até à fonte. Os testes e lint do backend e o lint/build do frontend passam no CI. A licença, a atribuição, a edição cartográfica declarada e as limitações das geometrias apresentadas estão documentadas. Os campos `0.1.0` existentes nas aplicações são metadados de desenvolvimento e não significam que a versão foi publicada.

## Depois de v0.1

| Etapa proposta | Resultado e condição |
| --- | --- |
| v0.2 — Comparações | Comparar municípios e períodos, com fórmulas documentadas e tratamento explícito de mudanças metodológicas e territoriais. Não pressupor continuidade entre [`0008273`](data/code-dictionary.md#ine-indicator-0008273) e [`0012918`](data/code-dictionary.md#ine-indicator-0012918). |
| v0.3 — Segundo tema | Selecionar e estudar um dataset concreto antes de integrar uma nova fonte. E-REDES é candidata para energia, sujeita a verificação de licença, unidade, cobertura e geografia. Definir a [política de autoridade e conflitos por conceito](https://github.com/rucorreias/ptscope/issues/8) antes de conciliar fontes concorrentes. |

## Decisões que esta etapa não força

A passagem de dados da API para o frontend não exige já PostgreSQL, PostGIS, ORM, migrações, jobs ou Redis. Na v0.1, os únicos fornecedores de dados integrados são INE e GEO API PT; a DGT/CAOP é preservada como origem cartográfica declarada pela GEO API PT, sem integração direta. O modelo conceptual e o contrato da API vêm antes do modelo físico; uma forma limitada e reprodutível de obter os dados de v0.1 é suficiente enquanto a decisão de persistência nasce dos requisitos e das observações reais. As descobertas sobre fontes pertencem a `docs/data/sources/`; as decisões internas a `docs/architecture/`.
