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

A coluna `normalized_value` apenas deve ser preenchida quando a transformação estiver semânticamente confirmada e validada.

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
