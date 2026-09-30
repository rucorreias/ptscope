# Modelo de domínio da v0.1

> **Rascunho de arquitetura (30-09-2026).** Este documento explica os dados e as suas relações. Ainda não define tabelas, modelos Pydantic ou endpoints. Falta confirmar a série do INE ([#1](https://github.com/rucorreias/ptscope/issues/1)) e a correspondência dos municípios entre fontes ([#2](https://github.com/rucorreias/ptscope/issues/2)). O contrato da API e o dashboard serão fechados na [#3](https://github.com/rucorreias/ptscope/issues/3).

## O que queremos responder e o que sabemos

A pergunta da v0.1 é: **como evoluiu a população residente de um município nos períodos que conseguimos confirmar?** Vamos obter estatísticas do **INE** e informação municipal e geometrias da **GEO API PT**. A GEO API PT indica a CAOP 2024.1, da DGT, como origem dos seus dados administrativos. Na v0.1, consultamos a GEO API PT; não está prevista uma integração direta com a DGT.

O [estudo INE](../data/sources/ine.md#61-indicador-0008273) preserva uma
observação real, filtrada, do Porto em 2023 e a metainformação do indicador
[`0008273`](../data/code-dictionary.md#ine-indicator-0008273): NUTS 2013, nota geográfica CAOP 2020 e quebra metodológica
2020–2021. O [estudo GEO API
PT](../data/sources/geoapi.md#5-resposta-real-de-municipioporto) preserva
[`dtmn="1312"`](../data/code-dictionary.md#geoapi-municipality-1312) e uma Feature `geojson` do Porto. A [página oficial da GEO
API PT](https://geoapi.pt/) identifica a CAOP 2024.1 como origem da informação
administrativa. Estes exemplos não provam que as geometrias de CAOP 2020 e CAOP 2024.1 sejam iguais, nem que exista uma regra aplicável a todos os municípios para relacionar os códigos.

O catálogo oficial de dados públicos
identifica [`0012918`](../data/code-dictionary.md#ine-indicator-0012918) ([entrada oficial](https://dados.gov.pt/pt/datasets/populacao-residente-n-o-64))
como indicador anual de população por NUTS 2024, sexo e grupo etário. A
metainformação e as observações deste indicador ainda não foram obtidas
diretamente na investigação atual; cobertura municipal, períodos e
comparabilidade com [`0008273`](../data/code-dictionary.md#ine-indicator-0008273) permanecem por verificar.

## Conceitos usados no projeto

| Conceito | Significado no PTScope v0.1 | Limite |
| --- | --- | --- |
| **Fornecedor técnico** | API que nos entrega a resposta: INE ou GEO API PT. | Pode não ter produzido todos os dados da resposta. |
| **Produtor original / operação** | Quem produziu os dados e, quando conhecida, a operação estatística ou cartográfica. | A GEO API PT reúne dados de várias origens; indicar quando a origem é desconhecida. |
| **Indicador** | Definição publicada de uma medida, com código externo, unidade, periodicidade, dimensões, classificação e notas metodológicas. | [`0008273`](../data/code-dictionary.md#ine-indicator-0008273) e [`0012918`](../data/code-dictionary.md#ine-indicator-0012918) são indicadores distintos até existir prova de equivalência. |
| **Dimensão do indicador** | Eixo publicado pelo INE, com ordem e classificação/versionamento próprios. | A posição `Dim2` é conhecida para o exemplo, não é regra de todos os indicadores. |
| **Categoria** | Código, designação, ordem e nível no âmbito de uma dimensão e versão; [`T`](../data/code-dictionary.md#ine-sex-t) em sexo não é [`T`](../data/code-dictionary.md#ine-age-t) em grupo etário. | Guardar o código de origem como string; «Total» é seleção explícita. |
| **Período de referência** | Categoria temporal da observação: código, designação, ordem e frequência. | Não equivale à data de extração, ingestão ou atualização; não inventar datas de início/fim. |
| **Referência geográfica** | Código e nome publicados, nível, classificação e versão e referência administrativa quando conhecida. | [`11A1312`](../data/code-dictionary.md#ine-geography-11a1312) e [`1312`](../data/code-dictionary.md#geoapi-municipality-1312) são referências distintas; não há identidade universal pelo nome. |
| **Observação recebida** | Resultado para um indicador e uma combinação concreta de categorias, tal como chegou numa consulta. Guarda valor, texto apresentado e eventuais indicações de estado. | Não receber um resultado não equivale a receber zero. |
| **Extração** | Consulta feita à fonte, com parâmetros, datas e referência à resposta original. | Uma nova consulta pode trazer valores revistos; conservar a anterior. |
| **Recurso geométrico** | Feature municipal recebida da GEO API PT com código original e contexto cartográfico declarado. | Uma Feature não é uma observação do INE nem representa automaticamente a geografia estatística. |
| **Correspondência territorial** | Ligação documentada entre dois códigos geográficos, com fontes, versões, provas e casos em que pode ser usada. | Pode não existir ou não servir para todas as edições e períodos. Não basta comparar nomes ou partes do código. |

**Como usar esta tabela:** estes são conceitos para discutir os dados. Não significa que seja preciso criar uma tabela na base de dados para cada linha. Para identificar uma categoria ou um território, precisamos do código e do seu contexto (classificação e versão), mesmo que a fonte não publique um identificador interno estável.

## Regras que os dados têm de cumprir

- Um **indicador** define as dimensões aplicáveis; cada **observação recebida**
  escolhe uma categoria em cada dimensão aplicável, incluindo período e
  geografia quando existirem. As dimensões variam de indicador para indicador.
- Uma observação recebida pertence a uma **extração**. Duas extrações com a
  mesma combinação de categorias podem trazer valores diferentes. Temos de conseguir consultar ambas. A forma de identificar cada resposta na base de dados fica por decidir.
- A seleção de **período** e **geografia** pode ser exposta como relação
  especializada para consulta, mantendo o código original e a dimensão de
  onde veio. A categoria temporal [`S7A2023`](../data/code-dictionary.md#ine-period-s7a2023) e a chave `Dados["2023"]`
  coexistem sem assumir que são intercambiáveis fora deste indicador.
- Uma **correspondência territorial** liga referências especificadas por
  fornecedor, classificação, versão/edição, nível e código. Exige evidência e
  declara o âmbito em que pode ser usada; uma referência sem correspondência
  não recebe valores estatísticos no mapa.
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

## Exemplo: população do Porto em 2023

No [pedido INE documentado](../data/sources/ine.md#8-estrutura-dos-dados-reais),
o indicador [`0008273`](../data/code-dictionary.md#ine-indicator-0008273) seleciona período [`S7A2023`](../data/code-dictionary.md#ine-period-s7a2023) (chave de resposta
`2023`), geografia [`11A1312`](../data/code-dictionary.md#ine-geography-11a1312) (Porto), sexo [`T`](../data/code-dictionary.md#ine-sex-t) (HM) e grupo etário
[`T`](../data/code-dictionary.md#ine-age-t) (Total). O campo `valor` é `"267236"` e `ind_string` é
`"267 236"`; a metainformação observada indica unidade `Número (N.º)`,
potência zero e precisão zero. Guardamos os valores originais e a data de
extração indicada na resposta. Para **esta observação**, podemos converter
`"267236"` para `Decimal("267236")`. Esta conversão não estabelece uma regra
para todos os indicadores.

No [exemplo GEO API PT](../data/sources/geoapi.md#5-resposta-real-de-municipioporto),
Porto tem [`dtmn="1312"`](../data/code-dictionary.md#geoapi-municipality-1312) e uma Feature municipal. A associação entre
[`11A1312`](../data/code-dictionary.md#ine-geography-11a1312) e [`1312`](../data/code-dictionary.md#geoapi-municipality-1312) é apenas candidata até a issue #2 estabelecer uma
correspondência versionada. Mesmo confirmando a relação dos códigos, isso não
demonstra equivalência geométrica entre CAOP 2020 e 2024.1.

Um exemplo histórico de outra série INE documentado na
[secção de qualificadores](../data/sources/ine.md#10-qualificadores-e-estado-da-observação)
continha `sinal_conv` e nenhuma chave `valor`. Essa situação modela uma
**observação recebida sem valor, mas com indicação do motivo**. É diferente
de uma observação que a consulta não devolveu e de `valor="0"`. Este exemplo
vem de uma fonte secundária e precisa de confirmação antes de definir as
regras de leitura da resposta.

## O que temos de guardar sobre a origem

Para cada consulta, guardar o fornecedor, o recurso e os parâmetros usados, o
código original, o idioma (se aplicável) e a entidade que produziu os dados
(quando conhecida). Guardar separadamente o período a que os dados dizem
respeito, a data de atualização indicada pela fonte, a data em que a resposta
foi obtida e a data em que entrou no PTScope. Sempre que possível, guardar
uma referência imutável à resposta original, o seu hash e a versão do código
que a interpretou. Se a fonte não indicar uma data de atualização por campo,
não atribuir uma por suposição.

Para a geometria, conservar também edição cartográfica declarada, referência
de origem e condições de reutilização/atribuição confirmadas **para o recurso
utilizado**. A licença GPL referida na documentação da GEO API PT identifica
software e não resolve por si só a redistribuição dos dados agregados; a
[questão continua aberta](../data/sources/geoapi.md#13-licença-e-condições-de-uso).

O caminho previsto é **API externa → módulo de cada fonte → modelo PTScope → API pública → interface**. O módulo INE lê `DimN`, `Dados` e os qualificadores; o módulo GEO API PT lê `dtmn` e GeoJSON. A API pública apresenta um contrato próprio, em vez de copiar a resposta externa. Este documento não fixa JSON de
resposta, armazenamento de snapshots, cache ou estratégia de carregamento da
geometria.

## Situações que o modelo tem de distinguir

| Caso | Representação/comportamento |
| --- | --- |
| Ano sem célula devolvida | Cobertura desconhecida/ausente na consulta; verificar filtros e fonte. Não criar zero. |
| Célula devolvida sem `valor`, com qualificador | Preservar o qualificador e a ausência; nunca calcular a partir de `ind_string` sem regra confirmada. |
| Mesmo indicador, período e categorias em duas consultas | Conservar ambas as respostas e datas até existir uma regra para escolher qual apresentar. |
| [`0008273`](../data/code-dictionary.md#ine-indicator-0008273) versus [`0012918`](../data/code-dictionary.md#ine-indicator-0012918) | Dois indicadores e referenciais potencialmente distintos; sem linha única antes de validar metodologia e correspondência. |
| INE [`11A1312`](../data/code-dictionary.md#ine-geography-11a1312) e GEO API PT [`1312`](../data/code-dictionary.md#geoapi-municipality-1312) | A ligação pode existir, mas exige validação; também não prova que as geometrias sejam iguais. |
| Geometria sem licença/CRS suficientemente esclarecidos | Não publicar camada derivada sem confirmar condições e transformação; o mapa base pode continuar como contexto. |

## O que falta confirmar

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

Ainda temos de decidir se precisamos de PostgreSQL/PostGIS, ORM, migrações, armazenamento da resposta original, agendamento e cache. As [regras já
aprovadas](data-ingestion.md) continuam a reger qualquer implementação.
