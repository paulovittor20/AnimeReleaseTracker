from datetime import datetime

from anime_manager import carregar_animes
from api import buscar_anime, buscar_calendario_anime


DIAS_DA_SEMANA = [
    "segunda-feira",
    "terça-feira",
    "quarta-feira",
    "quinta-feira",
    "sexta-feira",
    "sábado",
    "domingo",
]


def obter_nome_anime(anime):
    """
    Retorna o título em inglês quando disponível.

    Caso o título em inglês não exista, utiliza o título em romaji.
    """
    return anime["title"]["english"] or anime["title"]["romaji"]


def converter_timestamp(timestamp):
    """Converte um timestamp Unix em um objeto datetime."""
    return datetime.fromtimestamp(timestamp)


def formatar_data(timestamp):
    """
    Formata a data de lançamento de um episódio.

    Exemplo:
    domingo, 12/07 às 18:30
    """
    data = converter_timestamp(timestamp)
    dia_semana = DIAS_DA_SEMANA[data.weekday()]
    data_formatada = data.strftime("%d/%m às %H:%M")

    return f"{dia_semana}, {data_formatada}"


def episodio_e_hoje(timestamp):
    """Verifica se o episódio será ou foi lançado hoje."""
    data_episodio = converter_timestamp(timestamp).date()
    hoje = datetime.now().date()

    return data_episodio == hoje


def mostrar_separador():
    """Exibe um separador entre os animes mostrados no terminal."""
    print("----------------")


def mostrar_episodios_de_hoje():
    """
    Mostra os episódios cadastrados que têm lançamento marcado para hoje.

    Informa também se o episódio já foi lançado ou se ainda será lançado
    mais tarde no mesmo dia.
    """
    animes = carregar_animes()
    hoje = datetime.now().date()
    agora = datetime.now()
    encontrados = False

    if not animes:
        print("\nNenhum anime cadastrado.")
        return

    for anime in animes:
        calendario = buscar_calendario_anime(anime["id"])

        # Se a API falhar para um anime, continuamos verificando os demais.
        if not calendario:
            continue

        episodios = calendario["airingSchedule"]["nodes"]

        for episodio in episodios:
            data_episodio = converter_timestamp(
                episodio["airingAt"]
            )

            if data_episodio.date() != hoje:
                continue

            encontrados = True

            mostrar_separador()
            print(f"🔥 {obter_nome_anime(calendario)}")
            print(f"Episódio: {episodio['episode']}")

            if agora >= data_episodio:
                print("✅ Episódio lançado hoje!")
                print(
                    "Lançou às:",
                    data_episodio.strftime("%H:%M"),
                )

            else:
                print(
                    "⏰ Sai hoje às:",
                    data_episodio.strftime("%H:%M"),
                )

    if not encontrados:
        print("\nNenhum episódio lança hoje.")


def mostrar_episodios():
    """
    Mostra o próximo episódio de cada anime cadastrado.

    Quando não existe um próximo episódio anunciado, mostra o estado
    atual do anime, como finalizado, em hiato ou sem previsão.
    """
    animes = carregar_animes()

    if not animes:
        print("\nNenhum anime cadastrado.")
        return

    for anime in animes:
        resultado = buscar_anime(anime["id"])

        # Evita que uma falha temporária da API encerre o programa.
        if not resultado:
            mostrar_separador()
            print(f"Anime: {anime['nome']}")
            print("⚠️ Não foi possível consultar este anime.")
            continue

        mostrar_separador()
        print(f"Anime: {obter_nome_anime(resultado)}")

        proximo_episodio = resultado["nextAiringEpisode"]

        if proximo_episodio:
            numero_episodio = proximo_episodio["episode"]
            timestamp = proximo_episodio["airingAt"]

            if episodio_e_hoje(timestamp):
                print("🔥 EPISÓDIO LANÇA HOJE!")

            print(f"Próximo episódio: {numero_episodio}")
            print(f"Lançamento: {formatar_data(timestamp)}")

        else:
            mostrar_situacao_sem_proximo_episodio(resultado)

        mostrar_total_episodios(resultado)


def mostrar_situacao_sem_proximo_episodio(anime):
    """
    Explica por que um anime não possui próximo episódio anunciado.
    """
    status = anime["status"]

    if status == "FINISHED":
        print("🏁 Anime finalizado")

    elif status == "HIATUS":
        print("⏸️ Anime em hiato")

    elif status == "NOT_YET_RELEASED":
        print("⏳ Anime ainda não lançado")

    elif status == "CANCELLED":
        print("❌ Anime cancelado")

    else:
        print("Sem próximo episódio anunciado")


def mostrar_total_episodios(anime):
    """Mostra o total de episódios do anime, quando informado pela API."""
    total_episodios = anime["episodes"]

    if total_episodios:
        print(f"Total de episódios: {total_episodios}")

    else:
        print("Total de episódios ainda não anunciado")
