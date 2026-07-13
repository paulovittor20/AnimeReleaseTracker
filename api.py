import requests


URL = "https://graphql.anilist.co"
TEMPO_LIMITE = 10

# evita repetir a mesma mensagem para cada anime
# quando a conexçao com a internet estiver indisponível
def executar_consulta(query, variaveis=None):
    """
    Envia uma consulta GraphQL para a AniList.

    Retorna o conteúdo da chave 'data' quando a requisição
    funciona ou None quando ocorre algum problema.
    """

    try:
        resposta = requests.post(
            URL,
            json={
                "query": query,
                "variables": variaveis or {},
            },
            timeout=TEMPO_LIMITE,
        )

        # Gera uma exceção para respostas HTTP com erro,
        # como 400, 404, 500 ou 503.
        resposta.raise_for_status()

        resultado = resposta.json()

        # Uma API GraphQL pode retornar status HTTP 200
        # e ainda assim informar erros na resposta.
        if resultado.get("errors"):
            print("\n⚠️ A AniList retornou um erro na consulta.")

            for erro in resultado["errors"]:
                print(f"- {erro.get('message', 'Erro desconhecido')}")

            return None

        return resultado.get("data")

    except requests.Timeout:
        print("\n⚠️ A AniList demorou muito para responder.")
        return None

    except requests.ConnectionError:
            print("\n⚠️ Não foi possível conectar à AniList.")
            print("Verifique sua conexão com a internet.")
            return None

    except requests.HTTPError as erro:
        print(f"\n⚠️ Erro HTTP ao consultar a AniList: {erro}")
        return None

    except requests.RequestException as erro:
        print(f"\n⚠️ Erro ao consultar a AniList: {erro}")
        return None

    except ValueError:
        print("\n⚠️ A AniList retornou uma resposta inválida.")
        return None


def buscar_anime(anime_id):
    """Busca os dados atualizados de um anime pelo ID."""
    query = """
    query ($id: Int!) {
        Media(id: $id, type: ANIME) {
            id

            title {
                romaji
                english
            }

            format
            status
            episodes
            endDate {
                year
                month
                day
            }

            nextAiringEpisode {
                episode
                airingAt
            }
        }
    }
    """

    dados = executar_consulta(
        query,
        {"id": anime_id},
    )

    if not dados:
        return None

    return dados.get("Media")


def buscar_animes_por_nome(nome):
    """
    Pesquisa até dez animes de TV pelo nome informado.

    Retorna:
    - uma lista com os resultados;
    - uma lista vazia quando nenhum anime é encontrado;
    - None quando a consulta falha.
    """
    query = """
    query ($nome: String!) {
        Page(perPage: 10) {
            media(
                search: $nome
                type: ANIME
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

    dados = executar_consulta(
        query,
        {"nome": nome},
    )

    # None significa que a consulta falhou.
    if dados is None:
        return None

    pagina = dados.get("Page")

    if not pagina:
        return []

    return pagina.get("media", [])


def buscar_calendario_anime(anime_id):
    """
    Busca o calendário de lançamento dos episódios de um anime.

    O calendário é usado para descobrir a data em que
    determinado episódio foi lançado.
    """
    query = """
    query ($id: Int!) {
        Media(id: $id, type: ANIME) {
            title {
                romaji
                english
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

    dados = executar_consulta(
        query,
        {"id": anime_id},
    )

    if not dados:
        return None

    return dados.get("Media")