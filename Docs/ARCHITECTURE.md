# Anime Release Tracker — Arquitetura (v0.6)

Este documento descreve a arquitetura atual do projeto e a responsabilidade de cada módulo.

## Visão geral

```text
                  main.py
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
 anime_manager.py              tracker.py
         │                         │
         ├────────────┐            │
         ▼            ▼            ▼
   database.py     api.py       utils.py
         │            │
         ▼            ├───────────────┐
    animes.db          ▼               ▼
                 cache.py        AniList API
                     │
                     ▼
                 cache.json
```

## Responsabilidade dos módulos

### `main.py`

Inicializa o banco, atualiza a biblioteca ao abrir o programa, exibe avisos e controla o menu principal.

### `anime_manager.py`

Gerencia a biblioteca: carrega, adiciona, remove e atualiza animes, além de detectar mudanças de status e novos episódios.

### `database.py`

Centraliza a persistência da biblioteca no SQLite. Cria a tabela e converte os dados entre as linhas do banco e o formato usado pelo projeto.

### `tracker.py`

Exibe a biblioteca, próximos episódios e episódios lançados no dia.

### `api.py`

Centraliza todas as consultas GraphQL à AniList e utiliza o cache quando aplicável. Nenhum outro módulo deve acessar a API diretamente.

### `cache.py`

Mantém respostas temporárias da API em `data/cache.json`. O cache expira após 30 minutos e não substitui o banco de dados.

### `utils.py`

Reúne funções compartilhadas de títulos, datas, status, tipos e formatação do terminal.

## Armazenamento

```text
data/
├── animes.db    # biblioteca permanente
└── cache.json   # respostas temporárias da API
```

O SQLite é a fonte de verdade da biblioteca. O JSON é utilizado somente pelo cache.

## Fluxo principal

```text
main.py inicializa o SQLite
        ↓
anime_manager.py carrega a biblioteca pelo database.py
        ↓
api.py consulta o cache e, quando necessário, a AniList
        ↓
anime_manager.py sincroniza as alterações no SQLite
        ↓
main.py exibe os avisos e abre o menu
```

## Princípios

* Simplicidade: evitar complexidade desnecessária.
* Separação de responsabilidades: cada módulo possui uma função definida.
* Evolução incremental: implementar uma melhoria por vez.

## Próximos passos

* Central de Atualizações com histórico de eventos.
* Preparação da lógica para uma futura interface.
* Interface gráfica ou web somente após estabilizar o núcleo.
