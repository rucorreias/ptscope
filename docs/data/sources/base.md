# Portal BASE: descoberta de dados

> Data da análise: 25 de setembro de 2026.
> Âmbito: investigação da fonte e do seu contrato observável. Este documento
> não implementa uma integração, não define o modelo final de dados do PTScope
> e não estabelece regras de reconciliação com outras fontes.

As decisões gerais de ingestão do PTScope são mantidas em
[`docs/architecture/data-ingestion.md`](../../architecture/data-ingestion.md).
Este documento responde apenas à pergunta: **o que o Portal BASE realmente
disponibiliza e qual é o contrato observável da fonte?**

São usados três qualificadores:

- **Documentado**: consta de uma fonte oficial do Portal BASE, do IMPIC, de um
  diploma legal ou de metadados oficiais publicados pelo IMPIC no
  dados.gov.pt.
- **Observado**: foi confirmado numa resposta HTTP ou numa amostra real dos
  dados na data acima.
- **Inferência**: conclusão técnica plausível, mas não declarada de forma
  inequívoca pela fonte.

Regra aplicada em toda a análise:

```text
semântica desconhecida -> preservar bruto -> não normalizar -> documentar questão
```

Foram feitos apenas pedidos `GET` e `HEAD` pequenos, sequenciais e com timeout.
Os grandes ficheiros não foram descarregados. Para observar o contrato dos
datasets foram usados intervalos HTTP de 32 ou 64 KiB, suficientes para obter
registos completos no início de cada recurso.

## 1. Visão geral

**Documentado:** o [Portal BASE](https://www.base.gov.pt/) é o portal público português de
contratação pública. A sua função essencial é centralizar e publicitar
informação sobre a formação e a execução de contratos públicos, permitindo o
acompanhamento e a produção de informação estatística.

**Documentado:** a [Portaria n.º
318-B/2023](https://diariodarepublica.pt/dr/legislacao-consolidada/portaria/2023-223383895)
regula o funcionamento e a gestão do portal e aprova os modelos de dados que
lhe são transmitidos. O portal inclui uma área pública e uma área reservada
para informação de auditoria e controlo.

**Documentado:** o âmbito público inclui, entre outros elementos:

- anúncios nacionais e europeus;
- formação e execução de contratos;
- objeto e CPV;
- preço base, preço contratual e preço total efetivo;
- entidades adjudicantes, adjudicatários, concorrentes e candidatos;
- datas de adjudicação, celebração, início e fecho;
- prazo;
- contratos, anexos e aditamentos, com exceções por segredo ou dados pessoais;
- modificações objetivas;
- não celebração, impugnações e informação estatística.

**Observado:** os mecanismos públicos de distribuição atuais não expõem todo o
modelo legal com a mesma granularidade. Os downloads anuais achatam e omitem
parte da estrutura; a API documentada expõe apenas quatro famílias de consulta.

**Inferência:** atendendo às funções documentadas, o BASE deve ser entendido
como uma combinação de:

- **sistema de recolha**, porque recebe blocos de dados de várias origens;
- **agregador**, porque centraliza anúncios, procedimentos, contratos e
  execução;
- **sistema de publicação**, porque disponibiliza a área pública, downloads e
  API;
- **sistema estatístico**, porque suporta relatórios nacionais e europeus.

Não é correto tratar o BASE como produtor original de todos os factos
publicados.

## 2. Fontes oficiais consultadas

Fontes do Portal BASE e do IMPIC:

- [Portal BASE](https://www.base.gov.pt/)
- [Pesquisa pública](https://www.base.gov.pt/Base4/pt/pesquisa)
- [O que é o Portal BASE](https://www.base.gov.pt/Base4/pt/o-portal/base/)
- [O que nos comunicam](https://www.base.gov.pt/Base4/pt/o-portal/o-que-nos-comunicam/)
- [Formas de obter dados](https://www.base.gov.pt/Base4/pt/documentacao/formas-de-obter-dados-sobre-os-contratos-publicos/)
- [Documentação da API REST](https://www.base.gov.pt/APIBase2)
- [WADL da API](https://www.base.gov.pt/APIBase2/api.wadl)
- [Anúncio oficial da API, 7 de maio de 2025](https://www.base.gov.pt/Base4/pt/noticias/2025/api-para-consulta-de-dados-do-portal-base/)
- [Helpdesk do IMPIC](https://www.impic.pt/support/open.php)
- [Perguntas frequentes](https://www.base.gov.pt/Base4/pt/perguntas-frequentes/)
- [Portaria n.º 318-B/2023, versão consolidada no Diário da República](https://diariodarepublica.pt/dr/legislacao-consolidada/portaria/2023-223383895)
- [Requisitos de interligação das plataformas eletrónicas](https://www.base.gov.pt/Base4/media/fpre43qu/req_interligacao_pe_base_20200117.pdf)
- [Descrição técnica da arquitetura do Portal BASE](https://www.impic.pt/impic/assets/misc/img/informacao_institucional/concursos_publicos/Caderno_Encargos_24524_2024.pdf)
- [Legislação CPV no Portal BASE](https://www.base.gov.pt/base4/pt/legislacao/?index=13&month=0&scope=0&text=&type=0&year=0)

Datasets oficiais publicados pelo IMPIC no dados.gov.pt:

- [Contratos de 2012 a 2026](https://dados.gov.pt/pt/datasets/contratos-publicos-portal-base-impic-contratos-de-2012-a-2026)
- [Anúncios de 2012 a 2026](https://dados.gov.pt/pt/datasets/contratos-publicos-portal-base-impic-anuncios-de-2012-a-2026)
- [Modificações contratuais de 2012 a 2026](https://dados.gov.pt/pt/datasets/contratos-publicos-portal-base-impic-modificacoes-contratuais-de-2012-a-2026)
- [Entidades](https://dados.gov.pt/pt/datasets/contratos-publicos-portal-base-impic-entidades)

Foi ainda identificado em resultados indexados um antigo dataset complementar
“Local de Execução - Portal BASE - IMPIC (Transparência)”. O URL oficial
devolveu `404` em 25 de setembro de 2026; por isso, não foi tratado como fonte
atual nem incluído na lista acima.

Os metadados estruturados foram consultados através da API pública do
dados.gov.pt, por exemplo:

```text
GET https://dados.gov.pt/api/1/datasets/contratos-publicos-portal-base-impic-contratos-de-2012-a-2026/
```

O dados.gov.pt foi usado apenas porque os recursos são publicados pela
organização oficial do IMPIC e a própria documentação do BASE indica este
canal.

## 3. Responsabilidade e proveniência

### 3.1. Gestão e operação

**Documentado:** a gestão do Portal BASE é responsabilidade do Instituto dos
Mercados Públicos, do Imobiliário e da Construção, I. P. (IMPIC, I. P.). O
IMPIC disponibiliza a interface pública, publica os datasets e autoriza o
acesso à API de grandes volumes.

**Documentado:** documentos técnicos do próprio IMPIC descrevem uma arquitetura
com portal público, CMS, webservices REST de front-end, webservices de
plataformas, back-office, camada de serviços, base de dados e business
intelligence.

Não foi encontrada uma fonte atual que identifique inequivocamente uma empresa
externa como operador técnico corrente. Cadernos de encargos demonstram
contratação de manutenção e evolução, mas não bastam para atribuir a operação
atual a um adjudicatário específico.

### 3.2. Origem dos dados

**Documentado:** a Portaria n.º 318-B/2023 distingue as seguintes origens:

| Conteúdo | Origem documentada |
|---|---|
| Anúncio nacional | Diário da República, gerido pela Imprensa Nacional-Casa da Moeda (INCM). |
| Anúncio europeu | Sistema de Informação para os Mercados Públicos (SIMAP). |
| Blocos técnicos e de formação | Entidade adjudicante, normalmente através de plataforma eletrónica. |
| Dados sem plataforma eletrónica | Entidade adjudicante, por introdução direta no Portal BASE. |
| Alguns ajustes diretos e consultas prévias | Software de gestão administrativa/contabilística ou plataforma eletrónica. |
| Execução e modificações | Entidade adjudicante e, em casos previstos, plataforma eletrónica. |
| Pagamentos | Entidade adjudicante, plataforma eletrónica ou, quando possível, solução de faturação eletrónica. |

**Documentado:** a informação constante do portal é da exclusiva
responsabilidade das entidades adjudicantes, independentemente da via de
transmissão. O IMPIC pode identificar incorreções ou incoerências e pedir a
respetiva correção, mas não se substitui à entidade comunicante.

**Inferência:** uma cadeia de proveniência pode, portanto, conter vários papéis:

```text
canal de distribuição -> Portal BASE/IMPIC -> sistema de transmissão
-> entidade responsável pelo registo -> partes e factos do contrato
```

Exemplo:

```text
dados.gov.pt -> dataset do IMPIC -> Portal BASE -> plataforma eletrónica
-> entidade adjudicante -> adjudicatário
```

O dados.gov.pt é um canal de distribuição. A plataforma eletrónica é um canal
de transmissão. Nenhum destes papéis deve ser confundido automaticamente com o
produtor ou responsável pelo conteúdo do registo.

## 4. Formas de acesso

### 4.1. Interface web pública

**Documentado:** a [pesquisa pública](https://www.base.gov.pt/Base4/pt/pesquisa)
permite consultar contratos, anúncios, entidades, modificações contratuais,
bens móveis, não celebrações, impugnações e consultas preliminares.

Filtros visíveis para contratos incluem:

- texto do objeto;
- entidade adjudicante e adjudicatária;
- tipo de procedimento e de contrato;
- CPV;
- acordo-quadro e procedimento centralizado;
- peças do procedimento e critérios ambientais;
- prazo, preços e datas;
- país, distrito e concelho do local de execução.

**Observado:** as páginas de pesquisa dependem de JavaScript para carregar
resultados. A documentação técnica do IMPIC confirma que o CMS usa webservices
REST internos de front-end.

Esses webservices internos não foram investigados nem tratados como API
pública. A sua existência não implica estabilidade contratual ou autorização
para uso automatizado.

### 4.2. API oficial do IMPIC

**Documentado:** existe uma API para grandes volumes, com dados atualizados
diariamente. O acesso requer registo, pedido no Helpdesk e autorização prévia
do IMPIC. Após aprovação é fornecido um token.

**Documentado:** a página “Formas de obter dados” afirma que os campos da API
são os mesmos dos ficheiros do dados.gov.pt.

### 4.3. Downloads oficiais no dados.gov.pt

**Documentado:** o IMPIC publica recursos anuais em JSON, ZIP/JSON e XLSX, com
frequência declarada semanal.

| Dataset | Formatos atuais observados | Organização |
|---|---|---|
| Contratos | ZIP contendo JSON; XLSX | Um recurso por ano, 2012-2026. |
| Anúncios | JSON; XLSX | Um recurso por ano, 2012-2026. |
| Modificações | JSON; XLSX | Um recurso por ano, 2012-2026. |
| Entidades | JSON; XLSX | Snapshot agregado. |

**Observado:** cada recurso do dados.gov.pt inclui identificador, URL, formato,
tamanho, data de modificação e checksum SHA-1. O URL físico muda quando o
recurso é atualizado, enquanto o identificador do recurso fornece um caminho
“latest”.

### 4.4. Extração direta do portal

**Documentado:** os dados públicos podem ser extraídos gratuitamente e em
formatos abertos. A extração direta do portal é limitada por ficheiro e por um
número de linhas definido no sistema.

**Observado:** não foi encontrada, nas páginas atuais consultadas, a descrição técnica do
endpoint de exportação, do número de linhas ou do formato concreto dessa
extração direta.

### 4.5. Outros canais

**Documentado:** entidades públicas de auditoria, fiscalização e regulação
podem obter acesso direto por protocolo. Existem ainda integrações iAP e
webservices entre sistemas. Estes canais não são APIs públicas e estão fora do
âmbito de uma integração pública do PTScope.

**Observado:** não foi identificado um feed RSS/Atom de contratos nem uma distribuição
oficial atual em OCDS entre os quatro datasets correntes. Um recurso OCDS
histórico é referido em discussões antigas do dados.gov.pt, mas não foi tratado
como contrato atual.

## 5. API, endpoints e exportações

### 5.1. URL e autenticação

**Documentado:** a documentação da API está em:

```text
https://www.base.gov.pt/APIBase2
```

**Documentado:** o header obrigatório segundo o WADL é:

```http
_AcessToken: <Token>
```

O nome contém um só `c` em `_AcessToken` e deve ser preservado exatamente como
documentado. A página HTML chama-lhe genericamente “Authorization header”, mas
não usa o cabeçalho HTTP standard `Authorization` no exemplo.

### 5.2. Recursos documentados

| Recurso | Método e caminho | Filtros documentados |
|---|---|---|
| Contratos | `GET /APIBase2/GetInfoContrato` | `idContrato`, `IdProcedimento`, `nifEntidade`, `nAnuncio`, `numAcordoQuadro`, `numDias`, `Ano` |
| Anúncios | `GET /APIBase2/GetInfoAnuncio` | `nAnuncio`, `nifEntidade`, `IdIncm`, `numDias`, `CPV`, `Ano` |
| Modificações | `GET /APIBase2/GetInfoModContrat` | `idContrato`, `Ano` |
| Entidades | `GET /APIBase2/GetInfoEntidades` | `nifEntidade` |

**Documentado:** pelo menos um parâmetro de consulta é obrigatório. `numDias`
aceita 1 a 90 segundo o WADL. No recurso de anúncios, `CPV` aceita de um a oito
caracteres como pesquisa por prefixo e deve ser combinado com outro parâmetro.

**Documentado:** a representação de sucesso é JSON. Não estão documentados:

- paginação;
- ordenação;
- cursor;
- limite máximo de registos;
- tamanho máximo da resposta;
- compressão;
- rate limit numérico;
- validade/rotação do token;
- política de versões da API.

### 5.3. Erros observados

Pedido pequeno, sem token:

```http
GET /APIBase2/GetInfoContrato?idContrato=12345
```

Resposta real:

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8

The Token is required.
```

**Observado:** a falha de autenticação não usou 401/403 nem JSON. Um cliente
não pode considerar todo o HTTP 200 como sucesso de dados.

### 5.4. Contradições na documentação da API

Foram encontradas contradições explícitas:

1. O WADL declara `resources base="https://www.base.gov.pt"` e caminhos como
   `/GetInfoContrato`; esse URL devolveu 404. O caminho com `/APIBase2`
   respondeu.
2. O endpoint é apresentado como `GetInfoModContrat`, mas o exemplo `curl` usa
   `GetInfoModContrato`.
3. A secção de entidades contém a descrição copiada de modificações
   contratuais.
4. O exemplo de resposta não é JSON válido: faltam vírgulas entre vários
   elementos.
5. O WADL tipa `idContrato` e `IdProcedimento` como inteiros; os downloads e o
   próprio exemplo JSON devolvem-nos como strings.
6. O exemplo HTML apresenta preços e prazos como strings; o dataset atual de
   contratos usa números JSON para preços e inteiro para `prazoExecucao`.
7. A lista de “response codes” mistura estados HTTP com mensagens textuais; a
   resposta sem token confirmou HTTP 200 com mensagem de erro.
8. Uma página mais antiga do portal diz que a API estará disponível “em
   breve”, enquanto a notícia de 2025 e a API operacional confirmam que já foi
   lançada.

**Inferência:** a documentação é útil para descoberta, mas não constitui um
schema executável fiável. Qualquer integração futura exigirá fixtures reais
obtidas com acesso autorizado.

## 6. Objetos e relações

### 6.1. Objetos confirmados

| Objeto | Evidência pública |
|---|---|
| Contrato | Pesquisa, detalhe, API e downloads anuais. |
| Procedimento | Modelo legal e `idprocedimento` nos contratos; não existe endpoint público dedicado na API documentada. |
| Anúncio | Pesquisa, API e downloads anuais; anúncios nacionais têm ligação ao PDF do DRE. |
| Entidade | Pesquisa, API e snapshot agregado no dados.gov.pt. |
| Modificação contratual | Pesquisa, API e downloads anuais. |
| Lote | Modelo legal; listas embebidas nos downloads de contratos e anúncios. |
| Acordo-quadro | Campos no contrato e filtro da API; não foi observado como recurso autónomo. |
| Execução | Modelo legal; parte dos resultados é incorporada no registo do contrato, como fecho e preço total efetivo. |
| Documento | Contratos/anexos e ligações para peças são publicitados; não existe endpoint documental descrito na API pública. |
| Não celebração e impugnação | Interface pública e modelos legais; não aparecem como recursos da API oficial documentada. |

### 6.2. Relações observadas ou documentadas

```text
procedimento -> contrato
anúncio -> procedimento/contrato
contrato -> entidade adjudicante
contrato -> adjudicatário(s)
contrato -> CPV(s)
contrato -> local(is) de execução
contrato -> lote(s)
contrato -> modificação(ões)
contrato -> dados de execução
```

Cardinalidades:

- **Observado:** um `idprocedimento` aparece em vários contratos. Numa amostra
  parcial, um procedimento apareceu em 14 contratos.
- **Observado:** o mesmo `nAnuncio`/`idINCM` aparece em vários contratos.
- **Observado:** um contrato pode ter vários adjudicatários.
- **Documentado:** entidades adjudicantes e adjudicatários são repetíveis nos
  modelos legais, mesmo que a pequena amostra de contratos tivesse uma única
  entidade adjudicante por registo.
- **Observado:** um contrato pode ter várias localizações e vários lotes.
- **Observado:** um contrato pode ter várias modificações; o ficheiro repete o
  mesmo `idcontrato` em linhas distintas.
- **Documentado:** CPV é repetível e o modelo distingue objeto principal e
  secundário. O download achatado não conserva essa distinção.

Não foi observada uma chave de lote que permita relacionar, no download
achatado, cada adjudicatário, CPV, preço e localização com o lote específico.

## 7. Identificadores externos

**Inferência:** todos os identificadores abaixo devem ser interpretados no contexto do BASE e
preservados como strings.

| Campo | Objeto | Forma observada | Nota |
|---|---|---|---|
| `idcontrato` | Contrato | Dígitos em string, por exemplo `12380006` | Identificador de ligação usado também nas modificações. |
| `idprocedimento` | Procedimento | Dígitos em string, por exemplo `8111559` | Um procedimento pode originar vários contratos. |
| `nAnuncio` | Anúncio | String como `1/2026`; pode ser vazia no contrato | Número público do anúncio. |
| `IdIncm`/`idINCM` | Anúncio | Dígitos em string, por exemplo `419938349` | A capitalização varia entre recursos/documentação. |
| `nifEntidade` | Entidade | NIF/NIPC em string ou marcador `-` | Não identifica todas as entidades. |
| `numAcordoQuadro` | Acordo-quadro | String ou string vazia | Sem formato estável confirmado. |
| ID de recurso dados.gov.pt | Recurso de download | UUID | Identifica o recurso de distribuição, não um registo BASE. |

**Observado:** URLs da pesquisa pública incluem ainda parâmetros como
`actoid`, `adjudicatariaid` e `id` de detalhe. A sua semântica e estabilidade
não estão documentadas. Não devem ser promovidos a identificadores externos
sem confirmação.

**Documentado/observado:** embora alguns modelos legais e o WADL chamem
“numérico” ao identificador, o formato distribuído usa strings. Não se deve:

- converter para inteiro;
- remover zeros;
- acrescentar padding;
- deduzir uma hierarquia pelo comprimento;
- equiparar `idINCM`, `nAnuncio`, `idprocedimento` e `idcontrato`.

Não foi encontrada uma garantia formal de imutabilidade ou não reutilização
destes identificadores.

## 8. Contratos

### 8.1. Contrato observável do download JSON

**Observado:** o recurso `contratos2026.zip`, modificado em 20 de setembro de 2026, tinha:

- 41 046 395 bytes comprimidos;
- um único ficheiro `Contratos2026.json`;
- 311 842 762 bytes declarados para o JSON descomprimido.

A amostra parcial continha 277 registos completos. Não é aleatória nem
representativa do universo; serve apenas para confirmar forma, tipos e casos
limite.

| Campo original | Tipo observado | Significado/limitação |
|---|---|---|
| `idcontrato` | string | Identificador do contrato. |
| `nAnuncio` | string | Número de anúncio; frequentemente vazio quando não existe anúncio associado. |
| `TipoAnuncio` | string | Tipo de anúncio; pode ser vazio. |
| `idINCM` | string | Identificador INCM; pode ser vazio. |
| `tipoContrato` | array[string] | Um ou mais tipos de contrato. |
| `idprocedimento` | string | Identificador do procedimento. |
| `tipoprocedimento` | string | Designação do tipo de procedimento. |
| `objectoContrato` | string | Objeto do contrato; a chave mantém a ortografia original. |
| `descContrato` | string | Descrição do contrato; pode repetir o objeto. |
| `adjudicante` | array[string] | Valores compostos como `NIPC - nome`. |
| `adjudicatarios` | array[string] | Um ou mais valores compostos como `NIF/NIPC - nome`. |
| `dataPublicacao` | string | Data em `DD/MM/AAAA`; sem definição técnica suficiente para assumir que é sempre a publicação do contrato. |
| `dataCelebracaoContrato` | string | Data de celebração em `DD/MM/AAAA`. |
| `precoContratual` | number | Preço contratual; o modelo legal define preço contratual sem IVA, em euros. |
| `cpv` | array[string] | Código e designação CPV concatenados. |
| `prazoExecucao` | integer | Prazo, aparentemente em dias; a API de exemplo usa string. |
| `localExecucao` | array[string] | Localizações textuais compostas. |
| `fundamentacao` | string | Fundamentação legal do procedimento. |
| `ProcedimentoCentralizado` | string | Valor textual, observado como `Sim`/`Não`. |
| `numAcordoQuadro` | string | Número do acordo-quadro ou string vazia. |
| `DescrAcordoQuadro` | string | Descrição ou string vazia. |
| `precoBaseProcedimento` | number | Preço base; o modelo legal define preço base sem IVA, em euros. |
| `dataDecisaoAdjudicacao` | string | Data de decisão em `DD/MM/AAAA`. |
| `dataFechoContrato` | string | Data de fecho ou string vazia. |
| `PrecoTotalEfetivo` | number | Resultado comunicado na execução; sem estado associado no download. |
| `regime` | string | Regime legal textual. |
| `justifNReducEscrContrato` | array[string] ou null | Justificação para não redução a escrito. |
| `tipoFimContrato` | string | Causa/tipo de fim ou string vazia. |
| `CritMateriais` | string | Indicador textual de critérios relativos a materiais. |
| `concorrentes` | array[string] ou null | Lista composta por NIF/NIPC e nome. |
| `linkPecasProc` | string | URL das peças na plataforma eletrónica ou vazio. |
| `Observacoes` | string | Texto livre, frequentemente vazio. |
| `ContratEcologico` | string | Indicador textual. |
| `Ano` | integer | Ano de agrupamento do recurso; sem definição técnica encontrada. |
| `fundamentAjusteDireto` | string | Fundamentação adicional ou vazio. |
| `adjudicatarioPMEs` | array[string] ou null | Identificadores dos adjudicatários assinalados como PME; pode conter `-`. |
| `NUTs` | array[string] ou null | Código e designação NUTS concatenados. |
| `Lotes` | array[string] ou null | Designações de lotes sem identificador estruturado no download. |
| `TipoCriterioAdjudicacao` | string | Exemplo: `Monofator` ou `Multifator`; pode ser vazio. |

### 8.2. Campos documentados mas não expostos integralmente

**Documentado:** o Anexo X da Portaria define um modelo mais rico, com referência interna,
proposta, detalhe de lotes, linhas de artigo, datas de produção de efeitos,
país das entidades, distinção de CPV principal/secundário, localização por
lote e outros campos públicos e reservados.

**Observado:** o download anual não preserva toda essa estrutura. A ausência de
um campo no download não prova que o BASE não o recolha nem que não o mostre no
detalhe web.

### 8.3. Estado e documentos

**Observado:** não existe um campo `estado` na amostra do download. `dataFechoContrato` e
`tipoFimContrato` podem estar vazios e `PrecoTotalEfetivo` pode ser zero.

**Inferência:** derivar um estado apenas destes campos seria prematuro. Um zero
pode representar um valor real ou um default anterior ao relatório de
execução.

**Observado:** os dados contêm links para peças do procedimento, mas não uma lista
estruturada de contratos assinados, anexos, aditamentos e respetivos hashes.

**Documentado:** esses documentos podem aparecer na interface pública e têm regras próprias de
proteção de segredos e dados pessoais.

## 9. Entidades adjudicantes e adjudicatários

### 9.1. Representação nos contratos

**Observado:** nos contratos, entidades e concorrentes surgem como arrays de strings
compostas:

```json
{
  "adjudicante": [
    "501102752 - Município de Amarante"
  ],
  "adjudicatarios": [
    "516068121 - Tek4life SA"
  ]
}
```

O delimitador também pode ocorrer em nomes. Quando não há NIF/NIPC, surgem
valores como:

```json
{
  "adjudicatarios": [
    "- - EBSCO Information Services S.L.U."
  ]
}
```

**Inferência:** não é seguro separar a string apenas em todos os caracteres `-`.

### 9.2. Dataset de entidades

**Observado:** o snapshot `entidades.json` tinha 50 877 058 bytes e os campos:

| Campo | Tipo observado | Nota |
|---|---|---|
| `nifEntidade` | string | NIF/NIPC ou `-`. |
| `desigEntidade` | string | Designação comunicada. |
| `numContratos` | integer | Contagem agregada. |
| `totAdjudicatario` | integer | Contagem como adjudicatário. |
| `totValorContratIni` | number | Total agregado de valor contratual inicial. |
| `totAdjudicante` | integer | Contagem como adjudicante. |
| `totAdjudicanteValorContratIni` | number | Total agregado como adjudicante. |
| `descPais` | string | País textual, por vezes vazio. |
| `AliasPais` | string | Código de país, por vezes vazio. |

**Observado:** o dataset é uma agregação, não um cadastro canónico com
identificador interno e histórico de nomes.

Casos observados na pequena amostra:

- muitas entidades têm `nifEntidade: "-"`;
- a mesma organização plausível aparece com grafias diferentes;
- existem espaços adicionais, abreviaturas, acentos e erros ortográficos;
- nomes como `não adjudicado` e `sem adjudicação` aparecem como entidades;
- o mesmo nome ou variante pode estar associado a país diferente ou vazio;
- organizações estrangeiras podem não ter identificador fiscal publicado.

Exemplo real minimizado de variação, todos com NIF `-`:

```text
CALDERYS IBERICA REFRACTARIOS, S.A.
CALDERYS IBÉRICA REFRACTÁRIOS, S.A.
CALDERYS IBÉRICA REFRACTARIOS, S.A.
```

Isto demonstra que igualdade ou semelhança de nome não é identidade provada.

### 9.3. Múltiplos adjudicatários e agrupamentos

**Observado:** um contrato pode conter vários adjudicatários. A pequena amostra
incluiu dois contratos com mais de um adjudicatário.

**Documentado:** os modelos legais incluem um indicador de agrupamento.
**Observado:** esse indicador não existe como campo separado no download
achatado. Vários adjudicatários não devem ser classificados automaticamente
como consórcio ou agrupamento.

**Inferência:** o dataset não permite reconstruir com segurança alterações de designação,
fusões ou sucessões jurídicas. Não é proposta nesta fase qualquer resolução
automática de entidades.

## 10. Valores monetários

### 10.1. Conceitos distintos

| Conceito | Campo observado | Semântica documentada |
|---|---|---|
| Preço base do procedimento | `precoBaseProcedimento` / `PrecoBase` | Limite/preço base, sem IVA, em euros, nos modelos aplicáveis. |
| Preço contratual | `precoContratual` | Preço contratual sem IVA, em euros. |
| Preço após alteração | `modifContratoPrecoAlterado` | O Anexo XII chama-lhe “Preço após alteração contratual s/IVA (€)”. |
| Preço total efetivo | `PrecoTotalEfetivo` | Campo do relatório de execução, distinto do preço contratual inicial. |
| Totais de entidade | `totValorContratIni`, `totAdjudicanteValorContratIni` | Agregados do valor contratual inicial no snapshot de entidades. |

Estes conceitos não são intermutáveis nem devem ser somados sem uma definição
específica.

### 10.2. Tipos e formatos

**Observado:** no JSON atual de contratos, preços são números JSON com ponto
decimal. No exemplo da documentação da API são strings com vírgula decimal,
como `"105000,00"`.

**Observado:** em anúncios, `PrecoBase` é string e pode conter um número com
ponto decimal ou a palavra `"Inexistente"`.

**Observado:** na amostra parcial de 277 contratos:

- `precoContratual` variou entre `44.5` e `6034158.19`;
- `precoBaseProcedimento` incluiu zero;
- `PrecoTotalEfetivo` foi zero em 255 registos, quase sempre com data de fecho
  vazia;
- não foram encontrados valores negativos.

A amostra não demonstra que valores negativos sejam impossíveis.

Não existe campo de moeda no JSON observado. A moeda EUR e a exclusão de IVA
decorrem dos modelos legais para preço base, preço contratual e preço após
alteração. A semântica de IVA do `PrecoTotalEfetivo` não ficou confirmada nas
fontes consultadas.

**Inferência:** precisão decimal é necessária numa persistência futura, mas
este documento não escolhe o tipo físico. O valor bruto e o conceito monetário
devem permanecer distinguíveis.

### 10.3. Modificações

**Documentado:** `modifContratoPrecoAlterado` não deve ser interpretado como montante acrescido
ou reduzido. O nome legal correspondente indica o preço do contrato após a
alteração.

**Observado:** o mesmo contrato pode surgir várias vezes com diferentes preços
alterados. Somar esses valores produziria um resultado sem significado.

## 11. Temporalidade

### 11.1. Conceitos temporais documentados

**Documentado:** os modelos e regras do BASE distinguem:

- data do anúncio/publicação;
- data da decisão de adjudicação;
- data da celebração;
- data de produção de efeitos;
- data de início de execução;
- prazo/duração;
- data do ato de modificação;
- data de publicação da modificação;
- fecho físico;
- fecho financeiro;
- data de pagamento;
- data de submissão/correção do bloco.

Não devem ser condensados num único campo `date`.

### 11.2. Formatos observados

| Recurso | Campo | Formato observado |
|---|---|---|
| Contrato | `dataPublicacao` | `DD/MM/AAAA` |
| Contrato | `dataCelebracaoContrato` | `DD/MM/AAAA` |
| Contrato | `dataDecisaoAdjudicacao` | `DD/MM/AAAA` |
| Contrato | `dataFechoContrato` | `DD/MM/AAAA` ou string vazia |
| Modificação | `modifContratoData` | `DD/MM/AAAA 00:00:00` |
| Modificação | `modifDataPublicacao` | `DD/MM/AAAA 00:00:00` |
| Anúncio | `dataPublicacao` | `DD/MM/AAAA` |
| Anúncio | `DataLimitePropostas` | `DD/MM/AAAA` ou string vazia |
| Metadado dados.gov.pt | `last_modified` | ISO 8601 com offset UTC |

Não foi publicada informação de timezone nos campos de negócio. A componente
`00:00:00` das modificações não prova precisão horária.

**Observado:** `prazoExecucao` é inteiro no download de contratos, mas
`modifPrazoExecucao` é string no download de modificações. O modelo legal usa
prazo/duração, com dias em alguns relatórios.

**Observado:** existem contratos no recurso de 2026 com `dataPublicacao` em
2025 e `dataCelebracaoContrato` em 2026. A documentação da API não define o
campo com detalhe suficiente para concluir se `dataPublicacao` é a publicação
do contrato, do procedimento ou outra publicação associada.

`Ano` agrupa os recursos e é inteiro, mas a regra exata para o seu cálculo não
foi encontrada. Não deve ser assumido como sinónimo de todas as datas acima.

## 12. Geografia

### 12.1. Campos observados

**Observado:** os contratos expõem:

```json
{
  "localExecucao": [
    "Portugal, Porto, Porto"
  ],
  "NUTs": [
    "PT11A - Área Metropolitana do Porto"
  ]
}
```

Outras formas observadas:

```text
Portugal
Portugal, Faro
Portugal, Portugal Continental
Portugal, Guarda, Trancoso
PT150 - Algarve
PTZZZ - Extra-Regio NUTS 3 (Todos)
```

`localExecucao` é sempre um array na pequena amostra, mesmo com um só local.
`NUTs` pode ser `null` apesar de existir uma localização textual.

### 12.2. Modelo legal e perda no download

**Documentado:** os modelos legais podem recolher país, NUTS III, localidade,
distrito, concelho, freguesia e serviços do local de execução, incluindo
associação ao lote.

**Observado:** o download de contratos reduz essa estrutura a strings
compostas e a uma lista NUTS opcional. Não publica códigos de distrito,
município ou freguesia em campos separados.

**Observado:** a pequena amostra contém localizações repetidas exatamente no
mesmo array. Em 23 dos 277 registos existia pelo menos uma repetição.

Não foi confirmada qualquer equivalência entre os nomes do BASE e códigos INE,
CAOP ou geografias estudadas noutras fontes. O código `PT11A` é NUTS, não um
código municipal. A versão NUTS não aparece no registo.

**Inferência:** análises territoriais são possíveis, mas exigirão preservação
da string original e correspondências externas explícitas e versionadas. Uma
localização pode ser nacional, regional, distrital, municipal ou mais vaga.

## 13. CPV e outras classificações

**Documentado:** o BASE usa o Vocabulário Comum para os Contratos Públicos
(CPV), instituído pelo Regulamento (CE) n.º 2195/2002 e revisto, nomeadamente,
pelo Regulamento (CE) n.º 213/2008.

**Observado:** o formato encontrado nos downloads foi:

```text
72210000-0 - Serviços de programação de pacotes de software
```

O código tem oito dígitos e dígito de controlo após hífen. A designação vem
concatenada no mesmo texto no download.

**Documentado:** o modelo legal distingue:

- vocabulário principal e suplementar;
- objeto principal e secundário;
- CPV de contrato e CPV por lote;
- valor associado em alguns blocos.

**Observado:** `cpv` e `CPVs` são arrays, mas a amostra achatada não expõe a
versão, o papel principal/secundário, o vocabulário suplementar nem a ligação
ao lote.

**Documentado:** o filtro `CPV` da API de anúncios aceita prefixos de um a oito
caracteres, desde que acompanhado por outro parâmetro. Isso descreve a pesquisa
da API, não autoriza truncar o código armazenado nem construir uma hierarquia
sem a classificação oficial.

Outras classificações observadas incluem tipos de procedimento, tipos de
contrato, critérios de adjudicação, fundamentos legais e códigos de país. As
versões das respetivas listas não aparecem nos downloads.

## 14. Exemplos reais minimizados

**Observado:** os exemplos seguintes foram reduzidos a campos necessários para demonstrar o
comportamento. Mantêm valores reais da amostra oficial.

### 14.1. Contrato fechado com três conceitos monetários

```json
{
  "idcontrato": "12380006",
  "idprocedimento": "8111559",
  "objectoContrato": "Aquisição de bens - Computador e Telemóvel",
  "adjudicante": [
    "501102752 - Município de Amarante"
  ],
  "adjudicatarios": [
    "516068121 - Tek4life SA"
  ],
  "dataCelebracaoContrato": "02/01/2026",
  "dataFechoContrato": "27/03/2026",
  "precoBaseProcedimento": 2606.67,
  "precoContratual": 2606.0,
  "PrecoTotalEfetivo": 2606.0,
  "localExecucao": [
    "Portugal"
  ],
  "NUTs": [
    "PT11C - Tâmega e Sousa"
  ]
}
```

Os três valores não devem ser fundidos apesar de dois coincidirem.

### 14.2. Contrato com vários adjudicatários

```json
{
  "idcontrato": "12026866",
  "idprocedimento": "7926801",
  "tipoContrato": [
    "Aquisição de bens móveis"
  ],
  "adjudicatarios": [
    "514181435 - GROWSKILLS UNIPESSOAL, LDA",
    "504615947 - 1 - MEO - SERVIÇOS DE COMUNICAÇÕES E MULTIMÉDIA, S.A."
  ],
  "precoContratual": 120310.0,
  "localExecucao": [
    "Portugal, Braga, Vila Verde"
  ]
}
```

O segundo nome contém hífenes adicionais, demonstrando o risco de parsing por
separador simples.

### 14.3. Anúncio cujo preço base não é numérico

```json
{
  "nAnuncio": "100/2026",
  "IdIncm": "419944967",
  "tipoActo": "Anúncio de Alteração",
  "PrecoBase": "Inexistente",
  "dataPublicacao": "05/01/2026",
  "CPVs": [
    "30230000-0 - Equipamento informático"
  ]
}
```

`PrecoBase` não pode ser convertido cegamente em decimal.

### 14.4. Duas modificações do mesmo contrato

```json
[
  {
    "idcontrato": "12430731",
    "modifContratoData": "21/04/2026 00:00:00",
    "modifContratoPrecoAlterado": 38015.43,
    "modifDataPublicacao": "05/05/2026 00:00:00"
  },
  {
    "idcontrato": "12430731",
    "modifContratoData": "04/05/2026 00:00:00",
    "modifContratoPrecoAlterado": 38015.43,
    "modifDataPublicacao": "27/07/2026 00:00:00"
  }
]
```

Não existe um `idmodificacao` nestes registos. Os campos publicados podem não
ser suficientes para construir uma identidade estável da modificação.

## 15. Nulos, inconsistências e casos limite

### 15.1. Ausência heterogénea

**Observado:** foram encontradas quatro formas diferentes de ausência:

- `null`, por exemplo em `NUTs`, `Lotes` e `concorrentes`;
- string vazia, por exemplo em `nAnuncio`, `dataFechoContrato` e
  `numAcordoQuadro`;
- marcador `"-"`, sobretudo em NIF/NIPC;
- texto sem valor numérico, como `"Inexistente"` em `PrecoBase`.

Estas formas não são semanticamente equivalentes.

### 15.2. Inconsistências observadas

- `objectoContrato` usa grafia antiga e capitalização de chaves não uniforme.
- `IdIncm` nos anúncios e `idINCM` nos contratos diferem em capitalização.
- os downloads JSON e o exemplo da API divergem nos tipos de preços, prazos e
  ano;
- alguns textos preservam entidades HTML, por exemplo `&amp;`;
- `objectoContrato` e `descContrato` podem ser iguais;
- `localExecucao` pode repetir o mesmo valor;
- NUTS pode estar ausente quando existe localização textual;
- `PrecoTotalEfetivo` pode ser zero em contratos sem fecho comunicado;
- a mesma entidade aparece com grafias e países divergentes;
- existem entidades agregadas com nomes que representam estados do processo,
  como `não adjudicado`;
- datas de publicação de alguns contratos antecedem a celebração por vários
  meses, sem definição suficiente do campo;
- vários registos de modificação podem partilhar contrato, fundamento, prazo e
  preço, mas ter datas diferentes;
- não existe ID próprio da modificação no download;
- lotes são designações livres e podem conter valores monetários no texto;
- a pequena amostra observou preço base zero, mas não preço contratual negativo.

### 15.3. Contradições entre canais oficiais

- A API documenta tipos diferentes dos downloads que, segundo o portal,
  deveriam ter os mesmos campos.
- O WADL aponta para caminhos que devolveram 404 sem o prefixo `/APIBase2`.
- A página institucional antiga ainda anuncia a API como futura, mas a API foi
  lançada em 2025.
- O metadado `temporal_coverage` dos datasets de contratos, anúncios e
  modificações começa em 2024, apesar de existirem recursos desde 2012.
- No dataset de contratos, `last_update` estava em 23 de agosto de 2026,
  enquanto `last_modified` e os recursos eram de 20 de setembro de 2026.
- O dataset atual usa licença `other-pd` (“Outra - Domínio Público”), mas um
  dataset anterior de “Transparência” declarava CC BY 4.0.

Estas divergências devem ser conservadas como factos de proveniência, não
silenciosamente reconciliadas.

## 16. Atualizações e histórico

### 16.1. Correções na origem

**Documentado:** uma entidade adjudicante pode pedir correção ou anulação de um
bloco já submetido. Quando autorizada, a edição dá origem a uma nova versão. O
IMPIC também pode pedir correções de incorreções ou incoerências.

**Documentado:** o portal recebe um relatório de alteração/anulação. Os
anúncios de retificação e alterações provenientes das plataformas podem ser
validados e publicitados automaticamente.

**Documentado:** não é possível introduzir ou alterar dados cujo primeiro bloco
tenha sido introduzido há mais de dez anos. A informação pública também tem uma
janela de visibilidade de dez anos, após a qual o acesso depende de autorização
e pode envolver taxa.

### 16.2. Modificações contratuais

**Documentado:** modificação contratual e correção de dados são conceitos distintos:

- a modificação representa uma alteração material/jurídica do contrato;
- a correção altera um bloco comunicado incorretamente.

**Observado:** modificações são distribuídas como registos separados ligados
por `idcontrato`. Os campos atuais são:

```text
idcontrato
modifContratoFundamento
modifContratoTipoAto
modifContratoData
modifContratoPrecoAlterado
modifPrazoExecucao
modifDataPublicacao
Ano
```

**Documentado:** o modelo legal de modificação é mais rico e inclui preço antes
e depois, entidades, CPV, local, lotes e outras alterações. O download atual
não expõe toda essa estrutura.

### 16.3. Deteção pública de alterações

**Observado:** o dados.gov.pt publica `last_modified`, tamanho e checksum SHA-1
por recurso. Estes elementos permitem detetar que um snapshot anual mudou.

Não foi observado:

- timestamp de última atualização por contrato;
- número público da versão de um contrato;
- histórico de versões dentro do JSON anual;
- indicador de registo corrigido/anulado;
- feed incremental de alterações;
- identificador próprio de cada modificação contratual.

**Inferência:** comparar snapshots pode revelar diferenças, mas não permite
atribuir automaticamente cada diferença a correção, anulação, execução ou
modificação jurídica.

## 17. Limites técnicos

### 17.1. API

| Tema | Resultado |
|---|---|
| Autenticação | Token obrigatório, sujeito a pedido e autorização. |
| Atualização | **Documentado:** diária. |
| Filtros | Pelo menos um obrigatório; `numDias` limitado a 90. |
| Paginação | Não documentada. |
| Ordenação | Não documentada. |
| Limite de registos | Não documentado para a API. |
| Rate limit | Não documentado. |
| Timeout/SLA | Não documentado. |
| Erros | **Observado:** token ausente devolve HTTP 200 `text/plain`. |
| Versão | O nome `APIBase2` sugere uma geração, mas não há política de versão documentada. |

Não foi pedido um token e não foram efetuadas consultas autenticadas. Portanto,
o shape real de sucesso da API não foi confirmado diretamente.

### 17.2. Downloads

Tamanhos observados em 20 de setembro de 2026:

| Recurso | Tamanho |
|---|---:|
| Contratos 2026 ZIP | 41 046 395 bytes |
| JSON interno de contratos 2026 | 311 842 762 bytes descomprimidos |
| Anúncios 2026 JSON | 21 328 893 bytes |
| Modificações 2026 JSON | 1 154 105 bytes |
| Entidades JSON | 50 877 058 bytes |

**Observado:** os servidores do dados.gov.pt suportaram HTTP Range com resposta
206. Nenhum dos ficheiros completos foi descarregado.

**Documentado:** os downloads têm frequência semanal. Não foi encontrada uma
garantia de dia/hora de publicação nem retenção de snapshots anteriores.

### 17.3. Portal público

**Observado:** na data da análise, pedidos diretos à raiz e a páginas Base4
devolveram 404 após um redirecionamento para `/base4`, enquanto a API, o WADL,
os ficheiros e as páginas indexadas continuavam acessíveis. Pode tratar-se de
uma falha transitória ou de encaminhamento; não foi tentado contorná-la.

Não foi observado rate limiting nem mecanismo anti-bot nos poucos pedidos
sequenciais. Isto não demonstra ausência de limites.

## 18. Licença e reutilização

**Documentado:** a Portaria n.º 318-B/2023 determina que os dados de natureza
pública são passíveis de extração automática, gratuita e em formatos abertos,
através do BASE e de outros portais públicos.

**Observado:** os quatro datasets atuais do dados.gov.pt declaram a licença
`other-pd`, apresentada como “Outra (Domínio Público)”.

**Observado:** um dataset anterior, “Contratos Públicos - Portal BASE - IMPIC
(Transparência)”, declarava CC BY 4.0. O rodapé do Portal BASE apresenta
“Todos os direitos reservados”.

Estas declarações não são equivalentes. A legislação sobre acesso gratuito e
formato aberto também não substitui uma licença de reutilização específica.

Não foi encontrada uma licença única e inequívoca que cubra simultaneamente:

- interface web;
- respostas da API;
- datasets atuais;
- documentos anexos;
- conteúdo proveniente do DRE, SIMAP e plataformas eletrónicas.

**Inferência:** a licença deve ser avaliada por recurso. Para os downloads
atuais, o metadado de domínio público é a declaração mais específica
encontrada, mas a categoria “Outra” e as divergências históricas justificam
confirmação junto do IMPIC antes de redistribuição em massa.

Independentemente da licença, a proveniência deve identificar Portal BASE,
IMPIC, entidade comunicante, recurso, data de extração e origem do anúncio ou
bloco. Documentos associados podem conter direitos de terceiros e dados
pessoais; não devem herdar automaticamente a licença do dataset tabular.

## 19. Relevância para o PTScope

**Inferência:** o Portal BASE disponibiliza matéria-prima relevante para:

- valor contratado por entidade, período, CPV e local de execução;
- evolução de preço base, preço contratual e preço total efetivo, mantendo os
  conceitos separados;
- distribuição por tipo de procedimento e tipo de contrato;
- análise de entidades adjudicantes e adjudicatários;
- concentração observada de fornecedores, com cautela na identidade;
- contratação por CPV;
- contratos com vários adjudicatários, lotes ou localizações;
- relação entre procedimento, anúncio e contratos;
- modificações contratuais e diferença entre data do ato e publicação;
- cobertura e qualidade de informação territorial;
- futura construção de indicadores de risco ou integridade.

**Observado/inferência:** as limitações centrais para uso territorial e analítico são:

- a localização é frequentemente textual, agregada ou ausente;
- a versão NUTS não é indicada;
- não existem códigos municipais separados no download;
- entidades sem NIF/NIPC e variantes de nome impedem identidade automática;
- lotes e relações internas são achatados;
- o histórico de correções não é público no snapshot;
- a API exige autorização e tem contrato técnico incompleto;
- os downloads são snapshots grandes, não feeds incrementais;
- valores zero e campos vazios não têm sempre estado explicativo;
- licenciamento não é uniforme entre canais.

O BASE permite observar padrões, mas não autoriza classificar um contrato como
corrupto, fraudulento ou irregular. Qualquer indicador futuro de risco terá de
ter definição explícita, evidência, tratamento de falsos positivos e
metodologia auditável.

Este estudo não decide qual fonte deve prevalecer em divergências. Um valor do
BASE deve conservar o seu contexto, definição e proveniência até existir uma
política de reconciliação separada.

## 20. Questões abertas

Antes de implementar uma integração, permanecem por esclarecer:

1. Qual é a URL base normativa da API, dado o erro no `base` do WADL?
2. Qual é a grafia válida do endpoint de modificações:
   `GetInfoModContrat` ou `GetInfoModContrato`?
3. Qual é o schema JSON real de sucesso de cada endpoint autenticado?
4. A API devolve arrays, objetos ou envelopes de paginação?
5. Existem paginação, ordenação, cursor, limite de linhas ou tamanho máximo?
6. Quais são os rate limits, validade do token e regras de rotação?
7. Como são representados erros de parâmetros, ausência de dados e falhas
   internas, para além do erro de token observado?
8. Existe documentação de versão e compatibilidade da API?
9. O que significa exatamente `dataPublicacao` no dataset de contratos?
10. Qual é a regra de atribuição de `Ano` ao contrato e à modificação?
11. `PrecoTotalEfetivo = 0` significa zero real, ausência de execução ou valor
    ainda não comunicado em cada estado?
12. O `PrecoTotalEfetivo` inclui ou exclui IVA?
13. Existe moeda diferente de EUR em algum registo e como é representada?
14. Valores monetários negativos são permitidos em modificações ou execução?
15. Como se identifica de forma estável uma modificação contratual sem ID
    próprio no download?
16. Como são expostas correções/anulações e versões anteriores na área pública
    ou API?
17. Existe uma data de última atualização por contrato ou entidade?
18. Os snapshots semanais são completos e substitutivos ou podem omitir
    registos temporariamente?
19. Qual é a semântica exata dos totais no dataset de entidades e o respetivo
    período de cobertura?
20. Existe um identificador público estável de entidade além do NIF/NIPC?
21. Como são representados agrupamentos, consórcios, cessões e mudanças de
    designação nos downloads?
22. Como ligar lotes a adjudicatários, CPV, preço e local após o achatamento?
23. Que versão NUTS é usada em cada ano e como são comunicadas alterações de
    classificação?
24. Existe atualmente um recurso público estruturado de locais de execução que
    forneça códigos territoriais e chaves de ligação não presentes no contrato?
25. Qual é a classificação oficial aplicável a tipos de procedimento,
    contrato, fundamento e fim, e como é versionada?
26. Os CPV no download preservam a distinção principal/secundário noutro
    recurso público?
27. Qual é a licença explícita da API e dos downloads atuais, para além do
    marcador `other-pd`?
28. Os documentos anexos têm condições de reutilização próprias?
29. O acesso a registos com mais de dez anos pode ser autorizado para
    investigação e em que condições/taxa?
30. Quando estará estável o encaminhamento da interface Base4 observado como
    404 na data da análise?

**Inferência:** o Portal BASE é uma fonte oficial, ampla e indispensável sobre
contratação pública, mas o contrato público de dados é heterogéneo. A melhor
descrição observável combina os modelos legais, a API autorizada e os snapshots
semanais. Nenhum destes canais, isoladamente, preserva toda a semântica do
sistema de origem.
