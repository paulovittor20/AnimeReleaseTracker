import json
from datetime import datetime
from api import buscar_anime, buscar_calendario_anime 


dias = [
    "segunda",
    "terça",
    "quarta",
    "quinta",
    "sexta",
    "sábado",
    "domingo"
]

def obter_nome_anime(anime):

    if anime["title"]["english"]:
        return anime["title"]["english"]

    else:
        return anime["title"]["romaji"]
    

def formatar_data(timestamp):

    data = datetime.fromtimestamp(timestamp)

    data_formatada = data.strftime("%d/%m às %H:%M")

    dia_semana = dias[data.weekday()]

    return f"{dia_semana}, {data_formatada}"

def episodio_e_hoje(timestamp):

    data_episodio = datetime.fromtimestamp(timestamp)

    hoje = datetime.now()


    return (
        data_episodio.date() == hoje.date()
    )


def mostrar_episodios_de_hoje():

    with open("animes.json", "r", encoding="utf-8") as arquivo:
        animes = json.load(arquivo)


    hoje = datetime.now().date()

    encontrados = False


    for anime in animes:

        resultado = buscar_anime(anime["id"])


        if resultado is None:
            continue


        calendario = buscar_calendario_anime(anime["id"])



        if calendario is None:
            continue


        episodios = calendario["airingSchedule"]["nodes"]


        for episodio in episodios:

            data_episodio = datetime.fromtimestamp(
                episodio["airingAt"]
            )


            if data_episodio.date() == hoje:


                encontrados = True


                print("----------------")
                print(
                    "🔥",
                    obter_nome_anime(resultado)
                )

                print(
                    "Episódio:",
                    episodio["episode"]
                )


                agora = datetime.now()


                if agora >= data_episodio:

                    print(
                        "✅ Episódio lançado hoje!"
                    )

                    print(
                        "Lançou às:",
                        data_episodio.strftime("%H:%M")
                    )

                else:

                    print(
                        "⏰ Sai hoje às:",
                        data_episodio.strftime("%H:%M")
                    )



    if not encontrados:

        print(
            "Nenhum episódio lança hoje."
        )


def mostrar_episodios():
    with open("animes.json", "r", encoding="utf-8") as arquivo:
        animes = json.load(arquivo)


    for anime in animes:

        resultado = buscar_anime(anime["id"])

        print("----------------")
        print("Anime:", obter_nome_anime(resultado))




        if resultado["nextAiringEpisode"]:

            episodio = resultado["nextAiringEpisode"]["episode"]

            timestamp = resultado["nextAiringEpisode"]["airingAt"]

            data_formatada = formatar_data(timestamp)

            if episodio_e_hoje(timestamp):
                print("🔥 EPISÓDIO LANÇA HOJE!")
                
            print("Próximo episódio:", episodio)
            print(f"Lançamento: {data_formatada}")


        else:

            if resultado["status"] == "FINISHED":

                print("🏁 Anime finalizado")

            elif resultado["status"] == "HIATUS":

                print("⏸️ Anime em hiato")

            else:

                print("Sem próximo episódio anunciado")

        if resultado["episodes"]:

            print(
                "Total de episódios:",
                resultado["episodes"]
            )

        else:

            print(
                "Total de episódios ainda não anunciado"
            )

def mostrar_episodios_lancados_hoje():

    with open("animes.json", "r", encoding="utf-8") as arquivo:
        animes = json.load(arquivo)


    hoje = datetime.now().date()

    encontrou = False


    for anime in animes:

        calendario = buscar_calendario_anime(anime["id"])


        if calendario is None:
            continue


        episodios = calendario["airingSchedule"]["nodes"]


        for episodio in episodios:


            data_episodio = datetime.fromtimestamp(
                episodio["airingAt"]
            )


            if data_episodio.date() == hoje:

                encontrou = True


                print("----------------")
                print("🔥", obter_nome_anime(calendario))
                print(
                    "Episódio:",
                    episodio["episode"]
                )
                print(
                    "Lançou às:",
                    data_episodio.strftime("%H:%M")
                )


    if not encontrou:

        print(
            "Nenhum episódio lançado hoje."
        )

def verificar_status_animes():

    with open("animes.json", "r", encoding="utf-8") as arquivo:
        animes = json.load(arquivo)


    encontrou = False


    for anime in animes:

        resultado = buscar_anime(anime["id"])


        if resultado is None:
            continue


        status = resultado["status"]


        if status == "FINISHED":

            encontrou = True

            print("----------------")
            print("🏁 Temporada finalizada!")
            print(
                 obter_nome_anime(resultado)
            )

            print(
                "Total de episódios:",
                resultado["episodes"]
            )


        elif status == "HIATUS":

            encontrou = True

            print("----------------")
            print("⏸️ Anime em hiato!")
            print(
                 obter_nome_anime(resultado)
            )


            if resultado["nextAiringEpisode"]:

                data = datetime.fromtimestamp(
                    resultado["nextAiringEpisode"]["airingAt"]
                )


                print(
                    "Retorno previsto:",
                    data.strftime("%d/%m às %H:%M")
                )

            else:

                print(
                    "Sem data de retorno anunciada."
                )


    if not encontrou:

        print(
            "Nenhum anime finalizado ou em hiato."
        )

        