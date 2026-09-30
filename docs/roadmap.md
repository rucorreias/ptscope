# Plano de entregas do PTScope

> Este plano descreve o que falta entregar; as funcionalidades listadas ainda não estão todas disponíveis. O estado do código foi revisto em 29 de setembro de 2026 (`main` em `f36aa842`). Consulta as [issues](https://github.com/rucorreias/ptscope/issues) para ver as tarefas e os critérios de conclusão.

## Estado atual

O backend FastAPI disponibiliza health check e consulta municipal pela GEO API PT. O frontend Next.js já tem navegação Mapa/Dashboards, barra lateral e um mapa base MapLibre; os limites administrativos e os indicadores demográficos ainda não estão ligados. Existem estudos de GEO API PT, INE, Portal BASE e DGT/SNIG/CAOP em [`docs/data/sources/`](data/sources/). As decisões de ingestão estão em [`docs/architecture/data-ingestion.md`](architecture/data-ingestion.md). O CI atual executa pytest e pylint no backend; a validação do frontend ainda é local.

## v0.1 — Evolução da população por município

**Pergunta do utilizador:** como evoluiu a população residente de um município em todos os períodos que conseguimos verificar e explicar?

Na primeira versão, a pessoa poderá escolher um município e um período, ver os valores confirmados e consultar a definição do indicador, a unidade, a fonte, as datas e as limitações. A geometria municipal virá da GEO API PT quando as condições de uso e o contexto estiverem confirmados. Um valor do INE só será mostrado nesse município do mapa depois de validarmos a ligação entre os códigos territoriais.

A série [`0008273`](data/code-dictionary.md#ine-indicator-0008273) tem uma quebra metodológica entre 2020 e 2021: vamos assinalá-la e evitar cálculos que atravessem essa quebra sem uma regra justificada. Vamos investigar [`0012918`](data/code-dictionary.md#ine-indicator-0012918) para anos recentes, sem juntar as séries antes de confirmar que são comparáveis. Um ano sem valor não vira zero; um município sem correspondência não recebe um polígono escolhido apenas pelo nome.

O [modelo de domínio](architecture/domain-model.md) explica o que é um indicador, uma observação, um período, uma referência geográfica e a origem de cada dado. É um rascunho enquanto investigamos as fontes ([#1](https://github.com/rucorreias/ptscope/issues/1) e [#2](https://github.com/rucorreias/ptscope/issues/2)). Vamos validá-lo com respostas reais antes de definir o contrato da API ([#3](https://github.com/rucorreias/ptscope/issues/3)). As tabelas da base de dados ficam para uma decisão posterior.

| Ordem | Entrega verificável | Issue |
| --- | --- | --- |
| 1, em paralelo | Confirmar períodos, categorias, valores e eventuais revisões; estudar a extensão recente | [#1](https://github.com/rucorreias/ptscope/issues/1) |
| 1, em paralelo | Validar referências municipais INE ↔ GEO API PT, incluindo diferenças entre referenciais e casos sem correspondência | [#2](https://github.com/rucorreias/ptscope/issues/2) |
| 2 | Validar o modelo conceptual de domínio com exemplos reais; depois especificar dashboard e contrato da API | [#3](https://github.com/rucorreias/ptscope/issues/3) |
| 3, em paralelo | Implementar adapter INE e endpoint com testes offline | [#4](https://github.com/rucorreias/ptscope/issues/4) |
| 3, em paralelo | Apresentar geometria municipal da GEO API PT com origem e condições de uso identificadas | [#5](https://github.com/rucorreias/ptscope/issues/5) |
| 4 | Ligar o dashboard aos dados e ao mapa apenas para correspondências validadas | [#6](https://github.com/rucorreias/ptscope/issues/6) |
| Ao longo da entrega | Adicionar validação frontend ao CI e fechar a lista de evidências da versão | [#7](https://github.com/rucorreias/ptscope/issues/7) |

**Quando podemos publicar a v0.1:** a pessoa consegue ver a evolução confirmada de um município, perceber os anos em falta e a quebra metodológica e chegar à fonte de cada valor. A edição geográfica, as condições de uso e as limitações das geometrias estão documentadas. Os testes e verificações do backend e do frontend passam no CI. O número `0.1.0` que já aparece nas aplicações é apenas um identificador de desenvolvimento; não significa que a versão esteja publicada.

## Depois de v0.1

| Etapa proposta | Resultado e condição |
| --- | --- |
| v0.2 — Comparações | Comparar municípios e períodos, com fórmulas documentadas e tratamento explícito de mudanças metodológicas e territoriais. Não pressupor continuidade entre [`0008273`](data/code-dictionary.md#ine-indicator-0008273) e [`0012918`](data/code-dictionary.md#ine-indicator-0012918). |
| v0.3 — Segundo tema | Selecionar e estudar um dataset concreto antes de integrar uma nova fonte. E-REDES é candidata para energia, sujeita a verificação de licença, unidade, cobertura e geografia. Definir a [política de autoridade e conflitos por conceito](https://github.com/rucorreias/ptscope/issues/8) antes de conciliar fontes concorrentes. |

## Decisões que esta etapa não força

Para esta fase, ainda não precisamos de escolher PostgreSQL, PostGIS, ORM, migrações, jobs ou Redis. Primeiro confirmamos os dados e definimos o contrato da API; depois decidimos como os guardar. Na v0.1, os dados integrados vêm apenas do INE e da GEO API PT. A DGT/CAOP fica registada como origem cartográfica declarada, sem integração direta. Os estudos das fontes estão em `docs/data/sources/` e as decisões do PTScope em `docs/architecture/`.
