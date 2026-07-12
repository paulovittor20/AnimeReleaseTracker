import json
from datetime import datetime 
from api import buscar_animes_por_nome, buscar_anime, buscar_calendario_anime


ARQUIVO = "animes.json"


def formatar_tipo(tipo):

    tipos = {
        "TV": "Anime de TV",
        "ONA": "Anime Online",
        "OVA": "Especial OVA",
        "MOVIE": "Filme",
        "SPECIAL": "Especial",
        "MUSIC": "Clipe Musical"
    }

    return tipos.get(tipo, "Outro")


def formatar_status(status):

    status_nomes = {
        "RELEASING": "Em lançamento",
        "FINISHED": "Finalizado",
        "HIATUS": "Em hiato",
        "NOT_YET_RELEASED": "Ainda não lançado",
        "CANCELLED": "Cancelado"
    }

    return status_nomes.get(status, "Desconhecido")


def carregar_animes():

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)



def salvar_animes(animes):

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(
            animes,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


def atualizar_animes():

    animes = carregar_animes()

    avisos = {
        "finalizados": [],
        "hiato": [],
        "retornos": [],
        "outros": []
    }


    for anime in animes:

        dados = buscar_anime(anime["id"])


        if not dados:
            continue


        status_antigo = anime.get("status")


        nome_novo = (
            dados["title"]["english"]
            if dados["title"]["english"]
            else dados["title"]["romaji"]
        )


        status_novo = dados["status"]

        episodios_novos = dados["episodes"]



        # ==================================
        # Descobre último episódio lançado
        # ==================================

        ultimo_episodio_lancado = 0
        data_ultimo_episodio = None


        if dados["nextAiringEpisode"]:

            ultimo_episodio_lancado = (
                dados["nextAiringEpisode"]["episode"] - 1
            )


            calendario = buscar_calendario_anime(
                anime["id"]
            )


            if calendario:

                episodios = (
                    calendario["airingSchedule"]["nodes"]
                )


                for episodio in episodios:

                    if episodio["episode"] == ultimo_episodio_lancado:


                        data = datetime.fromtimestamp(
                            episodio["airingAt"]
                        )


                        data_ultimo_episodio = (
                            data.strftime("%d/%m/%Y")
                        )


                        break


        elif dados["status"] == "FINISHED":

            ultimo_episodio_lancado = dados["episodes"] or 0



        # ==================================
        # Cria histórico para animes antigos
        # ==================================

        anime["ultimo_episodio_lancado"] = ultimo_episodio_lancado


        if data_ultimo_episodio:
            
            anime["data_ultimo_episodio"] = data_ultimo_episodio


        # ==================================
        # Verifica mudanças de status
        # ==================================

        if status_antigo != status_novo:


            if status_antigo == "RELEASING" and status_novo == "FINISHED":

                mensagem = (
                    f"🎉 {nome_novo}\n"
                    f"A temporada foi finalizada!"
                )

                avisos["finalizados"].append(mensagem)



            elif status_antigo == "RELEASING" and status_novo == "HIATUS":

                mensagem = (
                    f"⏸ {nome_novo}\n"
                    f"O anime entrou em hiato."
                )

                avisos["hiato"].append(mensagem)



            elif status_antigo == "HIATUS" and status_novo == "RELEASING":

                mensagem = (
                    f"🔥 {nome_novo}\n"
                    f"O anime voltou do hiato!"
                )

                avisos["retornos"].append(mensagem)



            elif status_antigo == "NOT_YET_RELEASED" and status_novo == "RELEASING":

                mensagem = (
                    f"🚀 {nome_novo}\n"
                    f"O anime começou a ser lançado!"
                )

                avisos["outros"].append(mensagem)



            else:

                mensagem = (
                    f"🔄 {nome_novo}\n"
                    f"Status alterado: "
                    f"{formatar_status(status_antigo)} → "
                    f"{formatar_status(status_novo)}"
                )

                avisos["outros"].append(mensagem)



        # ==================================
        # Atualiza informações salvas
        # ==================================

        anime["nome"] = nome_novo

        anime["tipo"] = dados["format"]

        anime["episodios"] = episodios_novos

        anime["status"] = status_novo



    salvar_animes(animes)


    return avisos



def adicionar_anime():

    while True:

        nome = input("\nDigite o nome do anime (ou 0 para voltar): ")


        if nome == "0":

            return


        resultados = buscar_animes_por_nome(nome)


        resultados.sort(
            key=lambda anime: anime["title"]["romaji"]
        )


        if not resultados:

            print("\nNenhum anime encontrado. Tente novamente.")

            continue


        break


    print("\nResultados encontrados:\n")

    print("0 - Voltar:\n")


    for indice, anime in enumerate(resultados):

        if anime["title"]["english"]:
            titulo = anime["title"]["english"]

        else:
            titulo = anime["title"]["romaji"]

        print(f"{indice + 1} - {titulo}")

        print(
            "   Tipo:",
            formatar_tipo(anime["format"])
        )

        print(
            "   Episódios:",
            anime["episodes"] or "Não informado"
        )

        print(
            "   Status:",
            formatar_status(anime["status"])
        )

        print()


    try:

        escolha = int(
            input("\nEscolha o anime: ")
    )


    except ValueError:

        print("\nDigite apenas números.")

        return
        


    if escolha == 0:

        return


    if escolha < 0 or escolha > len(resultados):

        print("\nOpção inválida.")

        return


    anime_escolhido = resultados[escolha - 1]


    animes = carregar_animes()


    for anime in animes:

        if anime["id"] == anime_escolhido["id"]:

            print("\n⚠️ Esse anime já foi adicionado!")

            detalhes = buscar_anime(anime["id"])

            if detalhes["nextAiringEpisode"]:

                print(
                    "Próximo episódio:",
                    detalhes["nextAiringEpisode"]["episode"]
                )

            return



    if anime_escolhido["title"]["english"]:

        nome_salvar = anime_escolhido["title"]["english"]

    else:

        nome_salvar = anime_escolhido["title"]["romaji"]


    novo_anime = {
        "nome": nome_salvar,
        "id": anime_escolhido["id"],
        "tipo": anime_escolhido["format"],
        "episodios": anime_escolhido["episodes"],
        "status": anime_escolhido["status"],
        "ultimo_episodio": 0
    }


    animes.append(novo_anime)


    salvar_animes(animes)


    print("\n✅ Anime adicionado com sucesso!")

def remover_anime():

    animes = carregar_animes()


    if not animes:

        print("\nNenhum anime cadastrado.")
        return


    print("\nAnimes cadastrados:\n")


    for indice, anime in enumerate(animes):

        print(
            f"{indice + 1} - {anime['nome']}"
        )


    escolha = int(
        input("\nEscolha o anime que deseja remover: ")
    )


    if escolha < 1 or escolha > len(animes):

        print("Opção inválida.")
        return


    anime_removido = animes[escolha - 1]


    confirmar = input(
        f"\nTem certeza que deseja remover "
        f"{anime_removido['nome']}? (s/n): "
    )


    if confirmar.lower() == "s":

        animes.pop(escolha - 1)

        salvar_animes(animes)

        print(
            "\n✅ Anime removido com sucesso!"
        )

    else:

        print(
            "\nOperação cancelada."
        )