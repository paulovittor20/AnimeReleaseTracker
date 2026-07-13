# ARCHITECTURE.md

# Anime Release Tracker — Arquitetura (v0.3)

Este documento descreve a arquitetura atual do projeto.

Seu objetivo é explicar como os módulos estão organizados, quais são suas responsabilidades e servir como referência para futuras evoluções.

---

# Visão geral

O Anime Release Tracker foi dividido em módulos para separar responsabilidades e facilitar a manutenção do código.

Cada arquivo possui uma função específica dentro do projeto.

```
                 main.py
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
anime_manager.py             tracker.py
        │                         │
        ├──────────────┐          │
        ▼              ▼          ▼
   animes.json      utils.py    api.py
                                     │
                                     ▼
                                AniList API
```

---

# Responsabilidade dos módulos

## `main.py`

Responsável por iniciar o programa.

Funções:

* iniciar a aplicação;
* atualizar os animes ao abrir o programa;
* exibir os avisos encontrados;
* mostrar o menu principal;
* chamar as funções dos demais módulos.

---

## `anime_manager.py`

Responsável pelo gerenciamento dos animes cadastrados.

Funções:

* carregar e salvar o arquivo JSON;
* adicionar e remover animes;
* atualizar informações dos animes;
* detectar mudanças de status;
* detectar novos episódios;
* gerar avisos de atualização.

---

## `tracker.py`

Responsável pela exibição das informações ao usuário.

Funções:

* mostrar próximos episódios;
* mostrar episódios de hoje;
* formatar datas e horários de lançamento.

---

## `api.py`

Responsável pela comunicação com a API da AniList.

Funções:

* pesquisar animes;
* consultar informações atualizadas;
* consultar calendário de episódios;
* tratar erros das requisições.

Nenhum outro módulo deve acessar a AniList diretamente.

---

## `utils.py`

Contém funções compartilhadas entre diferentes módulos.

Atualmente:

* obter o melhor título disponível;
* formatar tipos de anime;
* formatar status.

---

## `animes.json`

Armazena os dados locais do projeto.

Enquanto o SQLite não for implementado, este arquivo funciona como o banco de dados da aplicação.

---

# Fluxo principal

Quando o programa é iniciado:

```
main.py

↓

anime_manager.py atualiza os animes

↓

api.py consulta a AniList

↓

animes.json é atualizado

↓

main.py exibe os avisos

↓

menu principal
```

---

# Filosofia da arquitetura

O projeto segue três princípios:

* **Simplicidade:** evitar complexidade desnecessária.
* **Separação de responsabilidades:** cada módulo possui uma função bem definida.
* **Evolução incremental:** novas funcionalidades devem ser adicionadas aos poucos, sem exigir reescrever o projeto.

---

# Próximos passos

As próximas versões irão expandir esta arquitetura.

Planejamento atual:

* **v0.4:** reorganização das listas de animes (em lançamento e finalizados).
* **v0.5:** implementação de cache.
* **v0.6:** migração para SQLite.
* **v0.7:** preparação para a interface gráfica.

Este documento será atualizado sempre que a arquitetura do projeto evoluir.
