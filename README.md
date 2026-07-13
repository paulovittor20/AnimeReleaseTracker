# Anime Release Tracker 🎬

O Anime Release Tracker é um projeto desenvolvido em Python para acompanhar lançamentos de animes utilizando a API da AniList.

Além de ser uma ferramenta para acompanhar lançamentos de animes, o projeto também serve como um ambiente de estudo para arquitetura de software, consumo de APIs, organização de código e boas práticas de desenvolvimento em Python.

---

## ✨ Funcionalidades

Atualmente o projeto permite:

* ✔ Buscar animes através da API AniList
* ✔ Adicionar e remover animes da biblioteca
* ✔ Organizar a biblioteca por status:

  * Todos
  * Em lançamento
  * Finalizados
  * Em hiato
* ✔ Visualizar os próximos episódios (apenas animes em lançamento)
* ✔ Ver episódios lançados no dia
* ✔ Atualizar automaticamente as informações dos animes cadastrados ao iniciar o programa
* ✔ Receber avisos quando detectar mudanças importantes:

  * Uma temporada foi finalizada
  * Um anime entrou em hiato
  * Um anime retornou do hiato
  * Um ou mais novos episódios foram lançados
* ✔ Exibir a data oficial de finalização de animes concluídos
* ✔ Armazenar os dados localmente em JSON

---

## 🛠️ Tecnologias utilizadas

* Python 3
* Requests
* GraphQL
* AniList API
* JSON
* Git
* GitHub

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
├── data/
│   └── animes.json
│
├── docs/
│   ├── ARCHITECTURE.md
│   └── PROJECT_CONTEXT.md
│
├── main.py
├── api.py
├── anime_manager.py
├── tracker.py
├── utils.py
├── requirements.txt
└── README.md
```

---

## 📈 Status do projeto

🟢 Desenvolvimento ativo.

A versão atual organiza a biblioteca por status, detecta automaticamente mudanças nos animes cadastrados e mantém os dados sincronizados com a AniList.

---

## 🎯 Roadmap

### v0.5

* Implementar cache para reduzir consultas repetidas à API.

### Futuro

* Migrar o armazenamento para SQLite.
* Implementar uma Central de Atualizações.
* Desenvolver uma interface gráfica.
* Continuar evoluindo a arquitetura do projeto.

---

## 📚 Aprendizados

Durante o desenvolvimento deste projeto estão sendo praticados conceitos como:

* Organização de projetos Python
* Consumo de APIs GraphQL
* Manipulação de arquivos JSON
* Tratamento de erros
* Arquitetura modular
* Versionamento com Git
* Evolução incremental de software
* Refatoração e reutilização de código
