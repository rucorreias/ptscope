# Dicionário de códigos externos

Aqui encontras os códigos usados nos documentos e o que significam **em cada fonte**. Para interpretar um código, precisamos também do seu tipo, da classificação e da versão. O mesmo texto pode ter significados diferentes; estar nesta lista não prova que dois códigos de fontes diferentes sejam equivalentes.

Na v0.1, só vamos integrar dados do **INE** e da **GEO API PT**. Os códigos do BASE e da DGT aparecem porque os estudos dessas fontes também estão documentados. A DGT pode ainda ser indicada como origem cartográfica dos dados fornecidos pela GEO API PT.

**Como usar este dicionário:** nos textos e tabelas, cada código aponta para a sua entrada. Nos exemplos JSON, URLs e comandos, a ligação fica ao lado para não alterar o exemplo. Anos, valores medidos, montantes, NIF, telefones, estados HTTP e nomes de campos não são códigos de classificação. A chave `Dados["2023"]` é um exemplo de valor temporal devolvido pela API, não um código de categoria. Os IDs de registo têm uma secção própria.

## Indicadores INE

Fonte de referência: [estudo INE](sources/ine.md). O tipo de evidência refere-se apenas ao exemplo descrito no estudo.

| Código | Significado neste contexto | Evidência |
|---|---|---|
| <a id="ine-indicator-0008273"></a>`0008273` | População residente por sexo e grupo etário; série observada com NUTS 2013, até município. | Observado |
| <a id="ine-indicator-0012918"></a>`0012918` | População residente por local de residência NUTS 2024, sexo e grupo etário; identificado no catálogo; metainformação JSON e comparabilidade por validar. | Documentado no catálogo |
| <a id="ine-indicator-0010006"></a>`0010006` | Idade média ao óbito por sexo e causa de morte; cobertura observada até NUTS III. | Observado |
| <a id="ine-indicator-0012910"></a>`0012910` | Índice de dependência de idosos; NUTS 2024. | Documentado |
| <a id="ine-indicator-0012234"></a>`0012234` | Valor mediano das vendas de alojamentos, últimos 12 meses; trimestral. | Documentado |
| <a id="ine-indicator-0010042"></a>`0010042` | Valor mediano de avaliação bancária da habitação; mensal. | Documentado |
| <a id="ine-indicator-0013012"></a>`0013012` | Ganho/remuneração por trabalhador; difundido pelo INE com fonte MTSSS/GEP. | Documentado |
| <a id="ine-indicator-0010003"></a>`0010003` | Orçamento do Estado financiado por impostos cobrados internamente. | Observado |
| <a id="ine-indicator-0002642"></a>`0002642` | Superfície das unidades territoriais; NUTS 2001, fonte DGT. | Documentado |

## Versões de dimensão e associação INE

Fonte de referência: [estudo INE](sources/ine.md). O tipo de evidência refere-se apenas ao exemplo descrito no estudo.

| Código | Significado neste contexto | Evidência |
|---|---|---|
| <a id="ine-version-03505"></a>`03505` | Versão da dimensão de residência NUTS 2013 na metainformação JSON; no SMI aparece como V03505. | Observado |
| <a id="ine-version-00305"></a>`00305` | Versão da dimensão sexo na metainformação JSON. | Observado |
| <a id="ine-version-00708"></a>`00708` | Versão da dimensão grupo etário na metainformação JSON. | Observado |
| <a id="ine-version-03622"></a>`03622` | Versão da dimensão causa de morte (lista OCDE adaptada) na metainformação JSON. | Observado |
| <a id="ine-version-v03505"></a>`V03505` | Identificador SMI da hierarquia NUTS 2013; corresponde à representação 03505 sem prefixo na API JSON, conforme estudo. | Documentado |
| <a id="ine-version-v05257"></a>`V05257` | Identificador SMI da hierarquia NUTS 2024. | Documentado |
| <a id="ine-version-v04479"></a>`V04479` | Identificador SMI da associação NUTS 2013/CAOP 2020. | Documentado |
| <a id="ine-version-v05320"></a>`V05320` | Identificador SMI da associação NUTS 2024/CAOP 2020. | Documentado |

## Categorias INE de período e dimensão

Fonte de referência: [estudo INE](sources/ine.md). O tipo de evidência refere-se apenas ao exemplo descrito no estudo.

| Código | Significado neste contexto | Evidência |
|---|---|---|
| <a id="ine-period-s7a2023"></a>`S7A2023` | Categoria anual do indicador [`0008273`](#ine-indicator-0008273); a resposta guarda os dados sob a chave `2023`. | Observado |
| <a id="ine-period-s3a202006"></a>`S3A202006` | Exemplo mensal retirado de uma fonte secundária antiga; a resposta usa a chave `202006`. Este formato ainda não está confirmado para todos os indicadores. | Histórico, fonte secundária |
| <a id="ine-geography-pt"></a>`PT` | Categoria geográfica Portugal na hierarquia observada de 0008273. | Observado |
| <a id="ine-geography-1"></a>`1` | Categoria geográfica Continente, NUTS I, na hierarquia de 0008273. | Observado |
| <a id="ine-geography-11"></a>`11` | Categoria geográfica Norte, NUTS II, na hierarquia de 0008273. | Observado |
| <a id="ine-geography-11a"></a>`11A` | Categoria geográfica Área Metropolitana do Porto, NUTS III, na hierarquia de 0008273. | Observado |
| <a id="ine-geography-11a1312"></a>`11A1312` | Porto na hierarquia NUTS 2013 do indicador [`0008273`](#ine-indicator-0008273). Não substituir automaticamente por [`1312`](#geoapi-municipality-1312). | Observado |
| <a id="ine-sex-t"></a>`T` | Total/HM na dimensão sexo do indicador [`0008273`](#ine-indicator-0008273); noutra dimensão, `T` pode significar outra coisa. | Observado |
| <a id="ine-sex-1"></a>`1` | Categoria H da dimensão sexo do indicador 0008273, distinta da categoria geográfica 1. | Observado |
| <a id="ine-sex-2"></a>`2` | Categoria M da dimensão sexo do indicador 0008273. | Observado |
| <a id="ine-age-t"></a>`T` | Total na dimensão grupo etário do indicador [`0008273`](#ine-indicator-0008273); diferente de [sexo `T`](#ine-sex-t). | Observado |

## Geografia municipal, freguesia e NUTS noutras fontes

Os códigos municipais foram observados no [estudo GEO API PT](sources/geoapi.md). Os exemplos DGT e BASE são identificados na respetiva linha. A evidência aplica-se a cada contexto, não ao literal isolado.

| Código | Significado neste contexto | Evidência |
|---|---|---|
| <a id="geoapi-municipality-1312"></a>`1312` | Município do Porto na GEO API PT; também observado como DTMN na CAOP 2025 da DGT. A ligação ao código INE [`11A1312`](#ine-geography-11a1312) exige confirmação da classificação e da versão. | Observado; ver [estudo DGT](sources/dgt-snig.md) |
| <a id="geoapi-municipality-1106"></a>`1106` | Município de Lisboa na GEO API PT. | Observado |
| <a id="geoapi-municipality-0113"></a>`0113` | Município de Oliveira de Azeméis na GEO API PT; preservar zero inicial. | Observado |
| <a id="geoapi-parish-131202"></a>`131202` | Freguesia do Bonfim na GEO API PT; também observada na CAOP 2025. | Observado; ver [estudo DGT](sources/dgt-snig.md) |
| <a id="dgt-nuts-1d3"></a>`1D3` | NUTS III apresentado no exemplo da freguesia de Pernes na CAOP 2025; não inferir relação com outras classificações. | Exemplo observado; ver [estudo DGT](sources/dgt-snig.md) |
| <a id="dgt-parish-141614"></a>`141614` | Código de freguesia num exemplo de resposta CAOP/DGT; significado e edição dependem do contexto do exemplo. | Exemplo observado; ver [estudo DGT](sources/dgt-snig.md) |
| <a id="base-nuts-pt11a"></a>`PT11A` | Código NUTS numa amostra BASE; não identifica município e a versão NUTS não consta do registo. | Observado; ver [estudo BASE](sources/base.md) |
| <a id="base-nuts-pt150"></a>`PT150` | Algarve na amostra de localização NUTS do BASE; classificação/edição a confirmar antes de reconciliar. | Exemplo observado; ver [estudo BASE](sources/base.md) |
| <a id="base-nuts-ptzzz"></a>`PTZZZ` | Extra-Regio NUTS 3 (Todos) na amostra BASE; versão a confirmar. | Exemplo observado; ver [estudo BASE](sources/base.md) |

## CRS identificados por EPSG no estudo DGT

Fonte de referência: [estudo DGT](sources/dgt-snig.md). O tipo de evidência refere-se apenas ao exemplo descrito no estudo.

| Código | Significado neste contexto | Evidência |
|---|---|---|
| <a id="epsg-3763"></a>`EPSG:3763` | PT-TM06/ETRS89, usado no continente e anunciado como CRS de armazenamento da coleção de municípios. | Ver estudo DGT |
| <a id="epsg-4326"></a>`EPSG:4326` | WGS 84, listado nos metadados DGT e na coleção OGC; o CRS da GEO API PT não foi confirmado. | Ver estudo DGT |
| <a id="epsg-4258"></a>`EPSG:4258` | ETRS89, indicado nos metadados e na coleção OGC. | Ver estudo DGT |
| <a id="epsg-5016"></a>`EPSG:5016` | PTRA08-UTM/ITRF93, Madeira no estudo DGT. | Ver estudo DGT |
| <a id="epsg-5014"></a>`EPSG:5014` | PTRA08-UTM/ITRF93, Açores grupo ocidental no estudo DGT. | Ver estudo DGT |
| <a id="epsg-5015"></a>`EPSG:5015` | PTRA08-UTM/ITRF93, Açores grupos central e oriental no estudo DGT. | Ver estudo DGT |
| <a id="epsg-5013"></a>`EPSG:5013` | CRS listado nos metadados DGT para Açores e Madeira; não inferir o CRS de cada geometria. | Ver estudo DGT |
| <a id="epsg-3857"></a>`EPSG:3857` | CRS anunciado na coleção OGC da DGT; não inferir o CRS da GEO API PT. | Ver estudo DGT |

## CPV, identificadores de exemplo e recursos externos

Os códigos CPV e os IDs de exemplo vêm do [estudo BASE](sources/base.md). Os identificadores SMI e os recursos INE são explicados nos estudos [INE](sources/ine.md) e [DGT](sources/dgt-snig.md). O tipo de evidência refere-se a cada exemplo.

| Código | Significado neste contexto | Evidência |
|---|---|---|
| <a id="base-cpv-72210000-0"></a>`72210000-0` | Serviços de programação de pacotes de software, conforme exemplo no download BASE. | Observado |
| <a id="base-cpv-30230000-0"></a>`30230000-0` | Código CPV presente num payload de exemplo BASE; validar designação na fonte antes de a usar. | Exemplo observado |
| <a id="base-idcontrato-12380006"></a>`12380006` | Valor de exemplo de idcontrato no BASE; identificador de registo, não categoria de vocabulário. | Exemplo observado |
| <a id="base-idprocedimento-8111559"></a>`8111559` | Valor de exemplo de idprocedimento no BASE; identificador de registo. | Exemplo observado |
| <a id="base-idincm-419938349"></a>`419938349` | Valor de exemplo de IdIncm no BASE; identificador de anúncio. | Exemplo observado |
| <a id="ine-smi-17818"></a>`17818` | Identificador da página SMI do indicador [`0012910`](#ine-indicator-0012910); não substituir um pelo outro. | Observado; ver [estudo INE](sources/ine.md) |
| <a id="ine-resource-9160"></a>`9160` | Identificador de recurso de download da tabela de correspondência do SMI INE. | Link oficial no [estudo DGT](sources/dgt-snig.md) |
| <a id="ine-resource-10698"></a>`10698` | Identificador de outro recurso de download da tabela de correspondência do SMI INE. | Link oficial no [estudo DGT](sources/dgt-snig.md) |

**Atenção a códigos parecidos:** [`03505`](#ine-version-03505) e [`V03505`](#ine-version-v03505) representam a mesma versão no exemplo API/SMI estudado. O significado de `1` e `T` muda com a dimensão: [geografia `1`](#ine-geography-1) e [sexo `1`](#ine-sex-1); [sexo `T`](#ine-sex-t) e [grupo etário `T`](#ine-age-t). A ligação entre [`1312`](#geoapi-municipality-1312) e [`11A1312`](#ine-geography-11a1312) ainda precisa de validação por edição territorial.
