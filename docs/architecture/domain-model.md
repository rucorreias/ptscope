# Modelo conceptual do domínio — v0.1

> **Estado: rascunho de arquitetura, 30-09-2026.** Descreve significados e
> relações, não tabelas, classes Pydantic, endpoints nem contratos físicos. A
> validação da série e da correspondência territorial continua nas issues
> [#1](https://github.com/rucorreias/ptscope/issues/1) e
> [#2](https://github.com/rucorreias/ptscope/issues/2). O contrato da API e a
> especificação final do dashboard continuam na
> [#3](https://github.com/rucorreias/ptscope/issues/3).

## Âmbito e evidência

A v0.1 responde à pergunta «como evoluiu a população residente de um município
nos períodos publicados e verificados?». Os únicos fornecedores de dados
integrados previstos são **INE** (estatística) e **GEO API PT** (contexto e
geometria municipal). A GEO API PT declara que a sua informação administrativa
assenta na CAOP 2024.1, originalmente da DGT. Esta atribuição de origem não
transforma a DGT num terceiro adapter da v0.1.

O [estudo INE](../data/sources/ine.md#61-indicador-0008273) preserva uma
observação real, filtrada, do Porto em 2023 e a metainformação do indicador
[`0008273`](../data/code-dictionary.md#ine-indicator-0008273): NUTS 2013, nota geográfica CAOP 2020 e quebra metodológica
2020–2021. O [estudo GEO API
PT](../data/sources/geoapi.md#5-resposta-real-de-municipioporto) preserva
[`dtmn="1312"`](../data/code-dictionary.md#geoapi-municipality-1312) e uma Feature `geojson` do Porto. A [página oficial da GEO
API PT](https://geoapi.pt/) identifica a CAOP 2024.1 como origem da informação
administrativa. Estes exemplos **não** demonstram igualdade entre as
geometrias das duas edições nem uma regra nacional para relacionar códigos.

O catálogo oficial de dados públicos
identifica [`0012918`](../data/code-dictionary.md#ine-indicator-0012918) ([entrada oficial](https://dados.gov.pt/pt/datasets/populacao-residente-n-o-64))
como indicador anual de população por NUTS 2024, sexo e grupo etário. A
metainformação e as observações deste indicador ainda não foram obtidas
diretamente na investigação atual; cobertura municipal, períodos e
comparabilidade com [`0008273`](../data/code-dictionary.md#ine-indicator-0008273) permanecem por verificar.

## Linguagem do domínio

| Conceito | Significado no PTScope v0.1 | Limite |
| --- | --- | --- |
| **Fornecedor técnico** | Serviço por onde chega a resposta: INE ou GEO API PT. | Não implica ser o produtor de cada campo. |
| **Produtor original / operação** | Entidade e operação estatística ou cartográfica atribuídas à informação, quando conhecidas. | GEO API PT agrega dados de diferentes origens; origem incerta fica assinalada. |
| **Indicador** | Definição publicada de uma medida, com código externo, unidade, periodicidade, dimensões, classificação e notas metodológicas. | [`0008273`](../data/code-dictionary.md#ine-indicator-0008273) e [`0012918`](../data/code-dictionary.md#ine-indicator-0012918) são indicadores distintos até existir prova de equivalência. |
| **Dimensão do indicador** | Eixo publicado pelo INE, com ordem e classificação/versionamento próprios. | A posição `Dim2` é conhecida para o exemplo, não é regra de todos os indicadores. |
| **Categoria** | Código, designação, ordem e nível no âmbito de uma dimensão e versão; [`T`](../data/code-dictionary.md#ine-sex-t) em sexo não é [`T`](../data/code-dictionary.md#ine-age-t) em grupo etário. | Guardar o código de origem como string; «Total» é seleção explícita. |
| **Período de referência** | Categoria temporal da observação: código, designação, ordem e frequência. | Não equivale à data de extração, ingestão ou atualização; não inventar datas de início/fim. |
| **Referência geográfica** | Código e nome publicados, nível, classificação e versão e referência administrativa quando conhecida. | [`11A1312`](../data/code-dictionary.md#ine-geography-11a1312) e [`1312`](../data/code-dictionary.md#geoapi-municipality-1312) são referências distintas; não há identidade universal pelo nome. |
| **Observação recebida** | Célula publicada para um indicador e a seleção completa das suas dimensões numa extração; conserva valor, apresentação e qualificadores. | A ausência de uma célula numa resposta não é uma observação de valor zero. |
| **Extração** | Ocorrência de consulta a um recurso, com parâmetros, datas e referência ao payload. | Repetir o pedido pode produzir uma revisão: não substituir silenciosamente a extração anterior. |
| **Recurso geométrico** | Feature municipal recebida da GEO API PT com código original e contexto cartográfico declarado. | Uma Feature não é uma observação do INE nem representa automaticamente a geografia estatística. |
| **Correspondência territorial** | Afirmação explícita e sustentada entre duas referências geográficas, com contexto, evidência e âmbito. | Pode estar pendente ou ser inválida para determinada edição/período; não resulta de cortar prefixos ou igualar nomes. |

**Nota de modelação:** os nomes acima designam conceitos, não a obrigação de
criar dez entidades persistentes. Classificação, versão e contexto pertencem à
identificação de cada categoria/referência, mesmo quando o fornecedor não
publica um identificador interno estável.

## Relações e invariantes

- Um **indicador** define as dimensões aplicáveis; cada **observação recebida**
  seleciona uma categoria por dimensão pertinente, incluindo período e
  geografia quando existirem. A lista de dimensões varia entre indicadores.
- Uma observação recebida pertence a uma **extração**. Duas extrações com a
  mesma seleção conceptual podem conter valores distintos e devem continuar
  rastreáveis. A identidade lógica da seleção é distinta da identidade da
  resposta recebida; a chave física fica por decidir.
- A seleção de **período** e **geografia** pode ser exposta como relação
  especializada para consulta, mantendo o código original e a dimensão de
  onde veio. A categoria temporal [`S7A2023`](../data/code-dictionary.md#ine-period-s7a2023) e a chave `Dados["2023"]`
  coexistem sem assumir que são intercambiáveis fora deste indicador.
- Uma **correspondência territorial** liga referências especificadas por
  fornecedor, classificação, versão/edição, nível e código. Exige evidência e
  declara o âmbito em que pode ser usada; uma referência sem correspondência
  fica sem valor estatístico aplicado à sua geometria.
- **Fornecedor** e **produtor** não são sinónimos: para limites municipais
  recebidos pela GEO API PT, esta é o fornecedor e a fonte cartográfica
  declarada é a DGT/CAOP 2024.1. Para a observação estudada, o INE fornece e
  indica «INE, Estimativas anuais da população residente» como operação.
- Uma **nota metodológica** deve conservar o seu texto e âmbito (indicador,
  período ou série, conforme publicado). A quebra 2020–2021 deve ser
  apresentada sem fabricar uma taxa de crescimento contínua.
- Códigos externos mantêm zeros e prefixos, como [`0008273`](../data/code-dictionary.md#ine-indicator-0008273), [`11A1312`](../data/code-dictionary.md#ine-geography-11a1312) e
  [`0113`](../data/code-dictionary.md#geoapi-municipality-0113). Valor bruto, valor de apresentação, valor numérico confirmado,
  unidade, potência e precisão são campos semanticamente distintos; um
  qualificador desconhecido não é normalizado.

## Percurso de uma observação verificada

No [pedido INE documentado](../data/sources/ine.md#8-estrutura-dos-dados-reais),
o indicador [`0008273`](../data/code-dictionary.md#ine-indicator-0008273) seleciona período [`S7A2023`](../data/code-dictionary.md#ine-period-s7a2023) (chave de resposta
`2023`), geografia [`11A1312`](../data/code-dictionary.md#ine-geography-11a1312) (Porto), sexo [`T`](../data/code-dictionary.md#ine-sex-t) (HM) e grupo etário
[`T`](../data/code-dictionary.md#ine-age-t) (Total). O campo `valor` é `"267236"` e `ind_string` é
`"267 236"`; a metainformação observada indica unidade `Número (N.º)`,
potência zero e precisão zero. Preservam-se os valores originais e a data de
extração publicada na resposta. A transformação para `Decimal("267236")`
é justificada **para esta célula**, sem inferir que outros indicadores usem a
mesma escala.

No [exemplo GEO API PT](../data/sources/geoapi.md#5-resposta-real-de-municipioporto),
Porto tem [`dtmn="1312"`](../data/code-dictionary.md#geoapi-municipality-1312) e uma Feature municipal. A associação entre
[`11A1312`](../data/code-dictionary.md#ine-geography-11a1312) e [`1312`](../data/code-dictionary.md#geoapi-municipality-1312) é apenas candidata até a issue #2 estabelecer uma
correspondência versionada. Mesmo confirmando a relação dos códigos, isso não
demonstra equivalência geométrica entre CAOP 2020 e 2024.1.

Um exemplo histórico de outra série INE documentado na
[secção de qualificadores](../data/sources/ine.md#10-qualificadores-e-estado-da-observação)
continha `sinal_conv` e nenhuma chave `valor`. Essa situação modela uma
**célula recebida sem valor e com qualificador**. Distingue-se de uma célula
não devolvida na consulta e de um `valor="0"`. A amostra é secundária e
ainda exige revalidação antes de fixar o parser.

## Proveniência e fronteiras

Para cada extração: fornecedor, recurso/endpoint e parâmetros efetivos,
identificador externo, idioma quando aplicável, produtor/operação conhecida,
período de referência, data de atualização da fonte, data de extração da
resposta e data de ingestão do PTScope. Quando possível: referência imutável ao
payload bruto, hash e versão do parser. Se a API não fornecer uma data de
atualização por campo, não inventar essa granularidade.

Para a geometria, conservar também edição cartográfica declarada, referência
de origem e condições de reutilização/atribuição confirmadas **para o recurso
utilizado**. A licença GPL referida na documentação da GEO API PT identifica
software e não resolve por si só a redistribuição dos dados agregados; a
[questão continua aberta](../data/sources/geoapi.md#13-licença-e-condições-de-uso).

O fluxo previsto é **API externa → adapter da fonte → domínio PTScope → API
pública → UI**. O adapter INE interpreta `DimN`, `Dados` e qualificadores;
o adapter GEO API PT interpreta `dtmn` e GeoJSON. A API pública não devolve o
payload externo como contrato próprio. Este documento não fixa JSON de
resposta, armazenamento de snapshots, cache ou estratégia de carregamento da
geometria.

## Casos que o modelo deve distinguir

| Caso | Representação/comportamento |
| --- | --- |
| Ano sem célula devolvida | Cobertura desconhecida/ausente na consulta; verificar filtros e fonte. Não criar zero. |
| Célula devolvida sem `valor`, com qualificador | Preservar o qualificador e a ausência; nunca calcular a partir de `ind_string` sem regra confirmada. |
| Mesma seleção em duas extrações | Conservar ambas e as respetivas datas até existir política explícita de revisão/apresentação. |
| [`0008273`](../data/code-dictionary.md#ine-indicator-0008273) versus [`0012918`](../data/code-dictionary.md#ine-indicator-0012918) | Dois indicadores e referenciais potencialmente distintos; sem linha única antes de validar metodologia e correspondência. |
| INE [`11A1312`](../data/code-dictionary.md#ine-geography-11a1312) versus GEO API PT [`1312`](../data/code-dictionary.md#geoapi-municipality-1312) | Duas referências com possível correspondência, sem join automático nem garantia de equivalência geométrica. |
| Geometria sem licença/CRS suficientemente esclarecidos | Não publicar camada derivada sem confirmar condições e transformação; o mapa base pode continuar como contexto. |

## Investigações e decisões pendentes

1. [#1](https://github.com/rucorreias/ptscope/issues/1): disponibilidade real
   por município/período, [`0012918`](../data/code-dictionary.md#ine-indicator-0012918), qualificadores e revisões. A
   metainformação direta do INE não respondeu nesta consulta; um resultado
   indexado ou um catálogo não substitui uma resposta observada.
2. [#2](https://github.com/rucorreias/ptscope/issues/2): correspondências INE
   ↔ GEO API PT, regiões/edições, geometrias e exceções. Confirmar licença e
   atribuição do uso pretendido, assim como CRS efetivo; os exemplos atuais
   não provam cobertura nacional.
3. [#3](https://github.com/rucorreias/ptscope/issues/3): finalizar a
   especificação do dashboard e **derivar** exemplos de contrato da API a
   partir de respostas reais e casos de ausência. Não fixar campos hipotéticos
   como se fossem factos da fonte.
4. [#8](https://github.com/rucorreias/ptscope/issues/8): após estudar fontes
   concorrentes, definir autoridade e resolução de conflitos por conceito e
   contexto, preservando divergências e proveniência.

Continuam em aberto PostgreSQL/PostGIS, ORM, migrações, modelo físico,
armazenamento bruto, scheduler e cache. As [regras já
aprovadas](data-ingestion.md) continuam a reger qualquer implementação.
