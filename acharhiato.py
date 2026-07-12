import requests


URL = "https://graphql.anilist.co"


query = """
query {

  Page(perPage: 10) {

    media(
      type: ANIME,
      status: HIATUS
    ) {

      id

      title {
        romaji
        english
      }

      episodes

    }

  }

}
"""


resposta = requests.post(
    URL,
    json={"query": query}
)


dados = resposta.json()


for anime in dados["data"]["Page"]["media"]:

    print("----------------")

    print("ID:", anime["id"])

    print(
        "Nome:",
        anime["title"]["english"]
        or anime["title"]["romaji"]
    )

    print(
        "Episódios:",
        anime["episodes"]
    )