# PROJECT_CONTEXT.md

# Anime Release Tracker - Contexto de Desenvolvimento

**Projeto iniciado:** 2026

**Linguagem:** Python

**Desenvolvedor:** Paulo Vitor

**Assistente de desenvolvimento:** ChatGPT

---

# Objetivo Principal

Desenvolver um sistema em Python para acompanhar animes automaticamente, consultando APIs para verificar mudanças de status e lançamento de episódios.

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

Não tentar transformar o projeto em algo extremamente complexo antes da hora.

---

# Estrutura Atual

```text
main.py
anime_manager.py
tracker.py
api.py
animes.json
```

## Responsabilidade de cada arquivo

### main.py

* Menu principal
* Entrada do usuário
* Chamada das funcionalidades

---

### anime_manager.py

Responsável por:

* adicionar anime
* remover anime
* listar animes
* manipular o arquivo JSON

---

### tracker.py

Responsável por:

* verificar mudanças nos animes
* atualizar episódios
* atualizar status
* controlar histórico de alterações

---

### api.py

Responsável por:

* comunicação com APIs externas
* tratamento das respostas
* padronização dos dados recebidos

---

### animes.json

Banco de dados temporário.

Será substituído futuramente por SQLite.

---

# Decisões Arquiteturais

## Banco de dados

Atualmente:

JSON

Motivo:

* facilidade
* aprendizado
* desenvolvimento rápido

Futuro:

SQLite

---

## Interface

Ainda não será criada.

Motivo:

Toda a lógica precisa estar pronta antes.

---

## APIs

Toda comunicação deve passar pelo arquivo:

api.py

Nenhum outro módulo deve acessar APIs diretamente.

---

# Estado Atual do Projeto

## Implementado

* Cadastro de animes
* Remoção
* Listagem
* Consulta à API
* Atualização do status
* Atualização do número de episódios

---

## Em desenvolvimento

Sistema de notificações.

Problema identificado:

Quando um episódio novo é encontrado, o sistema atualiza o JSON corretamente, porém o usuário não recebe um aviso claro informando que houve um novo lançamento.

Essa será a próxima funcionalidade implementada.

---

# Roadmap Técnico

## Etapa 1

Finalizar toda a lógica.

Inclui:

* notificações
* histórico
* melhorias internas
* tratamento de erros

---

## Etapa 2

Melhorar desempenho.

Inclui:

* cache
* reutilização de dados
* otimização das consultas

---

## Etapa 3

Migrar armazenamento.

Trocar:

JSON

por

SQLite

---

## Etapa 4

Criar interface.

Possibilidades:

* Tkinter
* CustomTkinter
* Interface Web

A decisão será tomada futuramente.

---

# Convenções

Sempre que possível:

* funções pequenas
* nomes descritivos
* evitar repetição de código
* comentar apenas quando necessário

---

# Forma de Desenvolvimento

O projeto será desenvolvido em pequenas etapas.

Fluxo adotado:

1. Escolher uma funcionalidade.
2. Entender o problema.
3. Implementar.
4. Testar.
5. Atualizar este documento.
6. Fazer commit no Git.

---

# Como retomar o projeto em outro chat

Ao iniciar uma nova conversa:

1. Enviar este arquivo (`PROJECT_CONTEXT.md`).
2. Enviar o `README.md`.
3. Informar, se necessário, quais arquivos do projeto mudaram desde a última atualização.

Com esses documentos, o contexto do projeto pode ser retomado rapidamente sem depender do histórico da conversa.

---

# Observações

Este documento é um registro vivo do desenvolvimento.

Sempre que uma decisão importante for tomada ou uma funcionalidade relevante for concluída, este arquivo deve ser atualizado.

O objetivo não é documentar tudo, mas preservar o contexto necessário para continuar o projeto em qualquer momento.
