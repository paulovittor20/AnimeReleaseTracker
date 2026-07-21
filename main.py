import os

from database import inicializar_banco

from anime_manager import adicionar_anime, atualizar_animes, remover_anime
from tracker import(
     mostrar_episodios,
    mostrar_episodios_de_hoje,
    mostrar_meus_animes,
    )


def limpar_tela():
    """Limpa o terminal no Windows, Linux ou macOS."""
    comando = "cls" if os.name == "nt" else "clear"
    os.system(comando)


def mostrar_categoria_de_avisos(titulo, avisos):
    """
    Exibe uma categoria de avisos.

    Esta função evita repetir o mesmo bloco de código
    para temporadas finalizadas, hiatos, retornos etc.
    """
    if not avisos:
        return

    print(titulo)
    print()

    for aviso in avisos:
        print(aviso)
        print()


def mostrar_avisos(avisos):
    """Exibe as mudanças encontradas durante a atualização dos animes."""
    if not any(avisos.values()):
        return

    print("======================")
    print("🔔 Novidades encontradas")
    print("======================\n")

    mostrar_categoria_de_avisos(
    "🔥 Novos episódios",
    avisos["episodios"],
)

    mostrar_categoria_de_avisos(
        "🎉 Temporadas finalizadas",
        avisos["finalizados"],
    )

    mostrar_categoria_de_avisos(
        "⏸ Animes em hiato",
        avisos["hiato"],
    )

    mostrar_categoria_de_avisos(
        "🔥 Retornos",
        avisos["retornos"],
    )

    mostrar_categoria_de_avisos(
        "🔄 Outras alterações",
        avisos["outros"],
    )


def menu():
    """Exibe as opções disponíveis no programa."""
    print("======================")
    print(" Anime Release Tracker ")
    print("======================")

    print("1 - Ver próximos episódios")
    print("2 - Adicionar anime")
    print("3 - Meus animes")
    print("4 - Episódios de hoje")
    print("5 - Remover anime")
    print("0 - Sair")


def menu_meus_animes():
    """Exibe os filtros disponíveis para a biblioteca do usuário."""

    while True:
        limpar_tela()

        print("======================")
        print("      Meus animes")
        print("======================")
        print("1 - Todos")
        print("2 - Em lançamento")
        print("3 - Finalizados")
        print("4 - Em hiato")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        limpar_tela()

        if opcao == "1":
            mostrar_meus_animes()

        elif opcao == "2":
            mostrar_meus_animes("RELEASING")

        elif opcao == "3":
            mostrar_meus_animes("FINISHED")

        elif opcao == "4":
            mostrar_meus_animes("HIATUS")

        elif opcao == "0":
            break

        else:
            print("\n⚠️ Opção inválida. Escolha um número de 0 a 4.")

        input("\nPressione ENTER para continuar...")

def executar_programa():
    """Inicializa o tracker e mantém o menu principal em execução."""

    inicializar_banco()

    # Atualiza os animes uma única vez quando o programa é iniciado.
    avisos = atualizar_animes()

    if any(avisos.values()):
        mostrar_avisos(avisos)
        input("\nPressione ENTER para continuar...")

    while True:
        limpar_tela()
        menu()

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            mostrar_episodios()

        elif opcao == "2":
            adicionar_anime()

        elif opcao == "3":
            menu_meus_animes()

        elif opcao == "4":
            mostrar_episodios_de_hoje()

        elif opcao == "5":
            remover_anime()

        elif opcao == "0":
            print("\nAté mais!")
            break

        else:
            print("\n⚠️ Opção inválida. Escolha um número de 1 a 5.")

        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    executar_programa()