# Anime Release Tracker 🎬

O Anime Release Tracker é um projeto desenvolvido em Python para acompanhar lançamentos de animes utilizando a API da AniList.

Além de ser uma ferramenta para acompanhar lançamentos de animes, o projeto também serve como um ambiente de estudo para arquitetura de software, consumo de APIs, organização de código e boas práticas de desenvolvimento em Python.

---

## ✨ Funcionalidades

Atualmente o projeto permite:

- ✔ Buscar animes através da API AniList
- ✔ Adicionar animes à lista de acompanhamento
- ✔ Remover animes da lista
- ✔ Visualizar os próximos episódios
- ✔ Ver episódios lançados no dia
- ✔ Atualizar automaticamente as informações dos animes cadastrados
- ✔ Receber avisos quando detectar mudança de status:
  - Uma temporada é finalizada
  - Um anime entra em hiato
  - Um anime retorna do hiato
  - Um ou mais novos episódios são oficialmente lançados
- ✔ Armazenar os dados localmente em JSON  

---

## 🛠️ Tecnologias utilizadas

- Python 3
- Requests
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

Instale as dependências:

```bash
pip install -r requirements.txt
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
├── utils.py
├── PROJECT_CONTEXT.md
├── README.md
├── ARCHITECTURE.md
└── requirements.txt
```

---

## 📈 Status do projeto

🟢 Desenvolvimento ativo.

O projeto continuará recebendo novas funcionalidades e melhorias conforme evolui.

---

## 🎯 Próximas melhorias

- Melhorar a organização do projeto
- Implementar cache
- Migrar para SQLite
- Desenvolver interface gráfica
- Evoluir continuamente a arquitetura

## 📚 Aprendizados

Durante o desenvolvimento deste projeto estão sendo praticados conceitos como:

- Organização de projetos Python
- Consumo de APIs GraphQL
- Manipulação de arquivos JSON
- Tratamento de erros
- Arquitetura modular
- Versionamento com Git
- Evolução incremental de software