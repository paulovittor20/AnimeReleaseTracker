import json
from datetime import datetime
from pathlib import Path
from api import (
    buscar_anime,
    buscar_animes_por_nome,
    buscar_calendario_anime,
)
from utils import obter_titulo, formatar_tipo, formatar_status

from api import (
    buscar_anime,
    buscar_animes_por_nome,
    buscar_calendario_anime,
)


# O caminho é baseado na localização deste arquivo.
# Assim, o JSON continua sendo encontrado mesmo que o programa
# seja executado a partir de outra pasta.
ARQUIVO = Path(__file__).parent / "data" / "animes.json"

def carregar_animes():
    """Carrega e devolve a lista de animes salva no JSON."""

    # Caso o arquivo ainda não exista, cria uma lista vazia.
    if not ARQUIVO.exists():
        salvar_animes([])
        return []

    try:
        with ARQUIVO.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except json.JSONDecodeError:
        print("\n⚠️ O arquivo animes.json está vazio ou corrompido.")
        return []


def salvar_animes(animes):
    """Salva a lista completa de animes no arquivo JSON."""
    with ARQUIVO.open("w", encoding="utf-8") as arquivo:
        json.dump(
            animes,
            arquivo,
            indent=4,
            ensure_ascii=False,
        )


def descobrir_ultimo_episodio(dados, anime_id):
    """
    Descobre o último episódio já lançado e sua data.

    Retorna uma tupla no formato:
    (numero_do_episodio, data_do_episodio)
    """
    ultimo_episodio = 0
    data_ultimo_episodio = None

    proximo_episodio = dados.get("nextAiringEpisode")

    if proximo_episodio:
        ultimo_episodio = proximo_episodio["episode"] - 1

        calendario = buscar_calendario_anime(anime_id)

        if calendario:
            episodios = calendario["airingSchedule"]["nodes"]

            for episodio in episodios:
                if episodio["episode"] != ultimo_episodio:
                    continue

                data = datetime.fromtimestamp(episodio["airingAt"])
                data_ultimo_episodio = data.strftime("%d/%m/%Y")
                break

    elif dados["status"] == "FINISHED":
        ultimo_episodio = dados["episodes"] or 0

    return ultimo_episodio, data_ultimo_episodio


def criar_aviso_de_status(nome, status_antigo, status_novo):
    """
    Cria a mensagem e informa em qual categoria ela deve aparecer.

    Retorna:
    (categoria, mensagem)

    Caso o status não tenha mudado, retorna:
    (None, None)
    """
    if status_antigo == status_novo:
        return None, None

    if status_antigo == "RELEASING" and status_novo == "FINISHED":
        return (
            "finalizados",
            f"🎉 {nome}\nA temporada foi finalizada!",
        )

    if status_antigo == "RELEASING" and status_novo == "HIATUS":
        return (
            "hiato",
            f"⏸ {nome}\nO anime entrou em hiato.",
        )

    if status_antigo == "HIATUS" and status_novo == "RELEASING":
        return (
            "retornos",
            f"🔥 {nome}\nO anime voltou do hiato!",
        )

    if status_antigo == "NOT_YET_RELEASED" and status_novo == "RELEASING":
        return (
            "outros",
            f"🚀 {nome}\nO anime começou a ser lançado!",
        )

    mensagem = (
        f"🔄 {nome}\n"
        f"Status alterado: "
        f"{formatar_status(status_antigo)} → "
        f"{formatar_status(status_novo)}"
    )

    return "outros", mensagem


def criar_aviso_de_episodio(
    nome,
    episodio_antigo,
    episodio_novo,
    data_episodio=None,
):
    """
    Cria um aviso quando o número do último episódio lançado aumenta.

    Retorna None quando nenhum episódio novo foi encontrado.
    """
    if episodio_novo <= episodio_antigo:
        return None

    quantidade_nova = episodio_novo - episodio_antigo

    if quantidade_nova == 1:
        mensagem = (
            f"🔥 {nome}\n"
            f"Novo episódio lançado: episódio {episodio_novo}"
        )

    else:
        mensagem = (
            f"🔥 {nome}\n"
            f"{quantidade_nova} episódios novos foram encontrados!\n"
            f"Último episódio disponível: {episodio_novo}"
        )

    if data_episodio:
        mensagem += f"\nData do lançamento: {data_episodio}"

    return mensagem


def atualizar_animes():
    """
    Consulta novamente os animes cadastrados e atualiza seus dados.

    Também devolve os avisos encontrados para que o main.py
    possa exibi-los ao iniciar o programa.
    """
    animes = carregar_animes()

    avisos = {
        "episodios": [],
        "finalizados": [],
        "hiato": [],
        "retornos": [],
        "outros": [],
    }

    for anime in animes:
        dados = buscar_anime(anime["id"])

        # Se a API falhar para um anime, os outros continuam sendo atualizados.
        if not dados:
            break

        nome_novo = obter_titulo(dados)
        status_antigo = anime.get("status")
        status_novo = dados["status"]

        # Guardamos o episódio antigo antes de atualizar o objeto.
        # Ele será usado futuramente para detectar lançamentos novos.
        episodio_antigo = anime.get(
            "ultimo_episodio_lancado",
            anime.get("ultimo_episodio", 0),
        )

        ultimo_episodio, data_ultimo_episodio = descobrir_ultimo_episodio(
            dados,
            anime["id"],
        )

        categoria, mensagem = criar_aviso_de_status(
            nome_novo,
            status_antigo,
            status_novo,
        )

        if categoria and mensagem:
            avisos[categoria].append(mensagem)



        mensagem_episodio = criar_aviso_de_episodio(
            nome_novo,
            episodio_antigo,
            ultimo_episodio,
            data_ultimo_episodio,
        )

        if mensagem_episodio:
            avisos["episodios"].append(mensagem_episodio)



        anime["nome"] = nome_novo
        anime["tipo"] = dados["format"]
        anime["episodios"] = dados["episodes"]
        anime["status"] = status_novo

        data_finalizacao = dados.get("endDate")

        if status_novo == "FINISHED" and data_finalizacao:
            anime["data_finalizacao"] = data_finalizacao
        else:
            anime.pop("data_finalizacao", None)

        anime["ultimo_episodio_lancado"] = ultimo_episodio

        if data_ultimo_episodio:
            anime["data_ultimo_episodio"] = data_ultimo_episodio

        # Remove a chave antiga, caso ela ainda exista no JSON.
        anime.pop("ultimo_episodio", None)

    salvar_animes(animes)

    return avisos


def adicionar_anime():
    """Pesquisa um anime na API e adiciona a escolha ao JSON."""
    while True:
        nome = input(
            "\nDigite o nome do anime (ou 0 para voltar): "
        ).strip()

        if nome == "0":
            return

        resultados = buscar_animes_por_nome(nome)

        if resultados is None:
            print("\n⚠️ Não foi possível realizar a pesquisa.")
            return
        
        if not resultados:
            print("\nNenhum resultado encontrado. Tente outro nome.")
            continue


        resultados.sort(
            key=lambda anime: anime["title"]["romaji"]
        )
        break

    print("\nResultados encontrados:\n")
    print("0 - Voltar\n")

    for indice, anime in enumerate(resultados, start=1):
        titulo = obter_titulo(anime)

        print(f"{indice} - {titulo}")
        print(f"   Tipo: {formatar_tipo(anime['format'])}")
        print(f"   Episódios: {anime['episodes'] or 'Não informado'}")
        print(f"   Status: {formatar_status(anime['status'])}")
        print()

    try:
        escolha = int(input("\nEscolha o anime: "))

    except ValueError:
        print("\nDigite apenas números.")
        return

    if escolha == 0:
        return

    if escolha < 1 or escolha > len(resultados):
        print("\nOpção inválida.")
        return

    anime_escolhido = resultados[escolha - 1]
    animes = carregar_animes()

    for anime in animes:
        if anime["id"] != anime_escolhido["id"]:
            continue

        print("\n⚠️ Esse anime já foi adicionado!")

        detalhes = buscar_anime(anime["id"])

        if detalhes and detalhes["nextAiringEpisode"]:
            print(
                "Próximo episódio:",
                detalhes["nextAiringEpisode"]["episode"],
            )

        return
    
    detalhes = buscar_anime(anime_escolhido["id"])

    if detalhes:
        ultimo_episodio, data_ultimo_episodio = descobrir_ultimo_episodio(
        detalhes,
        anime_escolhido["id"],
    )
    else:
        ultimo_episodio = 0
        data_ultimo_episodio = None

    novo_anime = {
    "nome": obter_titulo(anime_escolhido),
    "id": anime_escolhido["id"],
    "tipo": anime_escolhido["format"],
    "episodios": anime_escolhido["episodes"],
    "status": anime_escolhido["status"],
    "ultimo_episodio_lancado": ultimo_episodio,
    }
    data_finalizacao = detalhes.get("endDate")

    if detalhes["status"] == "FINISHED" and data_finalizacao:
        novo_anime["data_finalizacao"] = data_finalizacao

    if data_ultimo_episodio:
        novo_anime["data_ultimo_episodio"] = data_ultimo_episodio

    animes.append(novo_anime)
    salvar_animes(animes)

    print("\n✅ Anime adicionado com sucesso!")


def remover_anime():
    """Mostra os animes cadastrados e permite remover um deles."""
    animes = carregar_animes()

    if not animes:
        print("\nNenhum anime cadastrado.")
        return

    print("\nAnimes cadastrados:\n")
    print("0 - Voltar")

    for indice, anime in enumerate(animes, start=1):
        print(f"{indice} - {anime['nome']}")

    try:
        escolha = int(
            input("\nEscolha o anime que deseja remover: ")
        )

    except ValueError:
        print("\nDigite apenas números.")
        return

    if escolha == 0:
        return

    if escolha < 1 or escolha > len(animes):
        print("\nOpção inválida.")
        return

    anime_removido = animes[escolha - 1]

    confirmar = input(
        f"\nTem certeza que deseja remover "
        f"{anime_removido['nome']}? (s/n): "
    ).strip().lower()

    if confirmar != "s":
        print("\nOperação cancelada.")
        return

    animes.pop(escolha - 1)
    salvar_animes(animes)

    print("\n✅ Anime removido com sucesso!")