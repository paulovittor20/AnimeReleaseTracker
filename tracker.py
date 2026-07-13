from datetime import datetime

from anime_manager import carregar_animes
from api import buscar_anime, buscar_calendario_anime
from utils import (
     obter_titulo,
     formatar_status,
     titulo,
     obter_icone_status,
)



DIAS_DA_SEMANA = [
    "segunda-feira",
    "terça-feira",
    "quarta-feira",
    "quinta-feira",
    "sexta-feira",
    "sábado",
    "domingo",
]

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

    Informa se o episódio já foi lançado ou se ainda será lançado.
    Se uma consulta falhar, a operação é interrompida para não informar
    incorretamente que não existem episódios no dia.
    """
    animes = carregar_animes()

    if not animes:
        print("\nNenhum anime cadastrado.")
        return

    hoje = datetime.now().date()
    agora = datetime.now()
    encontrados = False

    for anime in animes:
        calendario = buscar_calendario_anime(anime["id"])

        # Sem os dados da API, não podemos afirmar
        # se existem ou não episódios marcados para hoje.
        if not calendario:
            print(
                "\n⚠️ Não foi possível verificar "
                "os episódios de hoje."
            )
            return

        episodios = calendario["airingSchedule"]["nodes"]

        for episodio in episodios:
            data_episodio = converter_timestamp(
                episodio["airingAt"]
            )

            if data_episodio.date() != hoje:
                continue

            encontrados = True

            mostrar_separador()
            print(f"🔥 {obter_titulo(calendario)}")
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

    Se uma consulta falhar, a operação é interrompida para evitar
    repetir a mesma mensagem de erro para todos os animes.
    """
    animes = carregar_animes()

    animes = [
        anime
        for anime in animes
        if anime.get("status") == "RELEASING"
    ]

    if not animes:
        print("\nNenhum anime cadastrado.")
        return

    for anime in animes:
        resultado = buscar_anime(anime["id"])

        # A função da API já informa o motivo da falha.
        # Aqui apenas interrompemos o loop para evitar
        # repetir a mesma mensagem para todos os animes.
        if not resultado:
            print(
                "\n⚠️ Não foi possível carregar "
                "os próximos episódios."
            )
            return

        mostrar_separador()
        print(f"Anime: {obter_titulo(resultado)}")

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


def mostrar_meus_animes(status_filtro=None):
    """
    Mostra os animes cadastrados.

    Quando status_filtro for informado, exibe apenas
    os animes que possuem aquele status.
    """
    animes = carregar_animes()

    if not animes:
        print("\nNenhum anime cadastrado.")
        return

    if status_filtro:
        animes = [
            anime
            for anime in animes
            if anime.get("status") == status_filtro
        ]

    if not animes:
        print("\nNenhum anime encontrado nessa categoria.")
        return

    animes.sort(key=lambda anime: anime["nome"].lower())

    for anime in animes:
        if status_filtro == "FINISHED":
            mostrar_anime_finalizado(anime)
            continue

        status = anime.get("status")
        icone = obter_icone_status(status)

        titulo(f"{icone} {anime['nome']}")

        print(f"Status: {formatar_status(status)}")

        total_episodios = anime.get("episodios")

        if total_episodios is not None:
            print(f"Total de episódios: {total_episodios}")
        else:
            print("Total de episódios ainda não anunciado")

        print("----------------------")


def mostrar_anime_finalizado(anime):
    """Exibe os dados de um anime finalizado."""

    icone = obter_icone_status(anime.get("status"))

    titulo(f"{icone} {anime['nome']}")

    total_episodios = anime.get("episodios")

    if total_episodios is not None:
        print(f"Total de episódios: {total_episodios}")
    else:
        print("Total de episódios: não informado")

    data_finalizacao = anime.get("data_finalizacao")

    if data_finalizacao:
        dia = data_finalizacao.get("day")
        mes = data_finalizacao.get("month")
        ano = data_finalizacao.get("year")

        if dia and mes and ano:
            print(f"Finalizado em: {dia:02d}/{mes:02d}/{ano}")
        else:
            print("Finalizado em: data não informada")
    else:
        print("Finalizado em: data não informada")

    print("----------------------")
