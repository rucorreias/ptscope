# PTScope

Plataforma pública de inteligência territorial para analisar crescimento,
stress socioeconómico, tendências futuras e indicadores de risco na contratação
pública em Portugal, em preparação para publicação como projeto open source.

> [!NOTE]
> O PTScope está numa fase inicial de desenvolvimento. A Fase 0 disponibiliza
> apenas a estrutura base do backend e uma API mínima, ainda sem fontes de dados
> externas.

## Objetivo

O PTScope pretende tornar informação territorial portuguesa mais acessível,
compreensível e útil para cidadãos, investigadores, jornalistas, organizações e
decisores públicos.

O projeto será desenvolvido de forma incremental, dando prioridade à qualidade
dos dados, transparência das fontes e clareza das análises.

## Estado atual

Neste momento, o repositório contém um backend mínimo em FastAPI com:

- informação básica sobre a aplicação;
- um endpoint de health check;
- um endpoint para consultar dados municipais através da GEO API PT;
- documentação interativa OpenAPI/Swagger gerada pelo FastAPI;
- uma base de documentação em `docs/`.

Outras fontes de dados ainda não estão integradas.

## Tecnologias

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- httpx, reservado para integrações HTTP futuras

## Começar

### Pré-requisitos

- Python 3.12
- `pip`

### Instalação

```bash
git clone https://github.com/rucorreias/ptscope.git
cd ptscope
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

No Windows PowerShell, ativa o ambiente virtual com:

```powershell
.venv\Scripts\Activate.ps1
```

### Executar o backend

```bash
cd backend
uvicorn app.main:app --reload
```

A API fica disponível em `http://127.0.0.1:8000`.

### Executar com Docker

Na raiz do projeto:

```bash
docker compose up --build
```

O volume do backend fica montado no contentor para permitir hot reload durante
o desenvolvimento.

### Executar os testes

Com o ambiente virtual ativo:

```bash
cd backend
pytest
```

### Executar o lint

Dentro de `backend/`, com o ambiente virtual ativo:

```bash
cd backend
python -m pylint app tests
```

## Endpoints

| Método | Caminho | Descrição |
| --- | --- | --- |
| `GET` | `/` | Estado básico do projeto |
| `GET` | `/api/v1/health` | Estado da API |
| `GET` | `/api/v1/municipios/{nome}` | Dados normalizados de um município |
| `GET` | `/docs` | Documentação Swagger interativa |
| `GET` | `/redoc` | Documentação ReDoc |

Exemplo:

```bash
curl http://127.0.0.1:8000/api/v1/municipios/porto
```

## Estrutura do projeto

```text
ptscope/
├── backend/
│   ├── app/
│   │   ├── api/        # Rotas e composição da API
│   │   ├── core/       # Configuração central futura
│   │   ├── schemas/    # Modelos de dados Pydantic
│   │   ├── services/   # Integrações externas futuras
│   │   └── main.py     # Aplicação FastAPI
│   ├── tests/
│   └── requirements.txt
├── docs/               # Documentação do projeto
└── postman/            # Collection e environments para desenvolvimento
```

## Contribuir

Obrigado por considerares contribuir para o PTScope. Código, documentação,
relatos de erros, propostas de fontes de dados e discussão sobre indicadores
territoriais são formas valiosas de participar.

Como o projeto ainda está a definir as suas bases, começa por
[abrir uma issue](https://github.com/rucorreias/ptscope/issues/new) para reportar
um problema ou alinhar alterações maiores antes de investir na implementação.
Procura primeiro por issues existentes para evitar duplicados.

Para contribuir com código:

1. Cria um fork do repositório.
2. Cria uma branch curta e descritiva a partir da branch principal.
3. Mantém a alteração focada e atualiza a documentação relevante.
4. Confirma que a aplicação arranca e que os endpoints afetados funcionam.
5. Abre um pull request explicando o problema e a solução proposta.

Ao participar, privilegia código simples, legível e idiomático. Mantém a
separação entre rotas HTTP (`routes`), integrações externas (`services`) e modelos
de dados (`schemas`).

Um guia `CONTRIBUTING.md` mais detalhado será acrescentado à medida que o fluxo
de desenvolvimento e testes amadurecer.

## Ajuda e comunidade

Para esclarecer uma dúvida, sugerir uma funcionalidade ou reportar um erro,
[abre uma issue](https://github.com/rucorreias/ptscope/issues/new) com contexto
suficiente para que outra pessoa consiga compreender e reproduzir o caso.

Este projeto pretende manter um espaço acolhedor e construtivo. Um código de
conduta e um canal privado para reportes sensíveis serão publicados antes da
abertura formal da comunidade.

## Documentação

A documentação inicial está em [`docs/README.md`](docs/README.md). Com o backend
em execução, o contrato atual da API pode ser explorado em
[`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs).

A collection e as instruções para testar a API no Postman estão em
[`postman/README.md`](postman/README.md).

## Segurança

Não publiques credenciais, tokens, dados pessoais ou outros segredos em issues,
pull requests ou commits. Se encontrares uma vulnerabilidade, evita divulgar
detalhes publicamente até existir um processo de reporte responsável definido.

## Licença

A licença do projeto ainda não foi definida. Até existir um ficheiro `LICENSE`,
o código não deve ser considerado disponível para reutilização ou distribuição
fora dos direitos concedidos pela legislação aplicável.
