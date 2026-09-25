# Ingestão de Dados: Decisões de Arquitetura

Este documento regista decisões técnicas do PTScope derivadas da investigação das fontes de dados. Não descreve o contrato original das APIs; para isso consultar `docs/data/sources/`.

**Distinção Fundamental:**

- **Facto da fonte** $\rightarrow$ documentado em `docs/data/sources/`
- **Decisão PTScope** $\rightarrow$ documentada em `docs/architecture/data-ingestion.md`

---

## 1. Proveniência como Requisito Obrigatório

Cada dado ingerido deve possuir metadados de proveniência rigorosos para garantir a auditabilidade e a possibilidade de reprocessamento. É obrigatório registar:

- **Provider:** O fornecedor técnico da resposta (ex: `GEO API PT`, `INE`).
- **Fonte/Produtor Original:** A entidade que produziu o dado (ex: `DGT`, `INE`, `IPMA`).
- **Dataset/Operação Estatística:** Quando aplicável, a operação específica (ex: `Estimativas anuais da população residente`).
- **Endpoint:** O URL e parâmetros da consulta efetuada.
- **Identificador Externo:** O código original da fonte (ex: código de difusão do indicador).
- **Datas:**
    - Data de referência do dado.
    - Data de extração da fonte.
    - Data de ingestão no PTScope.

Sempre que possível, devem ser preservados adicionalmente:
- Parâmetros da consulta.
- Hash do payload bruto recebido.
- Versão do transformador/parser utilizado no PTScope.

---

## 2. Preservação de Dados Brutos

Para evitar a perda de informação por transformações irreversíveis, o PTScope deve preservar o valor original recebido antes de qualquer normalização.

**Exemplo de fluxos de valor (INE):**
- `raw_value`: O valor tal como recebido no campo `valor` (ex: `"66.08"`).
- `display_value`: O valor formatado para exibição, se fornecido (ex: `ind_string` $\rightarrow$ `"66,08"`).
- `normalized_value`: O valor convertido para tipo numérico (ex: `Decimal("66.08")`).

A coluna `normalized_value` apenas deve ser preenchida quando a transformação estiver semanticamente confirmada e validada.

---

## 3. Tipos Numéricos e Precisão

Para garantir a integridade de dados estatísticos e evitar erros de arredondamento binário:

- **Valores Estatísticos:** Utilizar obrigatoriamente `Decimal` (ou `numeric` em SQL) para valores que exijam precisão.
- **Proibição de Float:** Evitar o uso de `float` como representação persistida de estatísticas.
- **Exceções:** O tipo `float` pode ser aceitável para certos dados geográficos (coordenadas) onde a precisão binária seja adequada e a performance de cálculo seja prioritária.

---

## 4. Tratamento de Códigos Externos

Todos os códigos provenientes de fontes externas (identificadores territoriais, códigos de indicadores, etc.) devem ser tratados estritamente como **strings**.

**Proibições:**
- Não converter automaticamente para inteiro.
- Não preencher com zeros à esquerda (`padding`) para atingir comprimentos fixos.
- Não remover prefixos.
- Não assumir comprimentos universais.

**Justificação:** Códigos como `1312`, `11A1312`, `0008273` e `S7A2023` representam identificadores em contextos e classificações diferentes; qualquer alteração destrutiva compromete a ligação com a fonte original.

---

## 5. Modelo Conceptual: Indicadores e Observações

O PTScope adota a distinção conceptual entre a definição do dado e a sua ocorrência:

- **Indicator:** Representa a definição estatística (metadados, unidade, periodicidade, fonte, metodologia).
- **Observation:** Representa uma célula concreta no espaço dimensional de um indicador.

**Exemplo de composição de uma Observação:**
`Indicator (0008273)` + `Período (2023)` + `Geografia (11A1312)` + `Sexo (HM)` + `Grupo Etário (Total)` $\rightarrow$ `Valor (267236)`.

---

## 6. Dimensões Genéricas e Flexíveis

O PTScope **não** utilizará um modelo de tabela rígida (ex: colunas fixas para `year`, `municipality`, `sex`, `age`).

**Justificação:** Os indicadores possuem dimensões arbitrárias e variáveis (ex: `causa de morte`, `categoria de alojamento`, `atividade económica`).

**Abordagem:**
O modelo deve suportar uma estrutura hierárquica e dinâmica:
`Indicator` $\rightarrow$ `IndicatorDimension` $\rightarrow$ `Dimension / Classification` $\rightarrow$ `Category`.

Uma observação deve referenciar a combinação completa de categorias relevantes para aquele indicador específico.

---

## 7. Representação Temporal

Para evitar inferências erradas sobre a validade dos dados, a dimensão temporal deve ser preservada de forma granular:

**Campos a preservar separadamente:**
- `period_code`: O código original da categoria temporal (ex: `S7A2023`).
- `period_label`: A designação humana (ex: `2023`).
- `period_order`: A ordem de ordenação publicada pela fonte.
- `frequency`: A periodicidade (anual, trimestral, etc.).

**Regra de Derivação:** Não derivar datas automaticamente de códigos (ex: `S7A2023` $\rightarrow$ `2023-01-01`) sem uma regra de negócio validada e explicitamente documentada para aquela periodicidade e fonte.

---

## 8. Geografia e Versionamento

Uma geografia externa deve preservar o contexto completo da sua origem para evitar ambiguidades:

- `classification`
- `classification_version`
- `administrative_reference`
- `external_code`

**Exemplo de Ambiguidade:**
Os códigos `1312` e `11A1312` podem referir-se territorialmente ao Porto, mas pertencem a contextos e classificações diferentes. Não são identificadores automaticamente intercambiáveis.

O PTScope deve permitir a definição de correspondências explícitas e versionadas entre diferentes entidades territoriais.

---

## 9. Revisões e Histórico

Dados estatísticos podem ser revistos retroativamente pelo produtor. A ingestão não deve assumir que a mesma chave implica um overwrite destrutivo.

O sistema deve preservar informação suficiente para reconstruir alterações e rastrear a evolução dos dados. Mecanismos a considerar incluem:

- Snapshots de ingestão.
- Histórico de versões da observação.
- Hashes do payload para deteção de mudanças.
- Data de atualização da fonte, data de extração e data de ingestão.

---

## 10. Preservação de Payloads Brutos

Devemos preservar o payload original (ou uma referência imutável ao mesmo) para:

- Auditoria de valores.
- Debugging de transformações.
- Reprocessamento total após alteração de regras.
- Evolução do parser sem necessidade de nova extração.

A decisão sobre o meio de armazenamento (PostgreSQL, JSONB, filesystem, object storage) permanece aberta.

---

## 11. Padrão de Integração de Fontes

O fluxo de dados segue a seguinte hierarquia:

`External API` $\rightarrow$ `Source-specific adapter/service` $\rightarrow$ `Normalized PTScope model`

**Princípios:**
- A API pública do PTScope não deve expor diretamente payloads externos.
- Cada provider deve ter o seu próprio adapter dedicado para isolar a fragilidade da fonte.

---

## 12. APIs Frágeis e Rate Limiting

Com base no comportamento observado (especialmente no INE), a integração deve implementar:

- Concorrência conservadora.
- Timeouts explícitos.
- Retry limitado com backoff para HTTP 429 e falhas transitórias.
- Pedidos pequenos e filtrados para evitar bloqueios.
- Cache de metainformação para reduzir a carga na fonte.

Valores como `max retries`, `backoff seconds`, `concurrency` e `cache TTL` deverão ser configuráveis e não fixos no código.

---

## 13. Estratégia de Testes

### Testes Normais
O framework de testes será o `pytest`. As integrações externas devem ser testadas prioritariamente via:
- Mocks de respostas.
- Fixtures reais minimizadas.
- Testes de parsing totalmente offline.

O CI normal **não** deve depender da disponibilidade ou estabilidade da GEO API PT ou do INE.

### Testes Externos
Pedidos reais às APIs só podem existir em:
- Verificações manuais.
- Suite de integração externa explicitamente separada do pipeline de CI standard.

---

## 14. Fixtures

A estrutura de fixtures recomendada segue a organização por fonte:

```text
backend/tests/fixtures/
├── geoapi/
└── ine/
```

Para o INE, as fixtures deverão cobrir cenários como:
- `meta_0008273.json` (Metadados de indicador).
- `data_0008273_porto.json` (Dados de observação).
- `meta_monthly.json` / `data_monthly.json` (Ciclos mensais).
- `meta_quarterly.json` / `data_quarterly.json` (Ciclos trimestrais).
- `catalog_sample.xml` (Amostra do catálogo).

---

## 15. Do Not Infer

O PTScope **não deve** realizar as seguintes transformações automaticamente sem confirmação documental explícita:

- Usar `areaha` como área normalizada.
- Aplicar o fator $10^{Potencia10}$ ao valor.
- Considerar dois indicadores equivalentes apenas por terem nomes semelhantes.
- Considerar duas geografias equivalentes apenas pelo nome.
- Interpretar qualificadores desconhecidos.
- Adicionar ou remover zeros de códigos.
- Remover prefixos territoriais.
- Juntar automaticamente séries NUTS de versões diferentes.
- Transformar dado confidencial, ausente ou não disponível em zero.
- Derivar períodos através de parsing cego de códigos.

**Regra Geral:**
`Semântica desconhecida` $\rightarrow$ `Preservar valor bruto` $\rightarrow$ `Não produzir valor normalizado` $\rightarrow$ `Registar questão em aberto`.

---

## 16. Fonte de Verdade Documental

Para evitar conflitos de informação, estabelece-se:

- `docs/data/sources/`: Fonte de verdade para **"O que a fonte externa faz?"**.
- `docs/architecture/`: Fonte de verdade para **"O que o PTScope decidiu fazer com essa informação?"**.

Sempre que uma decisão arquitetural depender de uma descoberta concreta, deve referenciar o documento correspondente em `docs/data/sources/`.

---

## 17. Decisões Ainda Não Tomadas

Para evitar a implementação prematura, regista-se que as seguintes definições **estão abertas**:

- Schema PostgreSQL final e modelo físico de observations.
- Escolha de ORM (SQLAlchemy, etc.) e ferramenta de migrações (Alembic).
- Estratégia de armazenamento de raw payloads (JSONB vs outros).
- Estratégia de particionamento de dados.
- Tecnologias de infraestrutura (Redis, Scheduler, Message Queues).
- Política completa de cache e retenção de dados.
- Modelo final de PostGIS.

---

## 18. Relação com os Documentos de Descoberta

Os documentos em `docs/data/sources/` devem manter todos os factos observados. Recomendações de implementação podem permanecer se ajudarem a explicar a implicação da fonte, mas:

- Devem estar marcadas como inferência/recomendação.
- Este documento (`docs/architecture/data-ingestion.md`) é a referência principal para decisões internas.
- Devem ser adicionados links para as secções de arquitetura correspondentes.
