# Documentação do PTScope

O PTScope está a dar os primeiros passos. Já é possível consultar um município através da GEO API PT no backend e navegar entre mapa e dashboards no frontend. O mapa mostra a base cartográfica, mas ainda não apresenta os limites municipais nem a série de população do INE.

- [Plano da v0.1](roadmap.md): o que falta fazer e em que ordem
- [Dicionário de códigos](data/code-dictionary.md): o significado dos códigos encontrados na documentação
- [Estudos das fontes](data/sources/): o que as APIs devolvem, com exemplos e limitações
- [Conclusão da validação INE para a #1](data/validations/ine-population-2026-09-30.md): períodos verificados, limites da evidência e regra para a v0.1
- [Modelo de domínio da v0.1](architecture/domain-model.md): o significado dos dados e as regras ainda por validar
- [Regras de ingestão](architecture/data-ingestion.md): como o PTScope deve tratar os dados

Nos estudos indicamos se uma informação está documentada pela fonte, se foi observada numa resposta ou se é uma hipótese nossa. As decisões sobre o funcionamento do PTScope ficam em `docs/architecture/`.

## Desenvolvimento

O backend está em `backend/`. Com o servidor a correr, a documentação da API fica em `http://127.0.0.1:8000/docs`. O frontend está em `frontend/` e assinala as áreas onde ainda faltam dados.

Para instalação e comandos de execução, consulta o [README principal](../README.md). As tarefas e critérios de conclusão estão nas [issues](https://github.com/rucorreias/ptscope/issues).
