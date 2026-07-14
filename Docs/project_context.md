# PROJECT_CONTEXT.md

# Anime Release Tracker - Contexto de Desenvolvimento

**Projeto iniciado:** 2026

**Linguagem:** Python

**Desenvolvedor:** Paulo Vitor

**Assistente de desenvolvimento:** ChatGPT

---

# Objetivo Principal

Desenvolver um sistema em Python para acompanhar lançamentos de animes automaticamente, consultando a API da AniList para verificar mudanças de status e lançamento de episódios.

O projeto tem como prioridade a lógica do sistema. A interface gráfica será desenvolvida apenas quando toda a estrutura principal estiver estável.

---

# Filosofia do Projeto

Este projeto tem caráter de aprendizado.

Sempre priorizar:

* Código simples
* Código legível
* Explicações passo a passo
* Evitar otimizações prematuras
* Implementar uma funcionalidade por vez

Sempre discutir a solução antes de implementá-la.

Não adicionar funcionalidades ou abstrações sem uma necessidade real.

---

# Estrutura Atual

```text
main.py
anime_manager.py
tracker.py
api.py
utils.py

data/
└── animes.json

docs/
├── ARCHITECTURE.md
└── PROJECT_CONTEXT.md
```

## Responsabilidade de cada arquivo

### main.py

Responsável por:

* Menu principal
* Entrada do usuário
* Navegação entre funcionalidades

---

### anime_manager.py

Responsável por:

* Adicionar anime
* Remover anime
* Atualizar biblioteca
* Manipular o arquivo JSON

---

### tracker.py

Responsável por:

* Exibir próximos episódios
* Exibir episódios lançados no dia
* Exibir a biblioteca do usuário
* Filtrar animes por status
* Apresentar informações ao usuário

---

### api.py

Responsável por:

* Comunicação com a API da AniList
* Tratamento das respostas
* Padronização dos dados recebidos

---

### utils.py

Responsável por funções reutilizáveis do projeto.

Exemplos:

* Formatação de status
* Ícones por status
* Títulos do terminal
* Separadores
* Funções auxiliares

---

### animes.json

Armazenamento atual da biblioteca.

Será substituído futuramente por SQLite.

---

# Decisões Arquiteturais

## Banco de dados

Atualmente:

JSON

Motivo:

* Facilidade
* Aprendizado
* Desenvolvimento rápido

Futuro:

SQLite

Quando a migração acontecer, será reavaliada a criação de funções genéricas para filtros por status, evitando abstração prematura na versão atual.

---

## Interface

Ainda não será criada.

Motivo:

Toda a lógica precisa estar pronta antes.

---

## APIs

Toda comunicação deve passar por:

`api.py`

Nenhum outro módulo deve acessar APIs diretamente.

---

## Organização da biblioteca

A biblioteca possui uma única área chamada **Meus Animes**.

Os diferentes status são exibidos através de filtros internos, evitando duplicação de menus e reutilizando a mesma lógica de listagem.

---

# Estado Atual do Projeto

## Implementado

* Cadastro de animes
* Remoção de animes
* Atualização automática da biblioteca
* Consulta à API da AniList
* Detecção de novos episódios
* Avisos de mudanças de status
* Avisos de novos episódios
* Organização da biblioteca por status
* Exibição da data oficial de finalização
* Chave `ultimo_episodio_lancado`
* Interface do terminal reorganizada

---

## Próxima funcionalidade

Central de Histórico de Alterações.

Objetivo:

Registrar todas as alterações detectadas pelo tracker, como:

* Novos episódios
* Mudanças de status
* Finalização de temporadas
* Retorno de hiato

Essa funcionalidade será implementada após a migração para SQLite, pois depende de um armazenamento estruturado.

---

# Roadmap Técnico

## Etapa 1

Finalizar a lógica principal.

Inclui:

* Melhorias internas
* Tratamento de erros
* Pequenas refatorações

---

## Etapa 2

Melhorar desempenho.

Inclui:

* Cache
* Reutilização de dados
* Otimização das consultas

---

## Etapa 3

Migrar armazenamento.

Trocar:

JSON

por

SQLite

---

## Etapa 4

Implementar a Central de Histórico de Alterações.

---

## Etapa 5

Criar interface gráfica.

Possibilidades:

* Tkinter
* CustomTkinter
* Interface Web

A decisão será tomada futuramente.

---

# Convenções

Sempre que possível:

* Funções pequenas
* Nomes descritivos
* Evitar repetição de código
* Comentar apenas quando necessário

Refatorações devem acontecer somente quando trouxerem benefícios reais ao projeto.

---

# Forma de Desenvolvimento

Fluxo adotado:

1. Discutir a funcionalidade.
2. Entender o problema.
3. Definir a melhor solução.
4. Implementar.
5. Testar.
6. Atualizar a documentação.
7. Fazer commit no Git.

---

# Como retomar o projeto em outro chat

Ao iniciar uma nova conversa:

1. Enviar este arquivo (`PROJECT_CONTEXT.md`).
2. Enviar o `README.md`.
3. Informar quais arquivos mudaram desde a última atualização, se houver.

Com esses documentos, o desenvolvimento pode continuar rapidamente sem depender do histórico da conversa.

---

# Observações

Este documento é um registro vivo do desenvolvimento.

Sempre que uma decisão arquitetural importante for tomada ou uma funcionalidade relevante for concluída, este arquivo deve ser atualizado.

O objetivo não é documentar tudo, mas preservar o contexto necessário para continuar o projeto em qualquer momento.
