# INE Portugal: descoberta de dados

As decisões de arquitetura e ingestão derivadas desta investigação são mantidas em:
docs/architecture/data-ingestion.md

> Data da análise: 25 de setembro de 2026.
> Âmbito: descoberta e avaliação da fonte estatística. Este documento não
> implementa a integração, não define ainda o esquema final da base de dados e
> não autoriza a normalização automática de valores cuja semântica não esteja
> confirmada.

Ao longo do documento são usados três qualificadores:

- **Documentado**: consta de uma página, publicação ou metainformação oficial
  do Instituto Nacional de Estatística (INE), do Sistema de Metainformação
  (SMI), da Direção-Geral do Território ou do Eurostat.
- **Observado**: foi confirmado numa resposta concreta da API ou numa página
  oficial consultada na data acima. Quando a observação provém de um exemplo
  histórico ou de uma fonte secundária, isso é indicado expressamente.
- **Inferência**: conclusão técnica plausível, mas não declarada de forma
  inequívoca pelo fornecedor.

As designações e os códigos devem ser preservados como publicados. Em
particular, um código territorial não deve ser preenchido, truncado ou
convertido num inteiro sem conhecer a classificação e a versão a que pertence.

## 1. Fontes consultadas

Fontes oficiais principais:

- [Portal do INE](https://www.ine.pt/)
- [Base de Dados do INE](https://www.ine.pt/xportal/xmain?xpgid=ine_indicadores&xpid=INE)
- [Página oficial da API do INE](https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_api&INST=322751522&xlang=pt)
- [Sistema de Metainformação (SMI)](https://smi.ine.pt/)
- [Descrição oficial do SMI](https://www.ine.pt/ine_novidades/CE_SIG/NotaTecnica/12/)
- [Classificações e versões no SMI](https://www.ine.pt/ine_novidades/CE_SIG/NotaTecnica/13/)
- [Referenciais geográficos no SMI](https://www.ine.pt/ine_novidades/CE_SIG/NotaTecnica/14/)
- [Apresentação oficial da API, INEWS n.º 38](https://www.ine.pt/ine_novidades/semin/INEWS38/files/assets/common/downloads/publication.pdf)
- [Medida SIMPLEX relativa à API do INE](https://simplex.gov.pt/simplexmais/app/files/8cbc00676451c2cc41beaa8b60dedc67.pdf)
- [Política de difusão estatística do Sistema Estatístico Nacional](https://www.ine.pt/ine_novidades/CSE_2017/105/)
- [Princípios relativos a metainformação e qualidade](https://www.ine.pt/ine_novidades/CSE_2017/104/)
- [NUTS no Eurostat](https://ec.europa.eu/eurostat/web/nuts)
- [Histórico das NUTS](https://ec.europa.eu/eurostat/web/nuts/history/)
- [Local Administrative Units no Eurostat](https://ec.europa.eu/eurostat/web/nuts/local-administrative-units)

Foram também consultadas páginas individuais de indicadores no SMI e páginas
de metainformação `bddXplorer`, indicadas nas secções respetivas.

**Observado:** foram efetuados poucos pedidos `GET`, deliberadamente filtrados:

- metainformação completa do indicador `0008273`;
- metainformação completa do indicador `0010006`;
- uma observação do indicador `0008273`, para o Porto, 2023, ambos os sexos e
  total de grupos etários.

Não foi descarregado o catálogo integral nem qualquer conjunto de dados em
massa. Um pequeno grupo de pedidos simultâneos recebeu HTTP 429 e pedidos
posteriores ficaram temporariamente indisponíveis. A investigação foi por isso
interrompida antes de produzir carga adicional.

## 2. Estado da API atual

O INE disponibiliza endpoints públicos com nomes e formato anteriores às
convenções modernas de APIs REST. Apesar de usarem ficheiros `.jsp`, os
endpoints de dados e metainformação devolveram conteúdo atualizado em JSON.

| Função | Endpoint | Estado nesta análise |
|---|---|---|
| Dados de um indicador | `https://www.ine.pt/ine/json_indicador/pindica.jsp` | **Observado:** operacional com filtros e dados atuais. |
| Metainformação de um indicador | `https://www.ine.pt/ine/json_indicador/pindicaMeta.jsp` | **Observado:** operacional. |
| Catálogo de indicadores | `https://www.ine.pt/ine/xml_indic.jsp` | **Documentado/identificado:** serviço XML associado à API; não foi descarregado nesta análise. |
| Página humana de metainformação | `https://www.ine.pt/bddXplorer/htdocs/minfo.jsp` | **Observado:** usada pelo próprio JSON através de `MetaInfUrl`. |
| Pesquisa e objetos metodológicos | `https://smi.ine.pt/` | **Documentado e observado:** fonte oficial de conceitos, variáveis, classificações e metodologias. |

Parâmetros observados:

| Endpoint | Parâmetros relevantes |
|---|---|
| `pindicaMeta.jsp` | `varcd=<código do indicador>`, `lang=PT` ou `lang=EN` |
| `pindica.jsp` | `op=2`, `varcd=<código>`, `Dim1=...` até `DimN=...`, `lang=PT` ou `lang=EN` |
| `xml_indic.jsp` | `opc=2`, `lang=PT` ou `lang=EN` |

**Observado:** os filtros `DimN` aceitam os códigos das categorias publicados
na metainformação. A seleção usada para a observação do Porto foi:

```text
op=2
varcd=0008273
Dim1=S7A2023
Dim2=11A1312
Dim3=T
Dim4=T
lang=PT
```

**Documentado:** a apresentação oficial de 2018 descreve um serviço de
catalogação e um serviço JSON para extração de indicadores e respetiva
metainformação, com filtros, em português e inglês e com atualização em tempo
real.

**Observado:** não existe um número de versão no caminho, nos parâmetros ou nos
cabeçalhos das respostas consultadas. Não foi encontrada uma especificação
OpenAPI/Swagger pública.

**Inferência:** os endpoints estão ativos na prática, mas o seu ciclo de vida,
política de compatibilidade e eventual substituição não são claros. A pesquisa
não encontrou uma API pública moderna separada que substitua inequivocamente
estes serviços. Isto significa apenas “não encontrada”, não prova que não
exista.

## 3. Autenticação, custos e limites

| Tema | Resultado |
|---|---|
| Autenticação | **Observado:** os pedidos bem-sucedidos não usaram chave, cookie de sessão nem cabeçalho de autenticação. |
| Custo | **Documentado:** a apresentação oficial da API caracteriza o acesso como gratuito. |
| Rate limit numérico | Não documentado nas fontes consultadas. |
| HTTP 429 | **Observado:** quatro pedidos de metainformação feitos em simultâneo receberam `429 Too Many Requests`. |
| `Retry-After` | Não confirmado. Não foi preservado um cabeçalho que permitisse determinar um intervalo oficial. |
| Paginação | Não documentada nem observada nos endpoints JSON. |
| Limite de linhas/resposta | Não foi encontrada confirmação oficial atual. |
| SLA/disponibilidade | Não documentado. Foram observados timeouts temporários após as respostas 429. |

**Inferência:** a integração deverá limitar a concorrência, usar pedidos
filtrados, aplicar backoff com jitter a 429 e erros transitórios, e manter cache
local de catálogo e metainformação. Não se deve assumir que a ausência de uma
chave equivale a capacidade ilimitada.

## 4. Catálogo de indicadores

Existem três caminhos complementares para descobrir indicadores:

1. A Base de Dados do INE permite pesquisa humana e usa o parâmetro
   `indOcorrCod` nas páginas dos indicadores.
2. O SMI expõe o “Código de difusão” e os objetos metodológicos associados.
3. O serviço `xml_indic.jsp` fornece um catálogo legível por máquina.

**Observado:** o mesmo identificador aparece como `varcd` na API, como
`IndicadorCod` no JSON, como `indOcorrCod` em URLs do portal e como “Código de
difusão” no SMI. Tem sete caracteres e pode começar por zero, por exemplo
`0008273`. Deve ser armazenado como texto.

**Observado:** o identificador interno da página do SMI não é o código de
difusão. Por exemplo, a página SMI `17818` corresponde ao código de difusão
`0012910`. Ambos podem ser úteis para proveniência, mas não são
intermutáveis.

Uma implementação cliente atual, usada apenas como referência secundária,
interpreta no XML de catálogo os seguintes elementos:

- atributo `id` do elemento `indicator`;
- `varcd`, `title`, `description`, `theme`, `subtheme` e `keywords`;
- `geo_lastlevel`;
- `dates/last_period_available` e `dates/last_update`;
- `periodicity` e `update_type`;
- URLs da Base de Dados e da metainformação;
- URLs JSON do conjunto de dados e da metainformação.

**Observado (fonte secundária):** estes campos são usados por um cliente que
consome o serviço atual, mas o XML completo não foi revalidado nesta análise.
Não devem ser promovidos a contrato interno sem guardar uma amostra oficial e
testar campos opcionais.

**Inferência:** o código de difusão parece ser a melhor chave externa do
indicador. Não foi encontrada uma garantia formal de imutabilidade; deve ficar
sempre associado a `provider=INE`, e não ser usado como chave primária global
do PTScope.

## 5. Indicadores reais analisados

Foram selecionados oito indicadores para cobrir frequências, unidades,
granularidades, fontes e versões territoriais diferentes.

| Código | Indicador resumido | Frequência | Geografia relevante | Motivo |
|---|---|---|---|---|
| `0008273` | População residente por sexo e grupo etário | Anual | NUTS 2013 até município | Caso municipal diretamente consultado. |
| `0012910` | Índice de dependência de idosos | Anual | NUTS 2024 | Mostra a nova versão territorial e indicador separado do equivalente NUTS 2013. |
| `0012234` | Valor mediano das vendas de alojamentos, últimos 12 meses | Trimestral | NUTS 2024; relevante ao nível local | Preço por m² e frequência trimestral. |
| `0010042` | Valor mediano de avaliação bancária da habitação | Mensal | Município 2013 | Caso municipal mensal e exemplo histórico de confidencialidade. |
| `0013012` | Ganho/remuneração por trabalhador | Anual | NUTS 2024 | A fonte estatística é MTSSS/GEP, embora a difusão seja feita pelo INE. |
| `0010006` | Idade média ao óbito por sexo e causa de morte | Anual | Portugal a NUTS III | Muitas categorias; não chega a município. |
| `0010003` | Orçamento do Estado financiado por impostos cobrados internamente | Anual | Portugal | Caso simples, percentual e decimal. |
| `0002642` | Superfície das unidades territoriais | Anual | NUTS 2001 | Unidade km², fonte DGT e relação explícita com a CAOP anual. |

Pelo menos três são diretamente municipais ou relevantes para análise
municipal: `0008273`, `0010042` e `0012234`. O indicador `0012910` usa uma
classificação geográfica hierárquica NUTS 2024; o nível municipal efetivamente
disponível deve ser confirmado na metainformação antes de ingestão.

**Documentado:** o SMI associa os indicadores a variáveis de medida e de
dimensão, operações/fontes estatísticas e classificações específicas.

**Observado:** nem todos os indicadores incluem todos os níveis geográficos. O
`0008273` inclui 308 municípios; o `0010006` termina em NUTS III.

## 6. Metainformação detalhada

### 6.1. Indicador `0008273`

Metainformação devolvida diretamente por `pindicaMeta.jsp`:

| Campo | Valor observado |
|---|---|
| `IndicadorCod` | `0008273` |
| `IndicadorNome` | População residente (N.º) por Local de residência (NUTS - 2013), Sexo e Grupo etário; Anual - INE, Estimativas anuais da população residente |
| `Periodic` | `Anual` |
| `PrimeiroPeriodo` | `2011` |
| `UltimoPeriodo` | `2023` |
| `UnidadeMedida` | `Número (N.º)` |
| `Potencia10` | `0` |
| `PrecisaoDecimal` | `0` |
| `DataUltimaAtualizacao` | `2026-07-17` |
| `DataExtracao` | `2026-09-25T15:21:23.058+01:00` |

Dimensões:

1. Período de referência dos dados, versão `XXXXX`;
2. Local de residência (NUTS - 2013), versão `03505`;
3. Sexo, versão `00305`;
4. Grupo etário, versão `00708`.

**Observado:** a nota da dimensão temporal informa que as estimativas desde
2021 têm base administrativa, enquanto as estimativas até 2020 são definitivas
e baseadas nos censos. A própria fonte alerta para uma quebra metodológica
entre 2020 e 2021.

**Observado:** a nota geográfica indica CAOP 2020, à data dos Censos 2021, e
NUTS 2013, em vigor no sistema estatístico desde 1 de janeiro de 2015.

### 6.2. Indicador `0010006`

Metainformação devolvida diretamente por `pindicaMeta.jsp`:

| Campo | Valor observado |
|---|---|
| `IndicadorCod` | `0010006` |
| `IndicadorNome` | Idade média ao óbito (Ano) por Local de residência (NUTS - 2013), Sexo e Causa de morte (Lista OCDE adaptada); Anual - INE, Óbitos por causas de morte |
| `Periodic` | `Anual` |
| `PrimeiroPeriodo` | `2018` |
| `UltimoPeriodo` | `2019` |
| `UnidadeMedida` | `Ano (Ano)` |
| `Potencia10` | `0` |
| `PrecisaoDecimal` | `1` |
| `DataUltimaAtualizacao` | `2021-03-26` |

Dimensões:

1. Período de referência;
2. Local de residência (NUTS - 2013), versão `03505`;
3. Sexo, versão `00305`;
4. Causa de morte (Lista OCDE adaptada), versão `03622`.

**Observado:** a geografia contém 36 categorias, do país até NUTS III, e não
contém municípios. A causa de morte contém 55 categorias, incluindo o total.

A [página correspondente no SMI](https://smi.ine.pt/Indicador/Detalhes_TabIndicador/13835?clear=True)
associa o código de difusão `0010006` à variável de medida “Idade média ao
óbito (Ano)” e às variáveis de dimensão de tempo, local de residência, sexo e
causa de morte.

### 6.3. Indicador `0002642`

A [metainformação oficial](https://ine.pt/bddXplorer/htdocs/minfo.jsp?lingua=PT&var_cd=0002642)
descreve a superfície em km² das unidades territoriais, com fonte
Direção-Geral do Território, periodicidade anual, primeiro período 2003 e
último período 2013.

**Documentado:** o conceito de área total inclui superfícies de água doce,
artificiais e salgadas. Cada ano de referência está associado à CAOP em vigor
em 31 de dezembro desse ano. Esta nota impede tratar a área como um atributo
atemporal do território.

### 6.4. Indicadores NUTS 2024

No SMI:

- [`0012910`](https://smi.ine.pt/Indicador/Detalhes_TabIndicador/17818?clear=True)
  tem periodicidade anual, fonte “INE, Estimativas anuais da população
  residente”, variável de medida “Índice de dependência de idosos (N.º)” e
  dimensão “Local de residência (NUTS - 2024)”.
- [`0012234`](https://smi.ine.pt/Indicador/Detalhes_TabIndicador/18376?clear=True)
  tem periodicidade trimestral, fonte “INE, Estatísticas de preços da
  habitação ao nível local (Metodologia 2022)”, medida em `€/m²` e dimensões de
  período, localização NUTS 2024 e categoria do alojamento.
- [`0013012`](https://smi.ine.pt/Indicador/Detalhes/18662?modal=1) usa localização
  NUTS 2024 e tem como fonte MTSSS/GEP, Quadros de pessoal.

**Observado:** a API de metainformação destes indicadores não foi reconsultada
após o limite HTTP 429. Campos como primeiro período, último período, precisão
e lista completa de categorias ficam por confirmar antes da integração.

## 7. Dimensões e categorias

O JSON de metainformação contém `Dimensoes.Descricao_Dim` e a lista de
categorias de cada dimensão. Nos casos observados, uma categoria inclui:

| Campo | Interpretação observada |
|---|---|
| `dim_num` | Número da dimensão. |
| `cat_id` | Identificador interno da categoria na resposta. |
| `categ_cod` | Código usado no filtro `DimN`. |
| `categ_dsg` | Designação humana. |
| `categ_ord` | Ordem publicada pelo INE. |
| `categ_nivel` | Nível hierárquico dentro da classificação. |

No indicador `0008273` foram observadas:

- 13 categorias temporais, de 2011 a 2023;
- 344 categorias geográficas;
- 3 categorias de sexo: `T`/HM, `1`/H e `2`/M;
- 19 categorias de grupo etário, incluindo `T`/Total.

A dimensão geográfica organiza-se em cinco níveis:

```text
PT       Portugal
1        Continente
11       Norte
11A      Área Metropolitana do Porto
11A1312  Porto
```

**Observado:** `categ_nivel` permite distinguir níveis que não podem ser
deduzidos com segurança apenas pelo comprimento do código. Existem códigos
alfanuméricos e classificações diferentes podem reutilizar formatos.

**Inferência:** a ordem das dimensões e os respetivos números fazem parte do
contrato de cada indicador, não de um contrato universal. A integração deve
ler primeiro a metainformação e não codificar que “Dim2 é sempre geografia” ou
que “Dim3 é sempre sexo”.

## 8. Estrutura dos dados reais

Resposta reduzida do pedido diretamente efetuado para o Porto:

```json
[
  {
    "IndicadorCod": "0008273",
    "IndicadorDsg": "População residente (N.º) por Local de residência (NUTS - 2013), Sexo e Grupo etário; Anual - INE, Estimativas anuais da população residente",
    "MetaInfUrl": "https://www.ine.pt/bddXplorer/htdocs/minfo.jsp?var_cd=0008273&lingua=PT",
    "DataExtracao": "2026-09-25T15:24:58.753+01:00",
    "DataUltimoAtualizacao": "2026-07-17",
    "UltimoPref": "2023",
    "Dados": {
      "2023": [
        {
          "geocod": "11A1312",
          "geodsg": "Porto",
          "dim_3": "T",
          "dim_3_t": "HM",
          "dim_4": "T",
          "dim_4_t": "Total",
          "ind_string": "267 236",
          "valor": "267236"
        }
      ]
    },
    "Sucesso": {
      "Verdadeiro": [
        {"Msg": "OK"}
      ]
    }
  }
]
```

Aspetos do contrato observados:

- a resposta de topo é um array, mesmo para um indicador;
- `Dados` é um objeto cujas chaves são períodos;
- a dimensão temporal não reaparece como `dim_1` na observação;
- a geografia usa campos especiais `geocod` e `geodsg`;
- as restantes dimensões usam pares `dim_N` e `dim_N_t`;
- `valor` e `ind_string` são strings;
- `ind_string` é uma apresentação localizada e `valor` é mais adequado a
  processamento;
- o nome do campo de atualização difere entre endpoints:
  `DataUltimaAtualizacao` na metainformação e `DataUltimoAtualizacao` nos dados.

**Observado (fonte secundária):** um exemplo atual do indicador nacional
`0010003` apresenta um valor decimal como:

```json
{
  "geocod": "PT",
  "geodsg": "Portugal",
  "ind_string": "66,08",
  "valor": "66.08"
}
```

**Observado (histórico, fonte secundária):** uma resposta publicada para o
indicador mensal `0010042` continha, num registo confidencial, `sinal_conv` e
`sinal_conv_desc`, sem o campo `valor`:

```json
{
  "geocod": "1111609",
  "geodsg": "Viana do Castelo",
  "dim_3": "T",
  "dim_3_t": "Total",
  "sinal_conv": "¿",
  "sinal_conv_desc": "Dado confidencial"
}
```

Este exemplo histórico deve ser revalidado antes de se fixar um parser, mas é
suficiente para não assumir que toda a célula contém `valor`.

## 9. Valor estatístico

**Observado:** o valor processável chega como texto. O valor de população
`267236` aparece em `valor`, enquanto `ind_string` contém `267 236`. No exemplo
percentual, `valor` usa ponto decimal e `ind_string` usa vírgula decimal.

Regras prudentes para a integração futura:

- preservar sempre `valor` e `ind_string` originais;
- converter `valor` com um tipo decimal, não com `float`, quando a precisão for
  relevante;
- não converter uma ausência de `valor` em zero;
- permitir valores com sinal no parser, embora não tenha sido observado um
  valor negativo nesta análise;
- não extrair o número a partir de `ind_string`, salvo como último recurso
  explicitamente controlado;
- guardar `PrecisaoDecimal`, unidade e potência juntamente com a série.

Não foi observado um `null` JSON explícito. Foi observada historicamente a
ausência da chave `valor` numa célula confidencial. No modelo normalizado, essa
ausência poderá resultar em valor numérico nulo, mas só em conjunto com o
qualificador original.

## 10. Qualificadores e estado da observação

O valor estatístico não é suficiente para representar uma observação.

**Observado (histórico, fonte secundária):** `sinal_conv` contém um código/sinal
e `sinal_conv_desc` a descrição “Dado confidencial”. Nesse caso, `valor` pode
estar ausente.

**Documentado:** publicações do INE usam, entre outras convenções, `Pe` para
valor preliminar e `Po` para valor provisório. Não foi confirmado que esses
códigos sejam enviados nos mesmos campos da API JSON.

Não foi confirmado nesta análise o significado, na API, de símbolos como `x`,
`//` ou `...`. Também não foi confirmada uma enumeração oficial e completa de
estados para todos os indicadores.

**Inferência:** o PTScope deve tratar o qualificador como dado de primeira
classe e armazenar pelo menos:

- código/sinal original;
- descrição original;
- presença ou ausência do valor;
- estado normalizado apenas quando existir uma tabela de correspondência
  documentada;
- versão dessa correspondência.

Uma célula confidencial, não aplicável, indisponível, provisória ou estimada
não deve ser confundida com zero nem com uma falha de transporte.

## 11. Dimensão temporal

No indicador anual `0008273`:

- o código interno da categoria é `S7A2023`;
- a designação é `2023`;
- a ordem observada é equivalente a `20230101`;
- a chave correspondente em `Dados` é `2023`.

**Observado (histórico, fonte secundária):** em indicadores mensais aparecem
códigos no formato `S3A202006`, enquanto a resposta agrupa os dados sob uma
chave como `202006` e pode apresentar o mês por extenso em `UltimoPref`.

**Documentado:** os indicadores analisados incluem periodicidades anual,
trimestral e mensal. O SMI também contém operações com outras frequências,
incluindo semestral, decenal e não periódica.

| Aspeto | Estado |
|---|---|
| Código anual `S7A<AAAA>` | **Observado** no indicador `0008273`. |
| Código mensal `S3A<AAAAMM>` | **Observado** em exemplo histórico. |
| Código trimestral | Não confirmado nesta análise. |
| Data inicial/final exata do período | Não aparece como tal nas observações consultadas. |
| Periodicidade | Metadado do indicador. |
| Ordem | Disponível em `categ_ord` na categoria temporal. |

**Inferência:** o período deve ser ingerido a partir da categoria da dimensão
temporal e da sua designação. Datas inicial e final só devem ser derivadas por
uma regra específica para a periodicidade e código confirmados, nunca por uma
subdivisão cega da string.

## 12. Geografia e níveis territoriais

O indicador `0008273` demonstra que a geografia do INE é uma dimensão
hierárquica e versionada:

| Nível observado | Exemplo | Designação |
|---|---|---|
| País | `PT` | Portugal |
| NUTS I | `1` | Continente |
| NUTS II | `11` | Norte |
| NUTS III | `11A` | Área Metropolitana do Porto |
| Município | `11A1312` | Porto |

**Observado:** a dimensão continha uma categoria de país, três de NUTS I, sete
de NUTS II, 25 de NUTS III e 308 municípios.

O código municipal composto `11A1312` inclui o caminho NUTS III `11A` e o
sufixo municipal `1312`. A GEO API PT apresenta o Porto como `1312`.

**Inferência:** existe uma correspondência útil entre o sufixo municipal do
indicador NUTS 2013 e o código municipal CAOP/INE usado pela GEO API PT. Isto
não autoriza preencher `1312` com zeros nem assumir que todos os códigos INE
têm sete dígitos. `1312` e `11A1312` pertencem a contextos de classificação
diferentes.

O distrito não aparece na hierarquia observada do indicador. Outros
indicadores podem terminar em Portugal, NUTS I, NUTS II, NUTS III, município,
freguesia, lugar ou níveis estatísticos mais finos.

**Inferência:** cada observação geográfica deve ser acompanhada por:

- código e designação originais;
- nível declarado pela categoria;
- classificação e versão;
- referencial administrativo/CAOP, quando indicado;
- ligação explícita, e versionada, a uma entidade territorial interna.

## 13. Versões territoriais

**Documentado:** a nomenclatura NUTS tem três níveis regionais. O município
corresponde a uma LAU, embora o INE possa publicar uma árvore combinada que
inclui país, NUTS e município.

**Documentado:** a NUTS 2013 passou a ser aplicada no Sistema Estatístico
Nacional e no sistema europeu em 1 de janeiro de 2015. A [página do
Eurostat](https://ec.europa.eu/eurostat/web/nuts/history/) indica que a NUTS
2024 está em vigor desde 1 de janeiro de 2024 e resulta do Regulamento Delegado
(UE) 2023/674.

No SMI, as versões observadas incluem:

- `V03505`, hierarquia NUTS 2013 com município e freguesia;
- `V05257`, hierarquia NUTS 2024 correspondente;
- `V04479`, associação NUTS 2013/CAOP 2020;
- `V05320`, associação NUTS 2024/CAOP 2020.

Na API JSON, a versão de dimensão surge sem o prefixo `V`, por exemplo `03505`.

**Observado:** existem indicadores separados para a mesma família conceptual
quando muda a versão territorial. O SMI relaciona, por exemplo, ocorrências do
índice de dependência de idosos em NUTS 2013 e em NUTS 2024; o código NUTS 2024
é `0012910`.

**Documentado:** quando uma classificação NUTS é alterada, o Eurostat prevê a
substituição de séries históricas pela nova desagregação quando isso seja
viável e aplicável ao domínio. Isto não garante que todos os indicadores do
INE tenham sido retroconvertidos.

**Inferência:** o PTScope não deve juntar séries NUTS 2013 e NUTS 2024 apenas
por terem o mesmo nome. Uma mudança de código de indicador, dimensão,
classificação, cobertura ou metodologia pode representar uma quebra real.

## 14. Alterações administrativas

**Documentado:** a revisão de 2013 da divisão administrativa portuguesa
introduziu alterações relevantes ao nível das freguesias. Publicações do INE
distinguem referenciais estáticos e referenciais “flutuantes”, nos quais as
alterações administrativas posteriores são consideradas segundo a CAOP e a
data de referência.

**Documentado:** no indicador `0002642`, a área de cada ano está associada à
CAOP em vigor em 31 de dezembro. Noutras publicações, extrações durante o ano
podem usar a geografia válida em 31 de dezembro do ano anterior.

**Observado:** a metainformação de `0008273` liga explicitamente a série NUTS
2013 à CAOP 2020 no contexto dos Censos 2021. A designação “NUTS 2013” não é,
por si só, suficiente para determinar o recorte administrativo de todos os
níveis locais.

Não foi confirmado um mecanismo da API que exponha diretamente:

- data de início e fim de validade de cada código geográfico;
- relação antecessor/sucessor após fusões ou desagregações;
- tabela completa de equivalências entre versões;
- política para códigos desativados em cada indicador.

**Inferência:** essas relações terão de vir do SMI, da CAOP ou de uma camada de
correspondência territorial dedicada, mantendo relações muitos-para-muitos e
intervalos de validade. Não se deve sobrescrever uma entidade histórica com o
nome ou limite atual.

## 15. Unidade, precisão e potência de 10

A metainformação JSON disponibiliza:

- `UnidadeMedida`;
- `Potencia10`;
- `PrecisaoDecimal`.

Unidades encontradas nos indicadores analisados incluem `Número (N.º)`,
`Percentagem (%)`, `Ano (Ano)`, `Euro por metro quadrado (€/m²)` e `Quilómetro
quadrado (km²)`.

**Observado:** `0008273` tem potência `0` e precisão `0`; `0010006` tem
potência `0` e precisão `1`. Páginas oficiais de outros indicadores apresentam
potência `3`, incluindo indicadores monetários.

**Inferência:** pela convenção estatística, potência `3` sugere uma escala de
`10³`. Não foi encontrada, porém, uma definição técnica inequívoca que esclareça
se o `valor` JSON já vem escalado ou se o consumidor deve aplicar o fator.

Até essa semântica ser confirmada:

- preservar `valor`, `UnidadeMedida`, `Potencia10` e `PrecisaoDecimal`;
- não multiplicar nem dividir automaticamente por `10^Potencia10`;
- não incorporar a potência no texto da unidade sem validação;
- mostrar o valor publicado (`ind_string`) quando for necessário reproduzir a
  apresentação oficial.

**Documentado:** as páginas de metainformação podem acrescentar fórmula,
conceitos e observações metodológicas. Estes elementos não devem ser
substituídos por interpretações inferidas a partir do título.

## 16. Revisões e atualização retroativa

**Documentado:** o INE corrige erros, publica revisões e documenta alterações
metodológicas. Existem indicadores cuja metainformação declara recalculação
retrospetiva após mudança de metodologia.

A [informação do INE sobre revisões de estimativas
populacionais](https://www.ine.pt/ine_novidades/semin/INEWS66/10/) descreve
efeitos em emprego, contas nacionais e indicadores per capita. Uma série já
extraída pode, portanto, mudar posteriormente.

**Observado:** a API expõe uma data de última atualização ao nível do indicador
e uma data/hora de extração. Não foi observado um identificador de versão da
observação nem uma data de revisão por célula.

**Inferência:** uma sincronização futura deve suportar:

- reextração de períodos históricos quando a data de atualização muda;
- snapshots ou histórico de versões, em vez de atualização destrutiva;
- comparação de payloads ou hashes por extração;
- registo da data de extração do fornecedor e da data de ingestão do PTScope;
- distinção entre revisão estatística e correção do pipeline interno.

## 17. Proveniência

O INE é o fornecedor da API, mas não é necessariamente o produtor primário de
todos os dados.

| Indicador | Fornecedor de difusão | Fonte/operação indicada |
|---|---|---|
| `0008273` | INE | INE, Estimativas anuais da população residente |
| `0012910` | INE | INE, Estimativas anuais da população residente |
| `0012234` | INE | INE, Estatísticas de preços da habitação ao nível local, Metodologia 2022 |
| `0013012` | INE | MTSSS/GEP, Quadros de pessoal |
| `0010006` | INE | INE, Óbitos por causas de morte |
| `0002642` | INE | Direção-Geral do Território |
| `0010003` | INE | Direção-Geral do Orçamento/Ministério das Finanças, segundo a metainformação associada |

**Inferência:** a proveniência mínima de uma ingestão deverá incluir:

- fornecedor e endpoint;
- código e designação do indicador;
- organização e operação estatística de origem;
- URL de metainformação;
- idioma;
- data de atualização da fonte;
- data/hora de extração;
- parâmetros/filtros usados;
- payload original ou referência imutável ao mesmo;
- hash do payload;
- versão do transformador do PTScope;
- licença e texto de atribuição aplicáveis.

Isto permite distinguir “obtido através do INE” de “produzido originalmente
pelo INE”.

## 18. Indicador e observações

Um indicador não é uma única série plana. É uma definição estatística que
combina:

- variável de medida;
- unidade, precisão e eventual escala;
- periodicidade;
- fonte/operação estatística;
- conjunto ordenado de dimensões;
- classificações e versões de cada dimensão;
- notas, conceitos, fórmula e metodologia;
- cobertura temporal disponível.

Uma observação é uma célula concreta desse espaço dimensional:

```text
indicador + período + geografia + categorias das restantes dimensões
-> valor + apresentação + qualificadores
```

No exemplo do Porto:

```text
0008273 + 2023 + 11A1312 + HM + Total
-> 267236 + "267 236"
```

**Inferência:** a chave lógica de uma observação deve incluir todas as
dimensões, mesmo quando uma categoria é “Total”. Omitir `sexo=T` ou
`grupo_etário=T` criaria colisões com desagregações e perderia significado.

## 19. Modelo dimensional sugerido pela fonte

Sem definir ainda o esquema físico, a fonte sugere quatro conceitos distintos:

1. **Indicador**: identidade, título, definição, unidade, periodicidade,
   precisão, fonte e metodologia.
2. **Dimensão do indicador**: posição (`Dim1`, `Dim2`, ...), designação,
   classificação e versão.
3. **Categoria**: código, designação, ordem, nível e possível relação
   hierárquica.
4. **Observação**: combinação de categorias, valor e qualificadores num dado
   período/extracção.

**Observado:** a posição da dimensão é necessária para construir o pedido, mas
os campos de resposta tratam tempo e geografia de forma especial.

**Inferência:** o modelo interno deve conseguir representar dimensões genéricas
sem criar uma coluna nova por cada indicador. Campos promovidos, como período e
geografia, podem coexistir com uma coleção ordenada de categorias para as
outras dimensões.

As classificações devem ser reutilizáveis entre indicadores quando o código de
versão o comprovar, mas a relação concreta indicador-dimensão deve preservar a
ordem e o subconjunto de categorias publicado.

## 20. Escala potencial

O número de observações cresce como produto das categorias das dimensões.

Para `0008273`, a metainformação observada contém:

```text
13 períodos × 344 geografias × 3 sexos × 19 grupos etários
= 254 904 células teóricas
```

Para `0010006`:

```text
2 períodos × 36 geografias × 3 sexos × 55 causas
= 11 880 células teóricas
```

O número real pode ser inferior se existirem combinações não publicadas,
confidenciais ou não aplicáveis.

**Observado (fonte secundária):** uma implementação cliente atual refere uma
ordem de grandeza superior a 13 mil indicadores no catálogo e avisa que a sua
obtenção integral pode ser demorada. Este total não foi contado nem confirmado
diretamente nesta análise.

**Inferência:** uma ingestão indiscriminada do catálogo completo poderia gerar
dezenas ou centenas de milhões de observações. A estratégia deverá ser
orientada por uma lista explícita de indicadores, geografias e períodos, com
estimativa prévia da cardinalidade e pedidos pequenos.

## 21. Licença e reutilização

**Documentado:** publicações oficiais do INE identificam conteúdo estatístico
sob [Creative Commons Atribuição 4.0 Internacional
(CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) e exigem indicação
clara da fonte. A política de difusão do Sistema Estatístico Nacional permite
redistribuição com menção da fonte.

**Documentado:** o acesso gratuito à API não substitui a licença nem elimina a
obrigação de atribuição.

Não foi encontrada, na análise técnica dos endpoints, uma página única que
especifique de forma exaustiva:

- condições de cache da API;
- política técnica para republicação de snapshots;
- duração recomendada da cache;
- condições adicionais para indicadores cuja fonte primária é outra entidade.

**Inferência:** para cada conjunto publicado pelo PTScope devem ser guardados e
exibidos o INE como fornecedor, a fonte/operação primária, o código do
indicador, a data de extração e a ligação para a metainformação. Antes de
redistribuição em massa, deve confirmar-se a licença aplicável ao recurso
concreto e a eventuais componentes de terceiros.

## 22. GEO API PT versus INE

| Tema | GEO API PT | INE |
|---|---|---|
| Foco | Objetos territoriais, geometrias e dados agregados de conveniência | Estatísticas oficiais, séries, dimensões e metainformação |
| Geometria | GeoJSON municipal e de freguesia | Não observada nos endpoints de indicadores |
| Catálogo estatístico | Limitado ao contrato próprio | Catálogo amplo de indicadores e SMI |
| Tempo | Snapshots e blocos como Censos 2011/2021 | Dimensão temporal explícita e várias periodicidades |
| Dimensões | Campos específicos do endpoint | Classificações genéricas e versionadas |
| Unidade/metodologia | Parcial; existem campos ambíguos como `areaha` | Unidade, precisão, potência, conceitos e notas metodológicas |
| Revisões | Não avaliadas como séries estatísticas | Parte explícita do processo estatístico |
| Código do Porto | `1312` | `11A1312` no indicador NUTS 2013 analisado |

Para população e censos, o INE deve ser preferido como fonte estatística
primária quando forem necessárias definição, dimensão, período, revisão e
metodologia. A GEO API PT continua útil para geometrias e para uma consulta
territorial simples, desde que a proveniência dos campos estatísticos seja
conhecida.

**Inferência:** os dados de Censos embebidos na GEO API PT não devem ser
misturados automaticamente com observações do INE pelo nome do campo. A
equivalência exige código de indicador, conceito, população de referência,
geografia, período e versão territorial compatíveis.

## 23. Campos candidatos para ingestão

Esta secção é um inventário de candidatos, não um esquema definitivo.

### Núcleo do indicador

- fornecedor e código externo;
- designação completa e designação curta interna;
- descrição/definição;
- periodicidade;
- primeiro e último período disponíveis;
- unidade, símbolo da unidade, potência de 10 e precisão decimal;
- fórmula;
- conceitos e notas metodológicas;
- fonte/operação estatística;
- idioma;
- URL da metainformação;
- data de última atualização.

### Observação

- código do indicador;
- período: código, designação e ordem originais;
- código e designação geográficos originais;
- código e designação de todas as categorias dimensionais;
- `valor` original;
- valor decimal normalizado, quando seguro;
- `ind_string`;
- código e descrição do qualificador;
- data de extração da fonte;
- data de ingestão;
- identificador do snapshot.

### Dimensões e classificações

- número/posição da dimensão;
- designação;
- código e versão da classificação;
- código, designação, ordem e nível da categoria;
- relação hierárquica, apenas quando confirmada;
- intervalo de validade, quando disponível;
- ligação a entidade territorial interna, versionada.

### Proveniência operacional

- endpoint e parâmetros usados;
- idioma;
- estado HTTP;
- hash e localização do payload bruto;
- versão do parser/transformador;
- fornecedor e produtor primário;
- licença e atribuição;
- mensagens de sucesso/erro devolvidas pela fonte.

### Útil mais tarde

- temas, subtemas e palavras-chave do catálogo;
- agenda esperada de atualização;
- relações entre indicadores antecessores/sucessores;
- indicadores derivados e dependências;
- qualidade, cobertura e flags normalizadas;
- correspondências territoriais entre versões.

### Ignorar nesta fase

- formatação HTML da página humana;
- IDs de interface sem semântica confirmada;
- inferências de unidade feitas apenas pelo nome;
- valores calculados a partir de `ind_string` quando existe `valor`;
- padding automático de códigos geográficos;
- equivalências entre indicadores baseadas apenas em títulos semelhantes.

## 24. Implicações para PostgreSQL

Embora PostgreSQL não faça parte desta fase, a descoberta tem consequências
para um desenho futuro:

- códigos de indicador, dimensão, categoria e geografia devem ser texto;
- valores processáveis devem preferir `numeric`, mantendo também o texto bruto;
- a ausência de valor deve ser distinguida de zero e acompanhada por
  qualificadores;
- dimensões são variáveis em número e ordem, pelo que uma tabela larga fixa não
  cobre o catálogo;
- classificações e versões territoriais precisam de entidades próprias;
- uma observação precisa de unicidade sobre indicador, período e combinação
  completa de categorias;
- atualizações retroativas exigem histórico, snapshots ou validade temporal;
- payloads brutos e hashes facilitam auditoria e reprocessamento;
- índices devem ser guiados pelos indicadores e geografias efetivamente
  ingeridos, não pelo catálogo teórico;
- geometrias deverão vir de uma fonte territorial própria e ser ligadas por
  correspondências versionadas, não copiadas das observações estatísticas.

**Inferência:** separar metadados, classificações e factos evita repetir textos
longos em milhões de observações. A forma concreta, incluindo normalização ou
uso complementar de JSONB, deve ser decidida após protótipos com indicadores
de cardinalidades diferentes.

## 25. Questões em aberto

Antes de implementar a integração, devem ser respondidas pelo menos estas
questões:

1. Qual é a documentação técnica oficial e atual dos parâmetros `op`, `opc` e
   `DimN`?
2. Existe uma política oficial de versionamento e de descontinuação dos
   endpoints JSP?
3. Quais são os limites atuais por pedido, minuto, dia, IP ou volume de
   resposta?
4. Existe paginação ou um método oficial de extração em lotes?
5. Qual é a semântica exata de `Potencia10` em relação a `valor`?
6. Qual é a enumeração completa de `sinal_conv` e de outros qualificadores na
   API JSON?
7. Como são representados de forma consistente valores provisórios, estimados,
   revistos, confidenciais, não aplicáveis e indisponíveis?
8. `DataUltimoAtualizacao` aplica-se a todo o indicador ou apenas à resposta
   filtrada?
9. Existe um identificador oficial de versão/revisão de uma observação?
10. O código de difusão pode ser reutilizado, substituído ou retirado? Como são
    publicados antecessores e sucessores?
11. Como obter oficialmente correspondências entre NUTS 2013, NUTS 2024 e as
    várias CAOP ao nível municipal e de freguesia?
12. Que indicadores NUTS 2024 têm efetivamente todos os 308 municípios?
13. Qual é o código interno dos períodos trimestrais e de outras frequências?
14. O catálogo XML tem campos opcionais ou limites que não aparecem nos
    clientes existentes?
15. Existe uma API SDMX pública de difusão que deva ser preferida para alguns
    domínios?
16. Existe um serviço HVD moderno com contrato e licença próprios para os
    indicadores estatísticos de elevado valor?
17. Que condições específicas se aplicam à republicação de indicadores cuja
    fonte primária não é o INE?
18. Qual é a política recomendada de cache e de atribuição para produtos que
    redistribuem observações?

## 26. Recomendações para a próxima fase

1. Começar por um conjunto pequeno de indicadores aprovados, incluindo um
   anual municipal (`0008273`), um mensal municipal (`0010042`) e um trimestral
   local (`0012234`).
2. Criar primeiro um cliente de metainformação; nenhum indicador deve ser
   ingerido sem dimensões, categorias, unidade, precisão e notas.
3. Aplicar concorrência muito baixa, timeout explícito, retry limitado e
   backoff com jitter, respeitando HTTP 429.
4. Pedir apenas períodos, geografias e categorias necessários; nunca iniciar
   por uma descarga integral do catálogo.
5. Guardar o payload bruto e os parâmetros de cada extração antes de
   normalizar.
6. Preservar `valor`, `ind_string`, qualificadores, unidade, potência e
   precisão sem transformações irreversíveis.
7. Não aplicar a potência de 10 até a semântica ser confirmada por documentação
   oficial ou teste inequívoco.
8. Modelar códigos como strings e não impor comprimentos universais.
9. Manter classificação NUTS, versão SMI e referencial CAOP junto da geografia.
10. Tratar revisões como novas versões de dados e reprocessar períodos
    históricos quando a fonte for atualizada.
11. Validar explicitamente a licença e a atribuição de cada fonte/operação
    antes de republicar em massa.
12. Fazer uma segunda ronda de descoberta, pequena e sequencial, para resolver
    potência de 10, qualificadores e períodos trimestrais antes de escrever a
    integração de produção.

Conclusão: a API atual do INE é utilizável e oferece metainformação bastante
mais rica do que uma simples lista de valores. A integração segura depende de
tratar dimensões, versões territoriais, qualificadores, proveniência e revisões
como parte do dado. O principal risco não é o transporte JSON; é apagar
significado estatístico durante a normalização.
