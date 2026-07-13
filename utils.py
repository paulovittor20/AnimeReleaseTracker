def obter_titulo(anime):
    """
    Retorna o melhor título disponível para um anime.

    Dá preferência ao título em inglês e utiliza o título
    em romaji quando o inglês não estiver disponível.
    """
    titulos = anime.get("title", {})

    return (
        titulos.get("english")
        or titulos.get("romaji")
        or "Título desconhecido"
    )


def formatar_tipo(tipo):
    """Converte o formato da AniList para um nome em português."""
    tipos = {
        "TV": "Anime de TV",
        "ONA": "Anime Online",
        "OVA": "Especial OVA",
        "MOVIE": "Filme",
        "SPECIAL": "Especial",
        "MUSIC": "Clipe Musical",
    }

    return tipos.get(tipo, "Outro")


def formatar_status(status):
    """Converte o status da AniList para um nome em português."""
    status_nomes = {
        "RELEASING": "Em lançamento",
        "FINISHED": "Finalizado",
        "HIATUS": "Em hiato",
        "NOT_YET_RELEASED": "Ainda não lançado",
        "CANCELLED": "Cancelado",
    }

    return status_nomes.get(status, "Desconhecido")