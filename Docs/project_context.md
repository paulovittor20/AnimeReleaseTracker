# Anime Release Tracker — Contexto de Desenvolvimento

**Versão atual:** v0.6  
**Linguagem:** Python  
**Desenvolvedor:** Paulo Vitor  

## Objetivo

Desenvolver um sistema em Python para acompanhar animes automaticamente, consultando a AniList para detectar mudanças de status e lançamentos de episódios. A prioridade é estabilizar a lógica antes de criar uma interface gráfica ou web.

## Filosofia

* Código simples e legível.
* Explicações passo a passo.
* Evitar abstrações e otimizações prematuras.
* Implementar e testar uma funcionalidade por vez.
* Manter responsabilidades bem separadas.

## Estrutura atual

```text
AnimeReleaseTracker/
├── data/
│   ├── animes.db
│   └── cache.json
├── docs/
│   ├── ARCHITECTURE.md
│   └── project_context.md
├── main.py
├── anime_manager.py
├── tracker.py
├── api.py
├── database.py
├── cache.py
├── utils.py
├── requirements.txt
└── README.md
```

## Responsabilidades

* `main.py`: inicialização, avisos, menus e navegação.
* `anime_manager.py`: cadastro, remoção, atualização e regras da biblioteca.
* `tracker.py`: filtros e exibição de episódios e animes.
* `api.py`: comunicação GraphQL com a AniList.
* `database.py`: persistência da biblioteca no SQLite.
* `cache.py`: cache temporário das respostas da API em JSON.
* `utils.py`: funções compartilhadas de formatação e datas.

## Decisões arquiteturais

### Persistência

O SQLite é a fonte de verdade da biblioteca. O antigo `animes.json` foi removido após a conclusão da migração.

O `cache.json` permanece porque tem outra responsabilidade: evitar consultas repetidas à AniList por 30 minutos.

### API

Toda comunicação externa deve passar pelo `api.py`.

### Interface

A interface será criada somente depois que o núcleo do sistema estiver estável.

### Filtros por status

A biblioteca possui uma única área, “Meus Animes”, com filtros internos. Novas abstrações só devem ser criadas quando houver necessidade real.

## Estado da v0.6

* Banco SQLite criado automaticamente.
* Biblioteca lida e salva pelo SQLite.
* Cadastro, atualização e remoção sincronizados com o banco.
* Cache JSON mantido e independente do banco.
* Referências ao armazenamento antigo removidas.
* Documentação atualizada.

## Próximos passos

1. Central de Atualizações e histórico de eventos.
2. Revisão de testes e tratamento de erros.
3. Preparação para interface gráfica ou web.
