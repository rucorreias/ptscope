# Investigação #2: municípios INE ↔ GEO API PT

> Estado: **amostra preparada; nenhuma correspondência aprovada**, 30 de setembro de 2026. Este documento cruza os estudos já existentes e regista a limitação da nova consulta neste ambiente. Não é uma tabela nacional de correspondência.

## Fontes e contextos

| Fonte consultada no PTScope | Referência municipal | Contexto da geografia |
|---|---|---|
| INE, indicador [`0008273`](../code-dictionary.md#ine-indicator-0008273) | Categoria da dimensão «Local de residência»; por exemplo, Porto [`11A1312`](../code-dictionary.md#ine-geography-11a1312) | NUTS 2013, versão [`03505`](../code-dictionary.md#ine-version-03505); a metainformação estudada refere CAOP 2020. |
| INE, indicador [`0012918`](../code-dictionary.md#ine-indicator-0012918) | Categoria municipal própria do indicador; Corvo [`2004901`](../code-dictionary.md#ine-geography-2004901) foi observado nas duas respostas filtradas | NUTS 2024, versão [`05257`](../code-dictionary.md#ine-version-05257). Não assumir que a coincidência de um código implica equivalência de todas as geografias. |
| GEO API PT | `dtmn` e `codigoine`; Porto [`1312`](../code-dictionary.md#geoapi-municipality-1312) | A [página do fornecedor](https://geoapi.pt/) declara DGT/CAOP 2024.1 como origem cartográfica. A edição/validade de cada Feature não vem especificada no exemplo estudado. |

INE e GEO API PT são os únicos fornecedores integrados previstos para a v0.1. A DGT é indicada apenas como produtora da cartografia declarada pela GEO API PT. O [estudo INE](../sources/ine.md#12-geografia-e-níveis-territoriais) e o [estudo GEO API PT](../sources/geoapi.md#4-estrutura-administrativa-observada) preservam os exemplos originais.

## Amostra e estado da evidência

| Caso | Código INE observado | Código GEO API PT observado | Estado |
|---|---|---|---|
| Porto, Continente | [`11A1312`](../code-dictionary.md#ine-geography-11a1312), no indicador [`0008273`](../code-dictionary.md#ine-indicator-0008273) | [`1312`](../code-dictionary.md#geoapi-municipality-1312) | **Candidato**, ainda sem correspondência explícita aprovada entre as edições. A semelhança textual e o nome não bastam. |
| Lisboa, Continente | Não extraído no estudo para esta comparação | [`1106`](../code-dictionary.md#geoapi-municipality-1106) | **Por comparar**. |
| Oliveira de Azeméis, zero inicial | Não extraído no estudo para esta comparação | [`0113`](../code-dictionary.md#geoapi-municipality-0113) | **Por comparar**. Guardar o zero inicial. |
| Corvo, Açores | [`2004901`](../code-dictionary.md#ine-geography-2004901) em respostas filtradas dos dois indicadores | Não extraído no estudo GEO API PT | **Por comparar**; não inferir o código do outro fornecedor. |
| Funchal, Madeira | Não extraído para esta comparação | Não extraído para esta comparação | **Por comparar**. |

O INE publicou 308 categorias municipais nas respostas filtradas dos dois indicadores. O estudo GEO API PT encontrou 308 nomes na listagem de municípios, mas **duas contagens iguais não provam uma correspondência um a um**. A lista completa, as exceções nas ilhas, as alterações administrativas e a geometria entre CAOP 2020 e 2024.1 continuam sem validação.

## Tentativa de nova consulta e verificador

Nesta sessão, uma consulta direta a `https://json.geoapi.pt/municipios?codigoine=1312` expirou na ligação de rede; o navegador do ambiente bloqueou o endpoint JSON. Não foram obtidas respostas novas do INE nem da GEO API PT. Por isso, **nenhuma linha acima recebeu o estado «aprovada»**.

O script [`tools/verify_territorial_sample.py`](../../../tools/verify_territorial_sample.py) prepara uma repetição manual com **sete pedidos no máximo**: metainformação dos dois indicadores INE e detalhe de cinco municípios na GEO API PT (Porto, Lisboa, Oliveira de Azeméis, Corvo e Funchal). Não consulta séries estatísticas nem descarrega uma listagem nacional. O resultado JSON guarda URL, hora, estado ou erro, SHA-256, códigos originais, candidatos INE, tipo de geometria e `bbox`; não guarda coordenadas ou payloads completos.

```bash
python3 tools/verify_territorial_sample.py \
  --output /tmp/ptscope_territorial_sample.json \
  --delay 0.75 --timeout 25
```

Nomes servem apenas para **localizar candidatos** dentro da metainformação do INE. Mesmo com nomes coincidentes e códigos parecidos, o script marca `candidate_needs_manual_evidence`, nunca aprova uma ligação. Respostas com códigos não textuais, códigos contraditórios, metainformação incompleta, geometria ausente ou categorias ambíguas ficam `unresolved`.

## Regra para o produto

- O dashboard pode mostrar uma observação do INE com o seu indicador, período e geografia originais, sem exigir polígono.
- O mapa pode mostrar a geometria da GEO API PT como contexto **depois** de confirmar as condições de reutilização/atribuição e o CRS efetivo para a apresentação pretendida.
- Só associar um valor do INE a um polígono quando existir uma correspondência revista, explícita e versionada para aquele indicador, geografia e edição. Sem correspondência, o mapa não pinta o município com o valor nem escolhe um polígono pelo nome.
- Guardar fornecedor técnico, produtor original declarado, URL/parâmetros, data, classificação e versão de cada lado, evidência da ligação e exceções. Uma relação entre códigos não prova igualdade das geometrias CAOP 2020 e 2024.1.

## Para concluir a issue #2

Executar a amostra num ambiente com acesso autorizado às duas APIs; conservar o resumo e rever cada par com evidência oficial de correspondência para as edições concretas. Documentar casos sem par no Continente, Açores e Madeira e verificar a cobertura antes de afirmar uma regra nacional. Confirmar ainda o CRS, a licença e o texto de atribuição aplicáveis à geometria. Até lá, a issue permanece aberta e o mapa estatístico fica condicionado.
