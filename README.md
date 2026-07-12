# Anime Release Tracker 🎬

Um sistema desenvolvido em Python para acompanhar lançamentos de animes utilizando a API AniList.

O objetivo do projeto é permitir que o usuário acompanhe os animes de seu interesse em um único lugar, visualizando próximos episódios, episódios lançados no dia e mudanças importantes como temporadas finalizadas, hiatos e retorno de lançamentos.

---

## ✨ Funcionalidades

Atualmente o projeto permite:

- 🔍 Buscar animes através da API AniList
- ➕ Adicionar animes à lista de acompanhamento
- ➖ Remover animes da lista
- 📅 Visualizar os próximos episódios
- 🔥 Ver episódios lançados no dia
- 🔔 Receber avisos quando:
  - Uma temporada é finalizada
  - Um anime entra em hiato
  - Um anime retorna do hiato
  - A quantidade de episódios é atualizada
- 💾 Armazenar os dados localmente em JSON

---

## 🛠️ Tecnologias utilizadas

- Python 3
- GraphQL
- AniList API
- JSON
- Git
- GitHub

---

## 🚀 Como executar

Clone o repositório:

```bash
git clone https://github.com/paulovittor20/AnimeReleaseTracker.git
```

Entre na pasta do projeto:

```bash
cd AnimeReleaseTracker
```

Execute:

```bash
python main.py
```

---

## 📂 Estrutura do projeto

```
AnimeReleaseTracker
│
├── main.py
├── api.py
├── anime_manager.py
├── tracker.py
├── animes.json
└── README.md
```

---

## 📈 Status do projeto

🟢 Em desenvolvimento.

O projeto continuará recebendo novas funcionalidades e melhorias conforme evolui.

---

## 🎯 Próximas melhorias

- Migrar o armazenamento de JSON para SQLite
- Criar um sistema de cache para reduzir chamadas à API
- Melhorar o sistema de notificações
- Desenvolver uma interface gráfica
- Criar uma versão Web utilizando FastAPI e React
- Adicionar suporte a múltiplas APIs de anime
