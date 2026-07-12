import os 

from tracker import mostrar_episodios, mostrar_episodios_de_hoje
from anime_manager import adicionar_anime, remover_anime, atualizar_animes

def limpar_tela():
    os.system("cls")

def mostrar_avisos(avisos):

    if not any(avisos.values()):

        return


    print("======================")
    print("🔔 Novidades encontradas")
    print("======================\n")


    if avisos["finalizados"]:

        print("🎉 Temporadas finalizadas\n")

        for aviso in avisos["finalizados"]:

            print(aviso)
            print()



    if avisos["hiato"]:

        print("⏸ Animes em hiato\n")

        for aviso in avisos["hiato"]:

            print(aviso)
            print()



    if avisos["retornos"]:

        print("🔥 Retornos\n")

        for aviso in avisos["retornos"]:

            print(aviso)
            print()



    if avisos["outros"]:

        print("🔄 Outras alterações\n")

        for aviso in avisos["outros"]:

            print(aviso)
            print()

def menu():

    print("======================")
    print(" Anime Release Tracker ")
    print("======================")

    print("1 - Ver próximos episódios")
    print("2 - Adicionar anime")
    print("3 - Episódios de hoje")
    print("4 - Remover anime")
    print("5 - Sair")

avisos = atualizar_animes()

if any(avisos.values()):

    mostrar_avisos(avisos)

    input("\nPressione ENTER para continuar...")


while True:

    limpar_tela()

    menu()

    opcao = input("\nEscolha uma opção: ")


    if opcao == "1":

        mostrar_episodios()


    elif opcao == "2":

        adicionar_anime()


    elif opcao == "3":

        mostrar_episodios_de_hoje()


    elif opcao == "4":

        remover_anime()


    elif opcao == "5":

        print("Até mais!")

        break


    else:

        print("\n⚠️ Opção inválida. Escolha um número de 1 a 5.")



    input("\nPressione ENTER para continuar...")

    limpar_tela()