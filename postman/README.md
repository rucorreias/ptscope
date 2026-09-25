# Postman

Esta pasta contém a collection, os environments e os exemplos da API PTScope
no formato Native Git do Postman.

## Utilização

1. Arranca o backend localmente ou com Docker.
2. Abre a raiz do repositório no Postman Desktop em Local View.
3. Seleciona `PTScope Local` ou `PTScope Docker` como environment.
4. Executa os pedidos da collection `PTScope API`.

A collection usa `http://127.0.0.1:8000` por omissão. Os environments podem
substituir a variável `baseUrl` sem alterar os pedidos.

## Segurança

Os ficheiros versionados só devem conter valores públicos adequados a
desenvolvimento local. Tokens, credenciais, cookies e outros segredos devem
permanecer em valores locais ou no Postman Vault e nunca ser adicionados ao Git.
