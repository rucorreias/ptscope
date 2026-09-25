# GEO API PT: descoberta de dados

As decisões de arquitetura e ingestão derivadas desta investigação são mantidas em:
docs/architecture/data-ingestion.md

> Data da análise: 25 de setembro de 2026.
> Âmbito: descoberta e avaliação da fonte. Este documento não define ainda o
> modelo de dados do PTScope nem uma estratégia de persistência.

Ao longo do documento são usados três qualificadores:

- **Documentado**: consta da documentação ou página oficial da GEO API PT.
- **Observado**: foi confirmado numa resposta real da API na data acima.
- **Inferência**: conclusão plausível, mas não declarada pelo fornecedor.

## 1. Visão geral da fonte

A [GEO API PT](https://geoapi.pt/) agrega dados territoriais de Portugal
continental e das Regiões Autónomas. A página oficial indica como domínios de
informação as divisões administrativas, georreferenciação, censos, códigos
postais, altimetria, uso e ocupação do solo, perigo de incêndio, perigo de
inundação e clima.

A API JSON usa como base `https://json.geoapi.pt`. A
[documentação oficial](https://geoapi.pt/docs/) é gerada com ReDoc e contém uma
especificação OpenAPI `3.0.1`, identificada como versão `1.0`. A especificação
está embebida na página; não foi encontrado um URL público estável para a
descarregar separadamente.

Fontes principais consultadas:

- [Página oficial da GEO API PT](https://geoapi.pt/)
- [Documentação/OpenAPI da API JSON](https://geoapi.pt/docs/)
- [Pedido de chave para acesso alargado](https://geoapi.pt/request-api-key)
- [Dados abertos da Direção-Geral do Território](https://www.dgterritorio.gov.pt/dados-abertos)
- [Catálogo de entidades da CAOP](https://www.dgterritorio.gov.pt/sites/default/files/ficheiros-cartografia/catalogo_entidades_CAOP2023.pdf)

Foram efetuados poucos pedidos `GET`, sem automatização ou varrimento: listagem
de municípios, pesquisa por código, detalhe de Porto, Lisboa e Oliveira de
Azeméis, freguesias do Porto e dois casos de erro.

## 2. Autenticação e limites

| Tema | Resultado |
|---|---|
| Autenticação para uso público | **Documentado e observado:** não é obrigatória. Os pedidos de análise funcionaram sem chave. |
| Chave de API | **Documentado:** opcional para acesso alargado. |
| Envio da chave | Query parameter `key` ou cabeçalho `X-API-Key`. |
| Limite com subscrição | **Documentado:** até 10 000 pedidos por dia na página de pedido de chave. |
| Limite público atual | **Não documentado** nas páginas oficiais atuais consultadas. |
| Cabeçalhos de rate limit | **Observado:** não foram enviados `RateLimit-*`, `X-RateLimit-*` nem `Retry-After` nas respostas testadas. |

A OpenAPI aplica globalmente os esquemas `ApiKeyAuthInHeader` e
`ApiKeyAuthInQuery`, o que sugere autenticação obrigatória. Isto contradiz a
página oficial, que afirma explicitamente que a API JSON é gratuita e não
requer autenticação, e contradiz os pedidos reais sem chave. Para integração,
deve considerar-se a chave opcional até confirmação do fornecedor.

## 3. Endpoints relevantes

| Endpoint | Estado | Comportamento documentado/observado |
|---|---|---|
| `GET /municipios` | Atual | Sem filtros devolve um array alfabético de nomes. **Observado:** 308 nomes. Com filtros pode devolver um município. |
| `GET /municipios?codigoine=1312` | Atual | **Observado:** devolveu o objeto do Porto com HTTP 200. |
| `GET /municipio/{municipio}` | Atual e recomendado | Detalhe do município, incluindo administração, geometria, freguesias, censos e, quando disponível, altimetria. |
| `GET /municipios/{municipio}` | Descontinuado | Alias antigo; usar `/municipio/{municipio}`. |
| `GET /municipio/{municipio}/freguesias` | Atual e recomendado | Lista de nomes, código do município, geometria municipal e Features das freguesias. |
| `GET /municipios/{municipio}/freguesias` | Descontinuado | Usar a variante singular `/municipio/...`. |
| `GET /municipio/{municipio}/altimetria` | Atual | Altimetria municipal e URL de GeoTIFF quando disponível. |
| `GET /municipio/{municipio}/freguesia/{freguesia}` | Atual e recomendado | Detalhe de uma freguesia dentro do município. |
| `GET /municipio/{municipio}/freguesias/{freguesia}` | Descontinuado | Usar `/municipio/{municipio}/freguesia/{freguesia}`. |
| `GET /distrito/{distrito}/municipios` | Atual e recomendado | Municípios do distrito. |
| `GET /distritos/{distrito}/municipios` | Descontinuado | Usar `/distrito/...` no singular. |
| `GET /codigo_postal/{cp}` | Atual e recomendado | Detalhe de CP4 ou CP7. |
| `GET /cp/{cp}` | Descontinuado | Usar `/codigo_postal/{cp}`. |

Filtros documentados para `/municipios`: `nome`, `codigo`, `nif`,
`codigopostal`, `email`, `telefone`, `fax`, `sitio` e `codigoine`. O parâmetro
`json` não é necessário quando se usa `json.geoapi.pt`.

Respostas reais consultadas: [municípios](https://json.geoapi.pt/municipios),
[Porto](https://json.geoapi.pt/municipio/porto),
[Lisboa](https://json.geoapi.pt/municipio/lisboa),
[Oliveira de Azeméis](https://json.geoapi.pt/municipio/Oliveira%20de%20Azem%C3%A9is)
e [freguesias do Porto](https://json.geoapi.pt/municipio/porto/freguesias).

Nota de contrato: a OpenAPI está parcialmente desatualizada. O schema de
município documenta, por exemplo, `codigo`, `rua`, `localidade`, `descrpostal`,
`populacao`, `eleitores` e `fax`, mas estes campos não apareceram nas três
respostas atuais. Em sentido inverso, as respostas incluem `dtmn`,
`distrito_ilha`, `Distrito`, `morada`, `geojson` e `altitude`, ausentes ou
incompletos nesse schema.

## 4. Estrutura administrativa observada

A hierarquia útil para o PTScope é:

`distrito/ilha -> município -> freguesia -> secção estatística -> subsecção estatística`

Nos exemplos do Continente, `distrito`, `distrito_ilha` e `Distrito` têm o
mesmo valor. A existência de `distrito_ilha` indica que o fornecedor usa um
campo comum para distrito ou ilha; o comportamento nas Regiões Autónomas não
foi testado nesta análise.

| Elemento | Campo(s) observado(s) | Forma |
|---|---|---|
| Município | `dtmn`, `codigoine`, `geojson.properties.Dicofre` | String com 4 caracteres: Porto `1312`, Lisboa `1106`, Oliveira de Azeméis `0113`. |
| Freguesia | `dtmnfr`, `codigoine`, `Dicofre`, `DICOFRE` | String com 6 caracteres: Bonfim `131202`. |
| Distrito/ilha | `distrito`, `distrito_ilha`, `Distrito` | Nome textual, com duplicação e variação de capitalização da chave. |
| NIF | `nif` | String de 9 caracteres associada ao município/câmara, não um código territorial. |
| Relação pai-filho | `municipio`, `Concelho`, `distrito_ilha`, `Distrito` | Nomes repetidos na Feature da freguesia; o prefixo de `dtmnfr` coincide com `dtmn` nos exemplos. |

**Documentado/observado:** a própria interface da GEO API PT apresenta `dtmn`,
`dtmnfr`, `Dicofre` e `codigoine` como “Código INE”. O catálogo CAOP descreve
`DTMN` como identificador do município e `DICOFRE` como identificador da
freguesia. Por isso, estes valores devem ser tratados como códigos externos e
como strings, preservando zeros à esquerda. Não devem ser preenchidos para sete
dígitos.

**Candidatos a identificadores externos estáveis:** `dtmn` para município e
`dtmnfr`/`DICOFRE` para freguesia, sempre acompanhados pela versão da CAOP ou
data de referência. A estabilidade entre reorganizações administrativas não
foi demonstrada. O campo numérico `id` das freguesias não está documentado e
não deve ser assumido como estável. Não é tomada aqui qualquer decisão sobre
chaves primárias internas.

## 5. Resposta real de `/municipio/porto`

Projeção reduzida da resposta real. Foram omitidas coordenadas e a maioria dos
indicadores censitários, sem alterar os valores apresentados:

```json
{
  "codigoine": "1312",
  "dtmn": "1312",
  "nome": "Porto",
  "distrito_ilha": "Porto",
  "distrito": "Porto",
  "Distrito": "Porto",
  "nif": "501306099",
  "areaha": "41.29",
  "email": "geral@cm-porto.pt",
  "telefone": 222097000,
  "sitio": "www.cm-porto.pt",
  "morada": "Praça General Humberto Delgado",
  "codigopostal": "4049-001",
  "geojson": {
    "type": "Feature",
    "properties": {
      "Area_T_ha": 4145.6,
      "Area_EA_ha": 4145.6,
      "Dicofre": "1312",
      "Concelho": "Porto",
      "Distrito": "Porto"
    },
    "geometry": {
      "type": "Polygon"
    },
    "bbox": [-8.6912941, 41.1383507, -8.5526135, 41.1859353]
  },
  "altitude": {
    "url_geotiff": "http://json.geoapi.pt/geotiff/municipalities/1312.tif",
    "altitude_maxima": 163,
    "altitude_minima": 0,
    "diferencial_de_altitude": 163
  },
  "censos2011": {
    "N_INDIVIDUOS_RESIDENT": 237591
  },
  "censos2021": {
    "N_INDIVIDUOS": 231800
  }
}
```

Campos relevantes observados:

| Campo | Tipo real | Interpretação/nota |
|---|---|---|
| `codigoine` | string | Código municipal de 4 caracteres; duplica `dtmn` nos três exemplos. |
| `dtmn` | string | Código CAOP/administrativo do município. |
| `nome` | string | Nome canónico apresentado pela API. |
| `distrito_ilha` | string | Distrito ou ilha do município. |
| `distrito` | string | Nome do distrito; duplicado por `Distrito` no Continente. |
| `Distrito` | string | Duplicação com capitalização diferente. |
| `nif` | string | NIF da entidade municipal. Proveniência específica não documentada. |
| `areaha` | string | Campo de área com unidade contraditória; ver secção 8. |
| `email` | string | Contacto municipal. |
| `telefone` | number | Contacto municipal; modelar como texto seria mais robusto. |
| `sitio` | string | Website, sem esquema `https://` no exemplo. |
| `morada` | string | Morada institucional. |
| `codigopostal` | string | Código postal da morada institucional, não cobertura postal do território. |
| `geojson` | object | Feature GeoJSON municipal, com `properties`, `geometry` e `bbox`. |
| `geojson.properties.Area_T_ha` | number | Área total em hectares, de acordo com o nome e a interface. |
| `geojson.properties.Area_EA_ha` | number | Segunda medida de área em hectares; expansão da sigla não documentada. |
| `geojson.properties.centros` | object | Cinco pares de coordenadas: `centro`, `centroide`, `centroDeMassa`, `centroMedio` e `centroMediano`. |
| `geojson.properties.Dicofre` | string | Código municipal de 4 caracteres no contexto desta Feature. |
| `geojson.geometry` | object | Limite administrativo; `Polygon` no exemplo. |
| `geojson.bbox` | array[number] | `[minLon, minLat, maxLon, maxLat]` por observação dos valores. |
| `altitude` | object | GeoTIFF, mínimo, máximo e diferencial; campo opcional na prática. |
| `geojsons.municipio` | object | **Observado:** igual a `geojson` nos três municípios. |
| `geojsons.freguesias` | array[object] | Features das freguesias; 7 no Porto. |
| `censos2011` | object | 121 indicadores na resposta do Porto. |
| `censos2021` | object | 32 indicadores na resposta do Porto. |

As Features de freguesia acrescentam `id`, `dtmnfr`, `freguesia`,
`tipo_area_administrativa`, `municipio`, `distrito_ilha`, `nuts1`, `nuts2`,
`nuts3`, `area_ha`, `perimetro_km`, vários aliases de nome/código e `centros`.

## 6. Outros dados disponíveis

| Grupo | Disponibilidade | Onde/observação |
|---|---|---|
| População | Sim | `censos2011.N_INDIVIDUOS_RESIDENT` e `censos2021.N_INDIVIDUOS`. O campo genérico `populacao` da OpenAPI não apareceu nas respostas atuais. |
| Censos | Sim | Objetos separados para 2011 e 2021, com métricas e nomenclaturas diferentes. |
| Área | Sim, mas ambígua | `areaha`, `Area_T_ha`, `Area_EA_ha` e `area_ha` nas freguesias. |
| Freguesias | Sim | Incluídas em `geojsons.freguesias` e no endpoint dedicado. |
| Geometria administrativa | Sim | Feature GeoJSON para município e Features para freguesias. |
| Centróides/centros | Sim | Cinco variantes em `properties.centros`; métodos exatos não documentados. |
| Códigos postais | Sim | Código da morada municipal no detalhe e endpoints próprios para CP4/CP7. |
| Altimetria | Parcial | Objeto `altitude`, endpoint dedicado e GeoTIFF; ausente em Oliveira de Azeméis no teste. |
| Uso e ocupação do solo | Sim, noutra consulta | Documentado nos endpoints GPS/georreferenciação, não no detalhe municipal testado. |
| Perigo de incêndio | Sim, noutra consulta | Documentado nos endpoints GPS, não no detalhe municipal testado. |
| Perigo de inundação | Sim, noutra consulta | Documentado nos endpoints GPS, não no detalhe municipal testado. |
| Clima | Sim, noutra consulta | Documentado nos endpoints GPS, com data/hora, temperatura, humidade e pressão. Não é uma série municipal. |

## 7. Geometria e representação espacial

- **Formato:** Features compatíveis com GeoJSON, com `type`, `properties`,
  `geometry` e `bbox`. `geojsons.freguesias` é um array de Features, não um
  `FeatureCollection`.
- **Tipo observado:** `Polygon` para os três municípios e para todas as suas 44
  freguesias combinadas. A OpenAPI também exemplifica apenas `Polygon`.
- **MultiPolygon:** **Não documentado e não observado** nesta amostra. O
  consumidor não deve, contudo, assumir que nunca ocorrerá sem testar todo o
  universo ou obter confirmação do fornecedor.
- **CRS:** não existe membro `crs` e a documentação não declara um EPSG.
  **Inferência:** a ordem e os valores são longitude/latitude e são compatíveis
  com WGS 84, mas `EPSG:4326` não foi confirmado pelo fornecedor.
- **Bounding box:** quatro números, observacionalmente na ordem
  `[min longitude, min latitude, max longitude, max latitude]`.
- **Centros:** são arrays `[longitude, latitude]`. A API não explica o algoritmo
  ou significado exato de cada uma das cinco variantes.
- **Precisão:** as coordenadas de limites apresentam cerca de sete casas
  decimais; alguns centros calculados têm mais de 14. Isto não equivale a
  precisão posicional garantida.
- **Fonte dos limites:** **Documentado:** Carta Administrativa Oficial de
  Portugal 2024.1, da DGT.

## 8. Área territorial

Existem campos incompatíveis que não devem ser normalizados sem decisão
explícita:

| Município | `areaha` | `Area_T_ha` | `Area_T_ha / 100` |
|---|---:|---:|---:|
| Porto | `41.29` | 4 145,6 | 41,456 km² |
| Lisboa | `84.92` | 10 018,2 | 100,182 km² |
| Oliveira de Azeméis | `161.1` | 16 125,9 | 161,259 km² |

- A interface e o nome `areaha` identificam hectares, mas os valores observados
  têm magnitude compatível com km² para Porto e Oliveira de Azeméis. Isto é uma
  contradição, não uma unidade confirmada.
- `Area_T_ha` e `Area_EA_ha` são numéricos e explicitam hectares. Nos três
  municípios têm o mesmo valor.
- A conversão matemática é `km² = hectares / 100`.
- Lisboa apresenta uma diferença de 15,262 km² entre `areaha` e
  `Area_T_ha / 100`, muito superior a arredondamento. A causa não está
  documentada.

Recomendação de descoberta: considerar `Area_T_ha` a candidata mais explícita,
mas manter o valor e nome de origem e não promover nenhum campo a área oficial
do PTScope até esclarecer definição, fonte e data de referência.

## 9. Dimensão temporal

| Grupo | Referência temporal conhecida | Cadência/atualização |
|---|---|---|
| Limites administrativos | CAOP 2024.1 | A página identifica a versão, mas a API não expõe `valid_from`, `valid_to` ou histórico. Cadência não documentada. |
| Códigos postais | Atualizados em julho de 2025 | Periodicidade futura não documentada. |
| Censos | 2011 e 2021 | Coexistem no mesmo objeto municipal. São snapshots decenais, com conjuntos de campos diferentes. |
| Altimetria | Sem data no payload | Fonte estática ESA/Copernicus; edição do modelo não documentada na resposta. |
| Contactos municipais | Sem data no payload | Data de recolha e cadência não documentadas. |
| Clima | Data e hora de medição no payload GPS | Frequência, atraso e retenção não documentados. |
| Riscos e uso do solo | Sem versão no payload analisado | A página liga às fontes, mas não declara a edição usada pela API. |

Não existe no detalhe municipal um carimbo de atualização global nem metadados
por campo. Um futuro modelo temporal deve manter `ano_referencia`, versão da
fonte e data de ingestão separadamente, em vez de tratar toda a resposta como
se tivesse a mesma atualidade.

## 10. Proveniência

A GEO API PT é um agregador/distribuidor. As entidades abaixo são as fontes
originais declaradas na [página oficial](https://geoapi.pt/); a GEO API PT é o
fornecedor técnico da resposta consumida pelo PTScope.

| Grupo | Fonte original declarada | Observação |
|---|---|---|
| Limites e estrutura administrativa | DGT, CAOP 2024.1 | Inclui município, freguesia, códigos administrativos e geometria. |
| Altimetria | ESA/Copernicus Digital Elevation Model | Resposta municipal contém extremos e URL de GeoTIFF quando disponível. |
| Códigos postais | CTT e INE | Página indica atualização em julho de 2025. |
| Censos 2011 e 2021 | INE | A API agrega as métricas por unidade administrativa. |
| Uso e ocupação do solo | DGT, sistema SMOS/COS | Disponível por localização GPS. Edição concreta usada não documentada. |
| Perigo de incêndio rural | DGT | Disponível por localização GPS. Edição concreta usada não documentada. |
| Perigo de inundação | Agência Portuguesa do Ambiente | Disponível por localização GPS. Edição concreta usada não documentada. |
| Clima | IPMA | Medições expostas por localização GPS. |
| NIF, contactos e morada municipal | **Não documentado** | A OpenAPI e a página oficial não identificam a origem destes campos. |
| `bbox` e variantes de centro | **Não documentado** | **Inferência:** podem ser derivados pela GEO API PT durante o processamento da geometria. |

Para auditoria futura, PTScope deverá registar tanto `provider=GEO API PT` como
a fonte original declarada, sem apresentar a GEO API PT como autora dos dados
oficiais subjacentes.

## 11. Nulos, ausências e inconsistências

| Observação | Porto | Lisboa | Oliveira de Azeméis |
|---|---:|---:|---:|
| Código municipal | `1312` | `1106` | `0113` |
| Freguesias | 7 | 24 | 13 |
| População 2011 | 237 591 | 547 733 | 68 611 |
| População 2021 | 231 800 | 545 796 | 66 175 |
| Altimetria | Presente | Presente | Ausente |
| Tipo de geometria | Polygon | Polygon | Polygon |
| `geojson == geojsons.municipio` | Sim | Sim | Sim |

Conclusões da comparação:

- Não foram encontrados valores JSON `null` nos três payloads. A API omite o
  campo `altitude` em Oliveira de Azeméis, em vez de o devolver com `null`.
- Os códigos são strings e os zeros à esquerda são significativos.
- `codigoine`, `dtmn` e `Dicofre` duplicam o código municipal; nas freguesias,
  `dtmnfr`, `codigoine`, `Dicofre` e `DICOFRE` duplicam o código de 6 caracteres.
- `distrito`, `Distrito` e `distrito_ilha` são duplicações sem normalização de
  nomes de chave.
- `geojson` duplica integralmente `geojsons.municipio` nos três casos.
- O número de indicadores difere por edição censitária: 121 em 2011 e 32 em
  2021 para cada amostra. Não são schemas equivalentes.
- O schema OpenAPI não acompanha integralmente os payloads reais, incluindo
  nomes e presença de campos.
- O parâmetro com acentos `Oliveira de Azeméis`, devidamente codificado no URL,
  foi resolvido com sucesso.

## 12. Comportamento HTTP e erros

| Caso testado | Resultado |
|---|---|
| `GET /municipio/porto` | HTTP 200, `application/json; charset=utf-8`. |
| `GET /municipio/municipio-que-nao-existe-ptscope` | HTTP 404, `{"erro":"Município não encontrado!"}`. |
| `GET /municipios?codigoine=abc` | HTTP 404, a mesma mensagem de município não encontrado. |
| `GET /municipios?codigoine=1312` | HTTP 200, objeto do Porto. |

A OpenAPI declara `codigoine` como inteiro, mas a implementação não devolveu
HTTP 400/422 para texto inválido; tratou-o como pesquisa sem resultado. A
OpenAPI também descreve a resposta 404 como string, enquanto o payload real é
um objeto com a chave `erro`.

Timeouts, respostas 429, indisponibilidade, 5xx e políticas de retry não foram
forçados, para evitar carga ou perturbação do serviço. Não há garantias de SLA
documentadas na API; existe apenas uma página pública de uptime ligada pelo
fornecedor.

## 13. Licença e condições de uso

- A metadata OpenAPI declara **GNU General Public License v3.0**. O link de
  licença publicado (`github.com/jfoclpf/geoapi.pt/...`) devolvia HTTP 404 na
  data da análise.
- A página oficial declara que a API JSON é gratuita e não requer autenticação.
  Gratuidade de acesso não equivale, por si só, a licença de redistribuição dos
  dados.
- Não foi encontrada na documentação consultada uma licença única e explícita
  para o conjunto agregado de dados, nem termos específicos de reutilização,
  caching, redistribuição ou uso comercial.
- Não foram encontrados requisitos consolidados de atribuição. Cada fonte
  original pode ter condições próprias.
- A GPL é uma licença de software. Sem declaração adicional, não se deve inferir
  que cobre automaticamente CAOP, censos, códigos postais, modelos de elevação,
  clima ou cartas de risco agregados pela API.

Antes de publicar snapshots ou redistribuir dados no PTScope, é necessário
confirmar as licenças e atribuições das fontes originais e esclarecer com o
fornecedor a licença do payload agregado.

## 14. Implicações para o futuro modelo do PTScope

- Separar identidade territorial, atributos correntes, observações temporais e
  geometria. Os censos não devem ser colunas “atuais” do município.
- Guardar códigos administrativos como strings e preservar zeros à esquerda.
- Manter código, versão CAOP e fonte juntos; alterações administrativas podem
  quebrar a continuidade de nomes ou códigos.
- Representar campos opcionais como tal. Ausência e `null` devem ser tratados
  como estados distintos quando relevante.
- Não usar `nif`, nome ou `id` interno da Feature como identidade territorial.
- Não normalizar `areaha` até a unidade e a discrepância com `Area_T_ha` serem
  esclarecidas.
- Tratar métricas de 2011 e 2021 como catálogos diferentes ligados a ano,
  definição e fonte.
- Aceitar `Polygon` e `MultiPolygon` no desenho futuro, mesmo que apenas
  `Polygon` tenha sido observado.
- Guardar payload bruto ou hash, data de ingestão e versão do adaptador para
  permitir auditoria e reprocessamento.
- Evitar devolver geometrias completas em todas as respostas públicas por
  defeito; os payloads são volumosos.

Estas são implicações de modelação, não uma proposta final de tabelas ou ERD.

## 15. Campos candidatos

### Core agora

| Campo lógico | Origem candidata | Nota |
|---|---|---|
| Nome do município | `nome` | Manter também o valor bruto recebido. |
| Código administrativo municipal | `dtmn`/`codigoine` | String de 4 caracteres; validar igualdade enquanto ambos existirem. |
| Distrito/ilha | `distrito_ilha` | Mais abrangente do que `distrito`, mas requer teste nas Regiões Autónomas. |
| Fonte e versão | GEO API PT + CAOP 2024.1 | Metadado essencial de proveniência. |

### Úteis mais tarde

| Grupo | Campos |
|---|---|
| Hierarquia detalhada | Freguesias, `dtmnfr`, NUTS 1/2/3, secções e subsecções. |
| Geometria | `geometry`, `bbox`, centro selecionado e versão CAOP. |
| Demografia | Indicador, valor, ano 2011/2021, unidade e definição. |
| Área | `Area_T_ha`, `Area_EA_ha`, área de freguesia e método/fonte. |
| Altimetria | Mínimo, máximo, diferencial e referência ao raster. |
| Contactos | NIF, email, telefone, website, morada e código postal. |
| Outros temas | Códigos postais, uso do solo, incêndio, inundação e clima, cada um com temporalidade e licença próprias. |

### Ignorar por agora

- Aliases duplicados apenas por capitalização: `Distrito`, `DICOFRE`,
  `Freguesia`, `Concelho`.
- `id` numérico da Feature de freguesia, por não estar documentado como estável.
- Todas as cinco variantes de centro em simultâneo, até existir um caso de uso
  e definição formal.
- `areaha`, enquanto unidade e significado permanecerem contraditórios.
- Campos de contacto como parte do núcleo territorial; mudam de forma
  independente da geografia.

## 16. Questões em aberto

1. Qual é a unidade e definição exatas de `areaha`, e por que diverge tanto de
   `Area_T_ha` em Lisboa?
2. O que distingue formalmente `Area_T_ha` de `Area_EA_ha`?
3. Qual é o CRS declarado e podem surgir geometrias `MultiPolygon`?
4. Os códigos `dtmn` e `dtmnfr` são garantidos como estáveis dentro de cada
   versão CAOP? Como são representadas fusões e desagregações?
5. Qual é o limite público atual, a janela de rate limit e a resposta 429?
6. Qual é a licença dos payloads agregados e quais são as atribuições
   obrigatórias por fonte?
7. Existe uma especificação OpenAPI descarregável e versionada fora do HTML?
8. Qual é a política de compatibilidade e versionamento dos endpoints?
9. Qual é a origem e data de atualização de NIF, contactos e moradas?
10. Por que falta altimetria em Oliveira de Azeméis e qual é a cobertura total?
11. Como são calculadas as cinco variantes de centro e os `bbox`?
12. Que edições exatas dos datasets de altimetria, uso do solo e riscos são
    usadas?
13. Existe um dicionário oficial e versionado para todos os indicadores dos
    Censos 2011 e 2021 expostos pela API?
14. A discrepância entre OpenAPI e payload real é transitória ou deve ser
    considerada comportamento normal?

## 17. Recomendações

1. Consumir apenas os endpoints atuais no singular e encapsular a GEO API PT
   num adaptador próprio.
2. Criar testes de contrato com Porto, Lisboa e Oliveira de Azeméis, cobrindo
   zeros à esquerda, campos ausentes, áreas divergentes e geometrias.
3. Preservar respostas brutas e metadados de proveniência antes de normalizar.
4. Não tratar `codigoine` municipal como código de sete dígitos; usar a string
   de 4 caracteres fornecida e validar freguesias separadamente com 6.
5. Adiar a escolha de área oficial, CRS, licença de redistribuição e política
   de atualização até obter confirmação documental.
6. Modelar censos e restantes temas como dados temporais e provenientes de
   fontes específicas, não como propriedades permanentes do município.
