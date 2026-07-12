import requests


URL = "https://graphql.anilist.co"


def buscar_anime(anime_id):

    query = """
    query {
      Media(id: ID, type: ANIME) {

        id

        title {
          romaji
          english
        }

        format

        status

        episodes

        nextAiringEpisode {
          episode
          airingAt
        }

      }
    }
    """


    query = query.replace("ID", str(anime_id))


    resposta = requests.post(
        URL,
        json={"query": query}
    )


    if resposta.status_code == 200:

        dados = resposta.json()

        return dados["data"]["Media"]

    else:

        return None



def buscar_animes_por_nome(nome):

    query = """
    query {
      Page(perPage: 10) {

        media(
          search: "NOME",
          type: ANIME,
          format_in: [TV]
        ) {

          id

          title {
            romaji
            english
          }

          format

          episodes

          status
        }
      }
    }
    """


    query = query.replace("NOME", nome)


    resposta = requests.post(
        URL,
        json={"query": query}
    )


    if resposta.status_code == 200:

        dados = resposta.json()

        return dados["data"]["Page"]["media"]

    else:

        return []


def buscar_calendario_anime(anime_id):

    query = """
    query {
      Media(id: ID, type: ANIME) {

        title {
          romaji
        }

        airingSchedule {

          nodes {

            episode
            airingAt

          }

        }

      }
    }
    """


    query = query.replace("ID", str(anime_id))


    resposta = requests.post(
        URL,
        json={"query": query}
    )


    if resposta.status_code == 200:

        dados = resposta.json()

        return dados["data"]["Media"]

    else:

        return None