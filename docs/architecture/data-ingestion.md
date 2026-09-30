# Ingestão de dados: decisões de arquitetura

Aqui ficam as regras que o PTScope segue ao receber e tratar dados. Para saber o que cada API devolve, consulta os [estudos das fontes](../data/sources/). O [modelo de domínio](domain-model.md) explica como estas regras se aplicam à v0.1.

**Onde procurar informação:**

- Os [estudos das fontes](../data/sources/) registam o que foi documentado ou observado nas APIs.
- Este documento regista o que decidimos fazer no PTScope com essa informação.

---

## 1. Proveniência como Requisito Obrigatório

Para conseguirmos explicar de onde veio um valor e voltar a processá-lo, guardamos:

- **Fornecedor:** A API que respondeu (por exemplo, `GEO API PT` ou `INE`).
- **Produtor original:** Quem produziu o dado, quando conhecido (por exemplo, `DGT` ou `INE`).
- **Conjunto de dados ou operação estatística:** Por exemplo, `Estimativas anuais da população residente`.
- **Pedido feito à API:** O URL e os parâmetros usados.
- **Código original:** Por exemplo, o código de difusão de um indicador.
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

Guardar o valor recebido antes de o converter. Assim, podemos voltar a verificar uma conversão ou corrigir uma regra sem perder a resposta original.

**Exemplo de fluxos de valor (INE):**
- `raw_value`: O valor tal como recebido no campo `valor` (ex: `"66.08"`).
- `display_value`: O valor formatado para exibição, se fornecido (ex: `ind_string` $\rightarrow$ `"66,08"`).
- `normalized_value`: O valor convertido para tipo numérico (ex: `Decimal("66.08")`).

Preencher `normalized_value` só quando estiver confirmado o significado do valor e a regra de conversão.

---

## 3. Tipos Numéricos e Precisão

Para não introduzir erros de arredondamento nos valores estatísticos:

- **Valores Estatísticos:** Utilizar obrigatoriamente `Decimal` (ou `numeric` em SQL) para valores que exijam precisão.
- **Proibição de Float:** Evitar o uso de `float` como representação persistida de estatísticas.
- **Exceções:** O tipo `float` pode ser aceitável para certos dados geográficos (coordenadas) onde a precisão binária seja adequada e a performance de cálculo seja prioritária.

---

## 4. Tratamento de Códigos Externos

Guardar códigos externos como **texto**. Isto inclui indicadores e identificadores territoriais, mesmo quando têm apenas algarismos.

**Não fazer:**
- Não converter automaticamente para inteiro.
- Não preencher com zeros à esquerda (`padding`) para atingir comprimentos fixos.
- Não remover prefixos.
- Não assumir comprimentos universais.

**Porquê?** [`1312`](../data/code-dictionary.md#geoapi-municipality-1312), [`11A1312`](../data/code-dictionary.md#ine-geography-11a1312), [`0008273`](../data/code-dictionary.md#ine-indicator-0008273) e [`S7A2023`](../data/code-dictionary.md#ine-period-s7a2023) identificam coisas diferentes. Mudar um código pode impedir-nos de encontrar a informação original. Consulta o [dicionário de códigos](../data/code-dictionary.md) para ver o contexto de cada um.

---

## 5. Modelo Conceptual: Indicadores e Observações

O [rascunho do modelo conceptual de domínio da v0.1](domain-model.md) aplica estas regras a observações INE e à informação territorial da GEO API PT. Distingue referências geográficas e extrações sem decidir ainda o contrato da API nem o esquema da base de dados.


É útil separar a **definição do que se mede** do **valor publicado para um caso concreto**:

- **Indicador:** Define a medida, unidade, periodicidade, fonte e metodologia.
- **Observação:** É o valor (ou a indicação de que não está disponível) para uma combinação de categorias desse indicador.

**Exemplo:** o indicador [`0008273`](../data/code-dictionary.md#ine-indicator-0008273), no período de 2023, para a geografia INE [`11A1312`](../data/code-dictionary.md#ine-geography-11a1312) (Porto), ambos os sexos e todas as idades, tem o valor observado de 267 236. A categoria de período é [`S7A2023`](../data/code-dictionary.md#ine-period-s7a2023); `2023` é a chave usada na resposta.

---

## 6. Dimensões Genéricas e Flexíveis

O PTScope não deve assumir que todos os indicadores têm as mesmas colunas (como `year`, `municipality`, `sex` e `age`).

**Porquê?** Um indicador pode ter sexo e idade; outro pode ter causa de morte, categoria de alojamento ou atividade económica.

**Abordagem:**
O modelo deve suportar uma estrutura hierárquica e dinâmica:
`Indicator` $\rightarrow$ `IndicatorDimension` $\rightarrow$ `Dimension / Classification` $\rightarrow$ `Category`.

Uma observação deve referenciar a combinação completa de categorias relevantes para aquele indicador específico.

---

## 7. Representação Temporal

Para evitar inferências erradas sobre a validade dos dados, a dimensão temporal deve ser preservada de forma granular:

**Campos a preservar separadamente:**
- `period_code`: O código original da categoria temporal (ex: [`S7A2023`](../data/code-dictionary.md#ine-period-s7a2023)).
- `period_label`: A designação humana (ex: `2023`).
- `period_order`: A ordem de ordenação publicada pela fonte.
- `frequency`: A periodicidade (anual, trimestral, etc.).

**Regra:** [`S7A2023`](../data/code-dictionary.md#ine-period-s7a2023) não indica, por si só, que o período começou em `2023-01-01`. Só calcular datas de início ou fim quando existir uma regra confirmada para essa fonte e periodicidade.

---

## 8. Geografia e Versionamento

Uma geografia externa deve preservar o contexto completo da sua origem para evitar ambiguidades:

- `classification`
- `classification_version`
- `administrative_reference`
- `external_code`

**Exemplo:**
Os códigos [`1312`](../data/code-dictionary.md#geoapi-municipality-1312) e [`11A1312`](../data/code-dictionary.md#ine-geography-11a1312) podem referir-se territorialmente ao Porto, mas pertencem a contextos e classificações diferentes. Não são identificadores automaticamente intercambiáveis.

Uma ligação entre códigos territoriais precisa de fonte, classificação, versão e prova dessa correspondência.

---

## 9. Revisões e Histórico

A fonte pode corrigir valores antigos. Se a mesma combinação de indicador, período e categorias aparecer de novo, não apagar silenciosamente a resposta anterior.

O sistema deve preservar informação suficiente para reconstruir alterações e rastrear a evolução dos dados. Mecanismos a considerar incluem:

- Snapshots de ingestão.
- Histórico de versões da observação.
- Hashes do payload para deteção de mudanças.
- Data de atualização da fonte, data de extração e data de ingestão.

---

## 10. Preservação de Payloads Brutos

Devemos preservar o payload original (ou uma referência imutável ao mesmo) para:

- Auditoria de valores.
- Investigar erros nas conversões.
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

<a id="15-do-not-infer"></a>

## 15. Não inferir sem confirmação

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

**Regra geral:** se ainda não sabemos o que um campo significa, guardar a resposta original, não criar um valor convertido e registar o que falta confirmar.

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
