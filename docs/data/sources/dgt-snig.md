# DGT, SNIG e Carta Administrativa Oficial de Portugal (CAOP)

## 1. Âmbito e método

Este documento descreve o contrato observável das fontes oficiais da
Direção-Geral do Território (DGT), do Sistema Nacional de Informação
Geográfica (SNIG) e da Carta Administrativa Oficial de Portugal (CAOP). O
objetivo é apoiar a descoberta de dados do PTScope; não define um modelo de
persistência, uma política de autoridade entre fontes nem uma integração.

As conclusões usam as seguintes etiquetas:

- **Documentado**: afirmação presente em documentação, metadados ou legislação
  oficial.
- **Observado**: comportamento verificado diretamente numa resposta, ficheiro
  ou recurso oficial em 2026-09-28.
- **Inferência**: interpretação plausível, mas não confirmada como contrato da
  fonte.
- **Decisão do PTScope**: regra de tratamento adotada ou proposta pelo projeto;
  não descreve uma propriedade da DGT, do SNIG ou da CAOP.

**Observado:** A investigação usou apenas pedidos `GET` públicos, sequenciais e
com timeout. Não foi descarregada cartografia nacional. Foram consultados
metadados e respostas pequenas; o único ficheiro descarregado integralmente foi
a tabela CAOP 2025 de áreas e perímetros, com cerca de 388 kB. Foi ainda pedido
um único elemento GeoJSON do município do Porto, com cerca de 416 kB. Para os
ficheiros GeoPackage nacionais foi usado um pedido parcial de um byte para
confirmar disponibilidade e dimensão.

**Decisão do PTScope:** sempre que a semântica não esteja confirmada, o valor
deve ser preservado em bruto, não deve ser normalizado e a dúvida deve ficar
documentada.

## 2. Visão geral

### 2.1 DGT

**Documentado:** A DGT é um serviço central da administração direta do Estado.
Entre as suas atribuições estão a execução da política de ordenamento do
território e a produção, manutenção e disponibilização de informação geográfica
de referência. A DGT gere o geoportal do SNIG e assegura a sua coordenação
operacional.

Fontes:

- [DGT — Carta Administrativa Oficial de Portugal](https://www.dgterritorio.gov.pt/atividades/cartografia/cartografia-tematica/caop)
- [SNIG — coordenação operacional](https://snig.dgterritorio.gov.pt/saber-mais/coordenacao/coordenacao-operacional)
- [Decreto-Lei n.º 29/2017](https://diariodarepublica.pt/dr/detalhe/decreto-lei/29-2017-106616122)

### 2.2 SNIG e RNDG

**Documentado:** O SNIG é a infraestrutura nacional de dados espaciais. O seu
geoportal permite pesquisar, visualizar e aceder a conjuntos e serviços de
dados geográficos registados por produtores públicos e privados. O SNIG não é,
por esse facto, o produtor de todos os recursos que cataloga.

**Documentado:** O Registo Nacional de Dados Geográficos (RNDG) é o catálogo de
metadados integrado no SNIG. O registo é obrigatório para entidades públicas
produtoras de dados geográficos abrangidos e suporta a descoberta e o acesso a
serviços segundo normas OGC e INSPIRE.

Fontes:

- [SNIG — saber mais](https://snig.dgterritorio.gov.pt/saber-mais)
- [SNIG — Registo Nacional de Dados Geográficos](https://snig.dgterritorio.gov.pt/saber-mais/registo-nacional-de-dados-geograficos)
- [Catálogo RNDG](https://snig.dgterritorio.gov.pt/rndg/)

### 2.3 CAOP

**Documentado:** A CAOP regista o estado da delimitação e demarcação das
circunscrições administrativas de Portugal. A Assembleia da República tem a
competência para fixar e alterar limites administrativos; a DGT executa e
mantém a CAOP para fins cadastrais e cartográficos.

**Documentado:** A construção e manutenção da CAOP usa, entre outras fontes, a
base cartográfica dos Censos 2001, diplomas legais, secções cadastrais, dados de
Procedimentos de Delimitação Administrativa acordados com as autarquias e
informação de organismos oficiais.

**Factos documentados:** As fontes consultadas distinguem os seguintes papéis:

| Papel | Entidade ou sistema |
| --- | --- |
| Competência para criar ou alterar limites | Assembleia da República, através de diploma legal |
| Execução e manutenção cartográfica da CAOP | DGT |
| Atribuição dos códigos DTMNFR | Instituto Nacional de Estatística (INE) |
| Catálogo e infraestrutura de descoberta | RNDG/SNIG, geridos pela DGT |
| Serviços e ficheiros de distribuição | DGT |
| Fontes locais de delimitação | Diplomas, autarquias e outros organismos oficiais, conforme a linhagem de cada edição |

**Decisão do PTScope:** Para efeitos de proveniência, o projeto tratará estes
papéis separadamente e não registará o SNIG como produtor da CAOP apenas por a
catalogar ou disponibilizar.

## 3. Fontes oficiais consultadas

### 3.1 Páginas e documentação

- [CAOP — página principal e histórico de versões](https://www.dgterritorio.gov.pt/atividades/cartografia/cartografia-tematica/caop)
- [Repositório oficial do modelo CAOP](https://github.com/dgterritorio/CAOP)
- [Modelo de dados CAOP](https://github.com/dgterritorio/caop/blob/master/documentacao/docs/modelo_de_dados.md)
- [Implementação do modelo CAOP](https://github.com/dgterritorio/caop/blob/master/documentacao/docs/implementacao_modelo.md)
- [DGT — perguntas frequentes](https://www.dgterritorio.gov.pt/loja/perguntas-frequentes)
- [DGT — dados abertos](https://www.dgterritorio.gov.pt/dados-abertos)
- [DGT — conjuntos e serviços de dados geográficos](https://www.dgterritorio.gov.pt/conjuntos-de-dados-geograficos-cdg)
- [Manual oficial da OGC API da DGT](https://dgterritorio.github.io/ogcapi-user/)
- [OGC API da DGT](https://ogcapi.dgterritorio.gov.pt/)

### 3.2 Metadados CAOP 2025 no RNDG

| Cobertura | Registo RNDG | Identificador do registo |
| --- | --- | --- |
| Continente | [CAOP 2025 — Continente](https://snig.dgterritorio.gov.pt/rndg/srv/por/catalog.search#/metadata/198497815bf647ecaa990c34c42e932e) | `198497815bf647ecaa990c34c42e932e` |
| Região Autónoma dos Açores | [CAOP 2025 — RAA](https://snig.dgterritorio.gov.pt/rndg/srv/por/catalog.search#/metadata/d9ca5eef-9860-4f5b-99a8-10661208d727) | `d9ca5eef-9860-4f5b-99a8-10661208d727` |
| Região Autónoma da Madeira | [CAOP 2025 — RAM](https://snig.dgterritorio.gov.pt/rndg/srv/por/catalog.search#/metadata/78aef3be-0232-43ad-9dd5-fcdce15da03f) | `78aef3be-0232-43ad-9dd5-fcdce15da03f` |

**Observado:** Os registos também podem ser obtidos em XML por uma rota de
formatação do GeoNetwork, por exemplo:

```text
GET https://snig.dgterritorio.gov.pt/rndg/srv/api/records/198497815bf647ecaa990c34c42e932e/formatters/xml
```

e por CSW 2.0.2:

```text
GET https://snig.dgterritorio.gov.pt/rndg/srv/por/csw
    ?service=CSW
    &version=2.0.2
    &request=GetRecordById
    &id=198497815bf647ecaa990c34c42e932e
    &elementSetName=full
    &outputSchema=http://www.isotc211.org/2005/gmd
```

**Observado:** A rota sem formatador
`/rndg/srv/api/records/{id}` devolveu HTTP 400 com um erro XML de transformação,
enquanto `/formatters/xml` e o pedido CSW devolveram HTTP 200.

**Limite da evidência:** Este teste não demonstra que todas as rotas internas do
frontend constituam uma API pública ou estável.

### 3.3 Legislação e alterações administrativas

- [Lei n.º 27/2025 — limites no concelho de Santarém](https://diariodarepublica.pt/dr/detalhe/lei/27-2025-911648870)
- [Lei n.º 48/2025 — limites no concelho de Castelo de Paiva](https://diariodarepublica.pt/dr/detalhe/lei/48-2025-913636013)
- [Alterações incluídas na CAOP 2024](https://www.dgterritorio.gov.pt/sites/default/files/ficheiros-cartografia/alteracoes_CAOP2024.pdf)
- [Alterações incluídas na CAOP 2024.1](https://www.dgterritorio.gov.pt/sites/default/files/ficheiros-cartografia/alteracoes_CAOP2024.1.pdf)
- [Alterações incluídas na CAOP 2025](https://www.dgterritorio.gov.pt/sites/default/files/ficheiros-cartografia/alteracoes_CAOP2025.pdf)

## 4. Edições, cobertura e datas de referência

**Documentado:** A DGT disponibiliza edições anuais da CAOP desde 2001. A
página oficial mantém ligações para as versões 2025, 2024.1, 2024, 2023 até
2007 e para versões anteriores identificadas de `6.0` a `1.0`. Existem edições
intercalares, como 2008.1, 2009.0, 2012.1 e 2024.1; por isso, o ano isolado não é
sempre um identificador suficiente da versão.

**Documentado:** A CAOP 2025 foi aprovada por despacho da Diretora-Geral do
Território de 2026-01-28 e publicitada pelo Aviso n.º 3502/2026/2, de
2026-02-18. Integra alterações administrativas ocorridas entre 2025-03-16 e
2025-12-31, concretamente as Leis n.º 27/2025 e n.º 48/2025.

**Documentado:** A tabela de áreas associada à CAOP 2025 declara como data de
referência da DGT `31-12-2025`.

**Documentado:** A CAOP abrange Portugal Continental, a Região Autónoma dos
Açores e a Região Autónoma da Madeira. A distribuição atual separa estas três
coberturas em ficheiros e serviços distintos.

**Observado:** Os três GeoPackages oficiais da edição 2025 estavam acessíveis e
tinham as seguintes dimensões, obtidas sem descarregar o conteúdo integral:

| Cobertura | Recurso oficial | Dimensão observada |
| --- | --- | ---: |
| Continente | [CAOP_Continente_2025-gpkg.zip](https://geo2.dgterritorio.gov.pt/caop/CAOP_Continente_2025-gpkg.zip) | 111 647 845 bytes |
| Açores | [CAOP_RAA_2025-gpkg.zip](https://geo2.dgterritorio.gov.pt/caop/CAOP_RAA_2025-gpkg.zip) | 15 909 724 bytes |
| Madeira | [CAOP_RAM_2025-gpkg.zip](https://geo2.dgterritorio.gov.pt/caop/CAOP_RAM_2025-gpkg.zip) | 15 235 290 bytes |

**Observado:** O ficheiro continental respondeu com `Last-Modified` de
2026-02-02.

**Decisão do PTScope:** O projeto tratará `Last-Modified`, data de referência,
aprovação, publicação e atualização dos metadados como conceitos distintos.
Uma referência à CAOP conservará pelo menos a
edição completa (`2024.1`, por exemplo), a cobertura territorial e a data de
referência quando publicada. “CAOP 2024” e “CAOP 2024.1” são recursos distintos.

## 5. Modelo territorial e identificadores

### 5.1 Hierarquia

**Documentado:** O modelo atual representa:

- distrito ou ilha, nível administrativo 3, identificado por `DI`/`DT`;
- município, nível administrativo 4, identificado por `DICO`/`DTMN`;
- freguesia ou união de freguesias, nível administrativo 5, identificada por
  `DICOFRE`/`DTMNFR`;
- troços de limite entre entidades administrativas, o oceano ou Espanha;
- relações entre troços, fontes e entidades administrativas.

**Documentado:** Na CAOP 2024, a nomenclatura dos campos mudou de `DI`, `DICO`
e `DICOFRE` para `DT`, `DTMN` e `DTMNFR`. A documentação consultada descreve
esta alteração como mudança de nomenclatura dos atributos, não como prova de
que os valores dos códigos tenham mudado nessa edição.

**Documentado:** A documentação cartográfica da DGT descreve `DT` com dois
dígitos, `DTMN` com quatro e `DTMNFR` com seis. A implementação do modelo atual
usa tipos textuais: até dois caracteres para distrito/ilha, quatro para
município, oito para entidade administrativa e três, quatro e cinco para NUTS
1, 2 e 3.

**Observado:** Na distribuição CAOP 2025, Porto surge como município `1312` e
Bonfim como freguesia `131202`. Os valores são strings nos schemas da OGC API.

**Decisão do PTScope:** Os identificadores serão preservados como
strings. Não devem ser convertidos para inteiro, preenchidos, truncados ou
decompostos sem uma regra oficial aplicável à versão e ao contexto.

### 5.2 Responsabilidade e estabilidade dos códigos

**Documentado:** A DGT declara que os códigos `DTMNFR` são criados pelo INE e
usados pela DGT na CAOP. Os metadados da CAOP 2025 repetem que a atribuição do
código único é da responsabilidade do INE.

**Documentado:** A CAOP 2024.1 incorporou a reposição e alteração de freguesias
determinada pelas Leis n.º 2/2025, n.º 3/2025 e n.º 25-A/2025. A DGT declara
que foram atribuídos novos códigos `DTMNFR` pelo INE, em conformidade com a 75.ª
deliberação da Secção Permanente de Coordenação Estatística.

**Limite da evidência:** A atribuição de novos códigos na CAOP 2024.1 demonstra
que pelo menos algumas alterações administrativas afetam identificadores. As
fontes consultadas não sustentam uma garantia geral de estabilidade dos códigos
através de fusões, reposições, desagregações ou alterações de limites.

**Inferência:** Para estudos longitudinais, apenas guardar o código corrente
pode impedir a reconstrução correta da geografia válida numa data passada. A
regra exata de versionamento fica por decidir depois de estudadas as tabelas de
correspondência oficiais.

### 5.3 Nomes

**Observado:** A OGC API publica nomes separados para município, freguesia,
distrito/ilha e regiões NUTS. Para freguesias, publica ainda
`designacao_simplificada`.

**Decisão do PTScope:** Igualdade de nome não será usada como igualdade de
entidade. Nomes e códigos serão conservados separadamente e associados à edição
observada.

## 6. Geometrias, áreas, CRS e precisão

### 6.1 Construção geométrica

**Documentado:** No modelo CAOP, uma entidade administrativa é construída a
partir do centroide e dos troços que delimitam a sua área. Uma entidade pode
ser constituída por áreas geograficamente descontínuas. Os troços podem separar
duas entidades, uma entidade e o oceano ou uma entidade e Espanha.

**Documentado:** A CAOP 2024 introduziu um modelo baseado em PostgreSQL/PostGIS
e alinhado com o modelo INSPIRE de Unidades Administrativas. As edições até
2023 seguiam um modelo baseado na norma ISO e no EuroBoundaryMap 3.0.

**Observado:** O elemento do município do Porto devolvido pela OGC API usa uma
geometria GeoJSON `MultiPolygon`, mesmo sendo um exemplo territorial simples.

**Decisão do PTScope:** Uma futura integração aceitará o tipo geométrico
publicado e não assumirá que municípios são sempre `Polygon`.

### 6.2 Sistemas de referência

**Documentado:** A implementação do modelo usa os seguintes CRS regionais:

| Cobertura | CRS documentado |
| --- | --- |
| Continente | PT-TM06/ETRS89, EPSG:3763 |
| Madeira | PTRA08-UTM/ITRF93, EPSG:5016 |
| Açores, grupo ocidental | PTRA08-UTM/ITRF93, EPSG:5014 |
| Açores, grupos central e oriental | PTRA08-UTM/ITRF93, EPSG:5015 |
| Sedes administrativas | ETRS89, EPSG:4258 |

**Documentado:** Os metadados RNDG da CAOP 2025 indicam EPSG:3763 e EPSG:4258
para o Continente; EPSG:5014, EPSG:5015, EPSG:5013 e EPSG:4326 para os Açores;
e EPSG:5016, EPSG:5013 e EPSG:4326 para a Madeira. A presença de vários CRS nos
metadados não confirma que todas as camadas ou formatos estejam disponíveis em
todos eles.

**Observado:** A coleção `municipios` da OGC API anuncia CRS84, EPSG:4326,
EPSG:3857, EPSG:4258 e EPSG:3763, com EPSG:3763 como CRS de armazenamento. O
pedido do Porto sem parâmetro `crs` devolveu `Content-Crs` correspondente a
CRS84.

**Decisão do PTScope:** O CRS efetivo será lido do recurso ou da resposta, não
deduzido apenas a partir da região.

### 6.3 Área e perímetro

**Documentado:** A tabela oficial de áreas CAOP 2025 declara que os valores
foram calculados diretamente da geodatabase, em PT-TM06/ETRS89 no Continente e
PTRA08-UTM/ITRF93 nas regiões autónomas. Explicita unidades de hectares e km²
para área, quilómetros para perímetro e metros para altitudes.

**Observado:** A tabela de municípios contém `area_ha`, `area_km2`,
`perim_km`, `altitude_max_m` e `altitude_min_m`. A OGC API expõe `area_ha` e
`perimetro_km`, mas não expõe `area_km2` na coleção `municipios`.

**Observado:** Para Porto, a tabela publica `4142.02` ha e `41.42` km². A
conversão do valor apresentado em hectares seria `41.4202` km²; portanto, o
campo em km² está publicado com menor precisão decimal.

**Decisão do PTScope:** Os campos oficiais e a precisão publicada serão
preservados. Um valor recalculado não substituirá o original, pois pode refletir
uma precisão ou regra de arredondamento diferente.

### 6.4 Escala e precisão posicional

**Documentado:** Os metadados RNDG indicam escala equivalente 1:25 000. A
linhagem enumera fontes em escalas que variam, conforme o caso, entre 1:1 000,
1:2 000, 1:2 500, 1:5 000 e 1:25 000, além de diplomas e procedimentos de
delimitação.

**Questão aberta:** Não foi encontrada nos recursos consultados uma medida
quantitativa única de exatidão posicional aplicável a todos os limites.

**Decisão do PTScope:** A escala de referência não será transformada numa
tolerância geométrica sem documentação que sustente essa conversão.

## 7. Formas oficiais de acesso

### 7.1 Página CAOP e downloads

**Documentado:** A página CAOP é o índice oficial para a edição corrente,
edições históricas, notas de alterações, GeoPackages e tabelas de áreas.

**Observado:** Em 2026-09-28, a edição 2025 era distribuída em GeoPackage ZIP
separado para Continente, Açores e Madeira. A tabela nacional de áreas e
perímetros estava disponível em:

- [Áreas de freguesia, município, distrito/ilha e país — CAOP 2025](https://www.dgterritorio.gov.pt/sites/default/files/ficheiros-cartografia/Areas_Freg_Mun_Dist_Pais_CAOP2025.zip)

**Observado:** Este ZIP contém um XLSX e um ZIP de CSV, incluindo tabelas de
freguesias, municípios e distritos/ilhas e notas metodológicas. Os CSV principais
foram lidos como UTF-8, mas o ficheiro de notas dentro do conjunto CSV estava em
ISO-8859-1.

**Decisão do PTScope:** A codificação será detetada ou configurada por ficheiro,
sem presumir uniformidade dentro do pacote.

### 7.2 Catálogo SNIG/RNDG

**Documentado:** O RNDG fornece descoberta e metadados; os registos apontam para
downloads e serviços mantidos pela DGT. Os metadados seguem perfis ISO/INSPIRE e
podem ser consultados por interface web, XML do GeoNetwork e CSW.

**Observado:** Os registos CAOP 2025 incluem ligações para WMS, GeoPackage e OGC
API. O catálogo é, portanto, uma camada de descoberta e proveniência, não uma
cópia necessária dos dados.

### 7.3 OGC API

**Documentado:** A DGT apresenta a OGC API como mecanismo oficial de acesso aos
seus conjuntos de dados e publica um manual de utilização.

**Observado:** A raiz `https://ogcapi.dgterritorio.gov.pt/?f=json` devolveu uma
landing page com ligações para `conformance`, `collections` e `openapi`. A
descrição OpenAPI observada usa OpenAPI 3.0.2 e identifica a implementação como
`pygeoapi` 0.23.4.

**Observado:** As coleções CAOP disponíveis eram:

| Coleção | Conteúdo observado |
| --- | --- |
| `distritos` | distritos do Continente |
| `municipios` | municípios do Continente |
| `freguesias` | freguesias do Continente |
| `admin` | unidades administrativas |
| `trocos` | troços de limites administrativos |
| `nuts1` | regiões NUTS 1 |
| `nuts2` | regiões NUTS 2 |
| `nuts3` | regiões NUTS 3 |

**Observado:** As descrições e extensões espaciais destas coleções referem o
Continente. Não foram observadas coleções CAOP específicas para Açores ou
Madeira nesta API. A CAOP nacional continua disponível para essas regiões por
GeoPackage e WMS próprios.

#### Contrato observado de `items`

**Observado:** O endpoint é:

```text
GET https://ogcapi.dgterritorio.gov.pt/collections/{collectionId}/items
```

A OpenAPI documenta os seguintes parâmetros relevantes:

| Parâmetro | Contrato observado/documentado na OpenAPI |
| --- | --- |
| `f` | `json`/GeoJSON por omissão; também `html`, `jsonld` e `csv` |
| `lang` | `pt-PT` ou `en-US` |
| `bbox` | filtro por caixa envolvente |
| `bbox-crs` | CRS da caixa envolvente |
| `crs` | CRS pretendido para a resposta |
| `limit` | omissão `100`, mínimo `1`, máximo `5000` |
| `offset` | omissão `0` |
| `properties` | seleção de propriedades |
| `skipGeometry` | omissão `false` |
| `sortby` | ordenação |
| atributos | filtros de igualdade específicos da coleção, como `dtmn=1312` |

**Observado:** Também existem endpoints de detalhe
`/items/{featureId}`, schema, queryables, mapas e tiles. Todos os pedidos `GET`
usados funcionaram sem credenciais. A OpenAPI não apresentou um requisito global
de segurança.

**Questão aberta:** Não foi encontrada documentação oficial de quota, rate
limit, SLA ou tamanho máximo de resposta além do limite de 5000 elementos por
pedido. A ausência de autenticação nos pedidos testados não garante ausência de
controlos operacionais futuros.

**Observado:** `limit=0` devolveu HTTP 400 em JSON, com código
`InvalidParameterValue`. Uma coleção inexistente devolveu HTTP 404 em JSON, com
código `NotFound`.

**Observado:** A declaração de conformidade anuncia partes de OGC API Features
relativas a criação, substituição e eliminação. Esta investigação não fez
pedidos de escrita.

**Limite da evidência:** Essa declaração, por si só, não demonstra que escrita
pública e anónima esteja autorizada.

**Decisão do PTScope:** O âmbito considerado neste estudo e numa eventual
integração é apenas de leitura por `GET`.

#### Schemas observados

**Observado:** `municipios` apresenta, entre outros:

| Campo | Tipo observado | Exemplo Porto |
| --- | --- | --- |
| `dtmn` | string; identificador | `1312` |
| `municipio` | string | `Porto` |
| `distrito_ilha` | string | `Porto` |
| `nuts3_cod` | string | `11A` |
| `nuts3` | string | `Área Metropolitana do Porto` |
| `nuts2` | string | `Norte` |
| `nuts1` | string | `Continente` |
| `area_ha` | number | `4142.02` |
| `perimetro_km` | integer no schema observado | `36` |
| `n_freguesias` | integer | `7` |
| `geometry` | geometria GeoJSON | `MultiPolygon` |

**Observado:** `freguesias` apresenta, entre outros, `dtmnfr`, `freguesia`,
`municipio`, `distrito_ilha`, `nuts3_cod`, nomes NUTS, `area_ha`,
`perimetro_km` e `designacao_simplificada`.

**Limitação observada:** O schema da API classifica `perimetro_km` como inteiro.
Este é o contrato publicado por esta representação; não demonstra que a medição
de origem tenha sido produzida sem casas decimais.

### 7.4 WMS

**Observado:** Foram confirmados serviços WMS 1.3.0 separados:

- [WMS CAOP Continente — GetCapabilities](https://geo2.dgterritorio.gov.pt/geoserver/caop_continente/wms?service=WMS&version=1.3.0&request=GetCapabilities)
- [WMS CAOP Açores — GetCapabilities](https://geo2.dgterritorio.gov.pt/geoserver/caop_raa/wms?service=WMS&version=1.3.0&request=GetCapabilities)
- [WMS CAOP Madeira — GetCapabilities](https://geo2.dgterritorio.gov.pt/geoserver/caop_ram/wms?service=WMS&version=1.3.0&request=GetCapabilities)

**Observado:** O WMS continental anuncia camadas de áreas administrativas,
distritos, municípios, freguesias, troços e NUTS 1, 2 e 3. O `GetCapabilities`
anuncia formatos de imagem como PNG, JPEG, GIF e TIFF, além de outros formatos
fornecidos pelo GeoServer.

**Limite da evidência:** Um formato anunciado pelo WMS é um formato de resposta
do serviço, não evidência de que exista um download vetorial oficial nesse
formato. Nesta investigação apenas foram testadas as capabilities, não cada
combinação de camada, estilo, CRS e formato.

**Questão aberta:** Não foi encontrada nos metadados atuais da CAOP uma ligação
específica para WFS. A existência de documentação geral de WFS na DGT não prova
que um serviço WFS atual da CAOP exista; não foi assumido.

### 7.5 Autenticação e limites

**Observado:** Downloads, metadados XML/CSW, OGC API e `GetCapabilities` WMS
responderam sem autenticação.

**Documentado:** Os metadados classificam o acesso como público e sem restrições
de acesso, sujeito às condições de licença.

**Questão aberta:** Não foram encontrados limites formais de frequência,
concorrência ou volume. A ausência de limites publicados não demonstra que não
existam controlos operacionais.

**Decisão do PTScope:** Esta descoberta não autoriza crawling ou downloads
indiscriminados; uma futura integração deverá usar pedidos limitados e
proporcionais.

## 8. Metadados, proveniência e licença por recurso

### 8.1 Registos regionais CAOP 2025

**Observado nos metadados RNDG:** Cada um dos três registos abaixo contém, ao
nível das restrições legais do conjunto identificado, `CC-BY-4.0` e exige o
mesmo texto de crédito quando informação geográfica propriedade da DGT seja
publicada ou divulgada, mesmo que parcialmente adaptada:

```text
Informação geográfica cedida pela Direção-Geral do Território
```

| Recurso identificado pelo registo | ID RNDG | Licença e atribuição no registo |
| --- | --- | --- |
| CAOP 2025 — Continente | [`198497815bf647ecaa990c34c42e932e`](https://snig.dgterritorio.gov.pt/rndg/srv/api/records/198497815bf647ecaa990c34c42e932e/formatters/xml) | `CC-BY-4.0`; texto de crédito acima |
| CAOP 2025 — Região Autónoma dos Açores | [`d9ca5eef-9860-4f5b-99a8-10661208d727`](https://snig.dgterritorio.gov.pt/rndg/srv/api/records/d9ca5eef-9860-4f5b-99a8-10661208d727/formatters/xml) | `CC-BY-4.0`; texto de crédito acima |
| CAOP 2025 — Região Autónoma da Madeira | [`78aef3be-0232-43ad-9dd5-fcdce15da03f`](https://snig.dgterritorio.gov.pt/rndg/srv/api/records/78aef3be-0232-43ad-9dd5-fcdce15da03f/formatters/xml) | `CC-BY-4.0`; texto de crédito acima |

**Observado:** Os mesmos registos identificam a DGT como ponto de contacto,
descrevem a linhagem, declaram frequência anual e data de publicação
2026-02-18, e ligam aos GeoPackages das respetivas coberturas. A página oficial
da CAOP atribui à DGT a execução e manutenção da carta; o papel ISO expresso
nestes três metadados é `pointOfContact`, não um papel codificado como
`originator` ou `owner`.

**Observado:** A data de atualização dos metadados consultados era 2026-07-02.
É uma data do registo, não necessariamente uma data de alteração do conteúdo
cartográfico.

### 8.2 OGC API

**Observado:** A secção `info.license` da [descrição OpenAPI do
serviço](https://ogcapi.dgterritorio.gov.pt/openapi?f=json) declara `CC-BY 4.0`
e liga a `https://creativecommons.org/licenses/by/4.0/`. A OpenAPI consultada
não contém o texto de crédito específico reproduzido nos três registos CAOP.

**Limite da evidência:** Esta declaração confirma a licença apresentada pelo
serviço OGC API, mas não esclarece sozinha se todas as coleções presentes ou
futuras têm exatamente as mesmas condições nem acrescenta uma regra de
atribuição específica por coleção.

### 8.3 WMS regionais

**Observado:** Os três `GetCapabilities` WMS consultados indicam ausência de
taxas e de restrições de acesso (`Fees`/`AccessConstraints` como `none`, `None`
ou `No conditions apply`). Não apresentam uma licença Creative Commons nem um
texto de atribuição no bloco de serviço.

**Limite da evidência:** Ausência de taxas ou restrições de acesso não equivale
a uma licença de reutilização. Para as camadas CAOP, a declaração explícita de
`CC-BY-4.0` e o crédito foram encontrados nos metadados regionais do conjunto,
não no `GetCapabilities` WMS.

### 8.4 Tabelas de áreas e ficheiros auxiliares

**Observado:** O ZIP das tabelas de áreas CAOP 2025 não contém um ficheiro de
licença autónomo. Não foi identificado um registo RNDG dedicado exclusivamente
a esse ZIP. A página geral de dados abertos da DGT menciona `CC BY 4.0`, mas a
investigação não confirmou uma declaração de licença incorporada ou específica
para este ficheiro auxiliar.

**Limite da evidência:** Não se propaga automaticamente para este ZIP a licença
de outro recurso apenas por estar ligado na mesma página CAOP. A condição exata
de reutilização das tabelas fica registada como questão aberta.

### 8.5 SNIG/RNDG e regra do PTScope

**Documentado:** O RNDG cataloga as condições de acesso e uso declaradas no
registo do recurso. A presença de um recurso no catálogo não identifica, por si
só, o SNIG como produtor.

**Decisão do PTScope:** A licença e a atribuição serão verificadas e guardadas
por recurso e edição. Uma política genérica do portal ou a licença de um dataset
relacionado não substituirá uma declaração específica do recurso consumido.

### 8.6 Informação de proveniência a conservar

**Decisão do PTScope:** Sem definir já um schema, uma futura ingestão deverá ser
capaz de conservar:

- entidade responsável pela execução e manutenção da CAOP: DGT;
- papel declarado nos metadados regionais consultados: DGT como
  `pointOfContact`;
- infraestrutura/catalogador: SNIG/RNDG;
- sistema/dataset: CAOP;
- edição completa e cobertura regional;
- identificador do registo de metadados;
- recurso, endpoint e parâmetros usados;
- identificador externo da entidade;
- CRS pedido e CRS devolvido;
- data de referência, publicação e atualização dos metadados;
- data e hora de extração;
- licença e texto de atribuição;
- diploma ou fonte de alteração, quando aplicável.

## 9. Exemplos reais minimizados

### 9.1 Porto na CAOP 2025

Pedido sem geometria:

```text
GET https://ogcapi.dgterritorio.gov.pt/collections/municipios/items
    ?f=json
    &dtmn=1312
    &skipGeometry=true
```

Resposta minimizada observada:

```json
{
  "numberMatched": 1,
  "numberReturned": 1,
  "features": [
    {
      "id": "1312",
      "properties": {
        "dtmn": "1312",
        "municipio": "Porto",
        "distrito_ilha": "Porto",
        "nuts3_cod": "11A",
        "nuts3": "Área Metropolitana do Porto",
        "nuts2": "Norte",
        "nuts1": "Continente",
        "area_ha": 4142.02,
        "perimetro_km": 36,
        "n_freguesias": 7
      }
    }
  ]
}
```

**Observado:** O identificador do elemento e o `dtmn` coincidem neste exemplo.
Isso não demonstra uma regra universal para todas as coleções.

**Observado:** O filtro das freguesias por município devolveu sete elementos.
Bonfim surgiu com `dtmnfr="131202"`, `area_ha=309.63` e
`perimetro_km=10`.

**Observado:** A soma dos `area_ha` publicados com duas casas decimais para as
sete freguesias do Porto foi `4142.01`, enquanto o município publica `4142.02`.

**Inferência:** A diferença de `0.01` ha é compatível com arredondamentos dos
valores apresentados, mas a causa não foi confirmada.

**Decisão do PTScope:** A diferença não será corrigida automaticamente.

### 9.2 Alteração administrativa: Pernes

**Documentado:** A Lei n.º 27/2025 alterou limites territoriais entre Pernes, a
União das Freguesias de São Vicente do Paul e Vale de Figueira e a União das
Freguesias de Achete, Azoia de Baixo e Póvoa de Santarém. O diploma contém a
descrição e coordenadas dos novos limites em ETRS89.

**Documentado:** A DGT identifica esta lei como uma das duas alterações
incorporadas na CAOP 2025.

**Observado:** Na CAOP 2025, Pernes aparece como:

```json
{
  "id": "141614",
  "dtmnfr": "141614",
  "freguesia": "Pernes",
  "municipio": "Santarém",
  "nuts3_cod": "1D3",
  "area_ha": 1589.07,
  "perimetro_km": 23
}
```

**Limite da evidência:** O caso demonstra que a edição e a data de referência
são necessárias para contextualizar uma geometria alterada. A manutenção do
código e do nome, por si só, não demonstra que a geometria seja igual entre
versões.

### 9.3 Alterações com novos códigos

**Documentado:** A nota CAOP 2024.1 relaciona a edição com a reposição de
freguesias em 2025 e indica que o INE atribuiu novos códigos `DTMNFR`. Aponta
para tabelas oficiais de correspondência do INE:

- [Correspondência estatística — recurso INE 9160](https://smi.ine.pt/Versao/Download/9160)
- [Correspondência estatística — recurso INE 10698](https://smi.ine.pt/Versao/Download/10698)

**Documentado:** No caso descrito pela CAOP 2024.1, as alterações administrativas
afetaram a organização territorial e implicaram a atribuição de novos códigos.

**Decisão do PTScope:** Geometria, designação, hierarquia ou identificador não
serão usados isoladamente para reconciliar versões.

## 10. Relação com GEO API PT e INE

### 10.1 Códigos

**Documentado no ecossistema DGT/INE:** A responsabilidade de atribuição de
`DTMNFR` é do INE; a DGT incorpora esses códigos na CAOP.

**Observado:** Na CAOP 2025, Porto usa `DTMN="1312"` e Bonfim usa
`DTMNFR="131202"`. A GEO API PT observada anteriormente usa os mesmos valores
para Porto e Bonfim e declara CAOP 2024.1 como fonte cartográfica.

**Observado:** No indicador INE anteriormente estudado sob NUTS 2013, Porto
aparece com o geocódigo composto `11A1312`. Na CAOP 2025, `dtmn="1312"` e
`nuts3_cod="11A"` são campos separados.

**Limite da evidência:** Para este exemplo, versão e classificação, é possível
relacionar os componentes publicados. Isto não autoriza uma regra genérica de
partição de códigos INE nem prova equivalência entre identificadores de sistemas
diferentes.

### 10.2 NUTS

**Documentado:** As notas da tabela CAOP 2025 dizem que a associação territorial
às NUTS segue o Regulamento Delegado (UE) 2023/674 e a Lei n.º 24-A/2022.

**Decisão do PTScope:** Uma correspondência CAOP–NUTS conservará a versão da
CAOP e a versão/classificação NUTS. O projeto não estabelecerá correspondências
apenas pela semelhança da designação ou do código.

### 10.3 Área do Porto

**Observado:** A CAOP 2025 publica para Porto `4142.02` ha, ou `41.42` km² na
tabela arredondada. A GEO API PT anteriormente observada, declarando CAOP
2024.1, publica `Area_T_ha=4145.6`, equivalente a `41.456` km².

**Observado:** Existe uma diferença de `3.58` ha entre valores ligados
a edições e canais distintos. Este estudo não determina se resulta de alteração
geométrica, processamento, edição da fonte ou outro fator.

**Decisão do PTScope:** Preservar valor, unidade, precisão, versão, recurso e
proveniência. Não escolher ainda CAOP, GEO API PT ou INE como autoridade para
área, população ou limites.

## 11. Nulos, campos ausentes e casos limite

**Observado:** Nos exemplos Porto, Bonfim e Pernes, os campos selecionados não
estavam nulos. Esta amostra pequena não permite concluir que sejam obrigatórios
em todo o país ou em todas as versões.

**Documentado:** A tabela de áreas contabiliza `3259` freguesias, `308`
municípios e `29` distritos/ilhas. A nota explica que o Corvo é contabilizado
como freguesia para efeitos estatísticos, apesar de legalmente não possuir
freguesia, nos termos do artigo 78.º da Lei n.º 9/87.

**Documentado:** O caso do Corvo é uma exceção explícita entre a contagem para
fins estatísticos e a existência jurídica de freguesia.

**Decisão do PTScope:** O projeto não imporá a regra “todo o município tem pelo
menos uma freguesia juridicamente constituída” sem representar o contexto da
fonte.

**Observado:** Os schemas da OGC API listam propriedades e tipos, mas as
respostas consultadas não forneceram uma garantia de não nulabilidade para cada
campo.

**Questão aberta:** Falta caracterizar, com amostra controlada e documentação
oficial, a ocorrência de `null`, strings vazias, geometrias inválidas ou
ausentes e entidades multipartes nas três regiões.

## 12. Atualizações e histórico

**Documentado:** A publicação CAOP é anual, podendo existir versões intercalares.
As notas de alterações associam edições a diplomas e períodos de vigência.

**Documentado:** O modelo interno descrito pela DGT inclui histórico de objetos,
com instante inicial, utilizador, motivo, tabelas de cópia e funções de consulta
temporal.

**Limite da evidência:** A documentação de histórico no modelo interno não
demonstra que esse histórico esteja exposto nos downloads ou serviços públicos.

**Observado:** A OGC API pública consultada expõe o estado corrente das coleções
CAOP e não apresentou, nos endpoints estudados, um parâmetro de edição ou data
para recuperar estados históricos.

**Observado:** Os downloads históricos permitem obter várias edições completas,
mas não constituem por si só um fluxo de alterações elemento a elemento.

**Questões abertas:**

- existe um identificador persistente de feição entre todas as edições, além do
  código administrativo sujeito a alterações?
- existe um changelog estruturado e completo, ou apenas notas e diplomas por
  edição?
- os GeoPackages mantêm datas de validade ou histórico interno não descrito na
  página de distribuição?
- como é comunicada uma correção a uma edição já publicada sem mudança do nome
  da versão?

## 13. Inconsistências e limitações observadas

### 13.1 Metadados RNDG

**Observado:** O campo `metadataStandardName` dos registos consultados refere
“ISO 19115 Sistema de Metadados dos Açores”, incluindo no registo do
Continente. Isto parece incompatível com a cobertura, mas a origem não foi
confirmada.

**Observado:** No registo continental, datas de etapas da linhagem aparecem como
2025-01-06, anteriores às Leis n.º 27/2025 e n.º 48/2025 que a CAOP 2025 declara
incorporar.

**Inferência:** As datas podem referir etapas diferentes ou resultar de erro de
metadados; a causa não foi confirmada.

**Decisão do PTScope:** Estes valores não serão usados isoladamente como data de
produção da edição.

**Observado:** Os metadados enumeram Shapefile, GeoPackage, imagens e OGC API
como formatos. A página atual de download da edição 2025 oferece GeoPackage;
imagens são também formatos de resposta WMS. Não foi confirmada uma descarga
Shapefile atual para cada cobertura.

**Observado:** Os metadados declaram que o conjunto não é conforme ao
Regulamento (UE) n.º 1089/2010 no resultado de conformidade INSPIRE, apesar de o
modelo atual se inspirar no tema INSPIRE de Unidades Administrativas. Alinhamento
do modelo e conformidade formal não são equivalentes.

### 13.2 OGC API

**Observado:** As coleções CAOP 2025 publicam uma extensão temporal entre
`2000-10-30T18:24:39Z` e `2007-10-30T08:57:29Z`, incompatível à primeira vista
com a edição 2025. Não foi encontrada explicação oficial.

**Decisão do PTScope:** Enquanto a semântica não for esclarecida, estes valores
não serão tratados como validade temporal da CAOP 2025.

**Observado:** Uma resposta com um único resultado incluiu uma ligação `next`
com `offset=1`, embora `numberMatched=1` e `numberReturned=1`.

**Decisão do PTScope:** Uma futura paginação não dependerá apenas da presença da
ligação para concluir que existem mais resultados.

**Observado:** Uma ligação canónica de coleção foi anunciada com tipo
`text/csv`, mas o URL apontava para a página HTML de metadados do SNIG. O tipo da
ligação e o recurso efetivo não eram coerentes.

**Observado:** A OGC API CAOP observada cobre o Continente, enquanto a CAOP como
dataset nacional inclui também Açores e Madeira por outros mecanismos.

### 13.3 Representação e precisão

**Observado:** A tabela CSV publica `area_km2` arredondada a duas casas, enquanto
`area_ha` permite uma conversão com quatro casas em km². A API não expõe o mesmo
conjunto de campos que a tabela.

**Observado:** A codificação de texto varia dentro do pacote das tabelas de
áreas.

**Limite da evidência:** Os recursos observados não partilham um contrato
tabular único. “CAOP 2025” identifica a edição, mas o contrato técnico depende
do recurso: GeoPackage, CSV/XLSX, OGC API, WMS ou metadados.

## 14. Relevância para o PTScope

**Avaliação do PTScope, não afirmação da fonte:** Os recursos observados parecem
adequados para suportar:

- referência espacial versionada para distritos/ilhas, municípios e
  freguesias;
- associação explícita entre códigos, nomes, hierarquia e geometria;
- cálculo ou validação de agregações territoriais, com o CRS e a edição
  preservados;
- contextualização de indicadores INE e dados GEO API PT sem presumir que as
  versões ou áreas coincidem;
- análise de alterações administrativas através de edições, diplomas e tabelas
  de correspondência;
- visualização por WMS e consulta seletiva por OGC API;
- rastreabilidade através dos metadados RNDG e da licença por recurso.

**Limite da evidência:** Os recursos CAOP estudados descrevem limites e unidades
administrativas. Não foram observados neles dados de população, atividade
económica ou contratação pública, nem uma declaração de autoridade sobre
conceitos produzidos por outras fontes.

**Decisão adiada:** Este estudo não determina qual fonte prevalece em áreas,
população, códigos compostos ou limites. Uma futura política do PTScope deverá
operar por conceito, edição, data de referência e finalidade, preservando
divergências e proveniência.

## 15. Questões abertas

1. Qual é o contrato exato das camadas e atributos dentro de cada GeoPackage
   2025, incluindo nulabilidade, constraints, índices e metadados embebidos?
2. Existem serviços públicos equivalentes à OGC API para Açores e Madeira que
   não estejam ligados nos registos consultados?
3. Existe atualmente um WFS oficial da CAOP, ou foi substituído por OGC API e
   downloads GeoPackage?
4. Que garantias de estabilidade são dadas aos identificadores de elemento da
   OGC API e aos URLs `/items/{featureId}` entre edições?
5. Como são publicadas correções dentro da mesma edição e como pode um consumidor
   detetar alterações sem voltar a descarregar o recurso?
6. As datas temporais anómalas da OGC API têm algum significado interno ou são
   metadados incorretos?
7. Porque refere o standard de metadados dos Açores no registo continental?
8. Qual é a medida de qualidade posicional por troço ou fonte, quando existe, e
   é disponibilizada publicamente?
9. Como devem ser interpretados os campos inteiros de perímetro da OGC API face
   a medições potencialmente mais precisas no GeoPackage?
10. Que relações formais existem entre identificadores CAOP, códigos do Sistema
    de Metainformação do INE e geocódigos compostos de cada versão NUTS?
11. Como devem ser representadas, sem perda, exceções como o Corvo e entidades
    com áreas descontínuas?
12. Quais são as condições específicas de reutilização das tabelas de áreas e
    dos restantes ficheiros auxiliares sem licença incorporada ou metadado
    dedicado?
13. Que licença se aplica à documentação do modelo e ao código do repositório
    GitHub quando esses recursos não contêm uma licença própria explícita?

## 16. Síntese do contrato observável

**Documentado:** A DGT executa e mantém a CAOP; o SNIG/RNDG cataloga e dá acesso;
o INE atribui códigos `DTMNFR`; a Assembleia da República determina alterações
de limites por diploma. Estes papéis são relacionados, mas não intercambiáveis.

**Observado:** A edição 2025 é distribuída por três GeoPackages regionais,
tabelas nacionais de áreas, WMS regionais e uma OGC API que, nas coleções CAOP
observadas, cobre o Continente. Os metadados RNDG fornecem linhagem, datas,
ligações e CRS. Cada um dos três registos regionais declara `CC-BY-4.0` e o
texto de crédito da DGT; outros recursos apresentam declarações menos
específicas, descritas na secção 8.

**Documentado e observado:** Edições diferentes podem refletir alterações
administrativas, incluindo novos códigos, e os campos e a precisão observados
não são idênticos entre CSV e OGC API. Não foi demonstrado um contrato único
para todos os formatos.

**Decisão do PTScope para uma integração futura:** preservar identificadores
como strings; guardar edição, cobertura, CRS, unidade, precisão, recurso e
proveniência; não reconciliar automaticamente valores divergentes; e tratar
metadados inconsistentes como questões de qualidade, não como factos a
normalizar.
