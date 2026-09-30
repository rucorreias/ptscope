# Conclusão da validação INE para a issue #1

> Registo das conclusões da consulta feita em **30 de setembro de 2026, 20:26–20:31 (Europe/Lisbon)**, descrita no [estudo INE](../sources/ine.md#27-validação-v01-população-municipal). Esta página organiza a evidência já publicada; **não representa uma nova consulta**. O resultado JSON detalhado dessa execução ficou em `/tmp` e não foi arquivado no repositório.

## O que foi consultado

O verificador [`tools/verify_ine_population_scope.py`](../../../tools/verify_ine_population_scope.py) consultou a metainformação de [`0008273`](../code-dictionary.md#ine-indicator-0008273) e [`0012918`](../code-dictionary.md#ine-indicator-0012918), seguida de uma resposta filtrada por cada período anual: `Dim3=T` ([sexo HM](../code-dictionary.md#ine-sex-t)) e `Dim4=T` ([grupo etário Total](../code-dictionary.md#ine-age-t)), sem filtrar a geografia. Foram **2 pedidos de metainformação + 18 pedidos de observações**. O estudo regista HTTP 200 para os 20 pedidos da execução completa. Repetições posteriores com timeouts mais curtos não tiveram sempre o mesmo sucesso.

Metainformação observada:

| Indicador | Geografia | Períodos | SHA-256 da resposta de metainformação |
|---|---|---|---|
| [`0008273`](../code-dictionary.md#ine-indicator-0008273) | NUTS 2013, versão [`03505`](../code-dictionary.md#ine-version-03505) | 2011–2023 | `fc245fdb5ffc2c3d9e9f9bb018537248332092489bde9fcedc574211d49f355b` |
| [`0012918`](../code-dictionary.md#ine-indicator-0012918) | NUTS 2024, versão [`05257`](../code-dictionary.md#ine-version-05257) | 2021–2025 | `fccbf9c8800bffb66926522d7a968079cfa8eaa266438299987ab6bc3374f9ed` |

## Resumo por período da execução documentada

As contagens abaixo transcrevem a conclusão agregada do [estudo INE](../sources/ine.md#27-validação-v01-população-municipal): em **cada** ano, a resposta teve o total de linhas geográficas e os 308 municípios esperados. `0` na coluna «municípios sem valor» significa que nenhum dos municípios observados veio sem o campo `valor`; não significa população zero. «Não observados» refere-se aos campos de qualificador nas respostas filtradas. O documento anterior **não guardou hashes nem horários individuais dos 18 payloads**, pelo que esta tabela não permite verificar byte a byte cada resposta histórica.

### Indicador [`0008273`](../code-dictionary.md#ine-indicator-0008273) — população municipal total, NUTS 2013

| Ano | HTTP | Linhas geográficas | Municípios observados | Municípios sem `valor` | Qualificadores |
|---|---:|---:|---:|---:|---|
| 2011 | 200 | 344 | 308 | 0 | Não observados |
| 2012 | 200 | 344 | 308 | 0 | Não observados |
| 2013 | 200 | 344 | 308 | 0 | Não observados |
| 2014 | 200 | 344 | 308 | 0 | Não observados |
| 2015 | 200 | 344 | 308 | 0 | Não observados |
| 2016 | 200 | 344 | 308 | 0 | Não observados |
| 2017 | 200 | 344 | 308 | 0 | Não observados |
| 2018 | 200 | 344 | 308 | 0 | Não observados |
| 2019 | 200 | 344 | 308 | 0 | Não observados |
| 2020 | 200 | 344 | 308 | 0 | Não observados |
| 2021 | 200 | 344 | 308 | 0 | Não observados |
| 2022 | 200 | 344 | 308 | 0 | Não observados |
| 2023 | 200 | 344 | 308 | 0 | Não observados |

A série tem uma **quebra metodológica entre 2020 e 2021**. A nota oficial descrita no estudo distingue estimativas até 2020, assentes em recenseamentos anteriores, das estimativas a partir de 2021, de base administrativa. Não apresentar uma variação que atravesse essa quebra como crescimento diretamente comparável sem uma regra justificada.

### Indicador [`0012918`](../code-dictionary.md#ine-indicator-0012918) — população municipal total, NUTS 2024

| Ano | HTTP | Linhas geográficas | Municípios observados | Municípios sem `valor` | Qualificadores |
|---|---:|---:|---:|---:|---|
| 2021 | 200 | 347 | 308 | 0 | Não observados |
| 2022 | 200 | 347 | 308 | 0 | Não observados |
| 2023 | 200 | 347 | 308 | 0 | Não observados |
| 2024 | 200 | 347 | 308 | 0 | Não observados |
| 2025 | 200 | 347 | 308 | 0 | Não observados |

Esta é **outra série**. A sobreposição de 2021–2023 e uma célula igual no Corvo em 2021 não demonstram equivalência nacional, continuidade metodológica nem igualdade de geografias.

## Decisão para a v0.1

- Podemos especificar uma visualização da população municipal total de 2011–2023 baseada em [`0008273`](../code-dictionary.md#ine-indicator-0008273), com unidade, fonte, data de atualização, período e aviso da quebra 2020–2021. O valor exibido deve conservar o valor e a apresentação originais.
- Podemos manter [`0012918`](../code-dictionary.md#ine-indicator-0012918) como uma segunda série de 2021–2025, identificada como NUTS 2024. **Não juntar as duas numa linha única** nem calcular diferenças entre elas sem prova de comparabilidade.
- Estas consultas validaram apenas `HM/Total`. Não permitem concluir sobre desagregações por sexo ou idade, todos os qualificadores possíveis, revisões de cada célula ou a ligação à geometria da GEO API PT. A correspondência territorial pertence à [issue #2](https://github.com/rucorreias/ptscope/issues/2).

## Como auditar uma nova execução

A partir da raiz do repositório:

```bash
python3 tools/verify_ine_population_scope.py \
  --output /tmp/ptscope_ine_population_scope.json \
  --summary-output /tmp/ptscope_ine_population_scope_summary.json \
  --delay 0.75 --timeout 25 --retries 1
```

O resumo JSON novo guarda **por período** o código temporal, URL, estado HTTP, SHA-256 da resposta, contagens, qualificadores, data de extração e erros. O script deixa de chamar «município inesperado» a uma geografia não classificada: compara os códigos recebidos com municípios e outras geografias conhecidas na metainformação e regista os códigos restantes como **geografias não reconhecidas**, porque a resposta não indica o seu nível. Uma repetição pode obter valores ou hashes diferentes se o INE publicar revisões; guardar a data e o ficheiro da execução usada para decisões posteriores.
