import sqlite3
import time
from pathlib import Path


PASTA_PROJETO = Path(__file__).parent
CAMINHO_BANCO = PASTA_PROJETO / "data" / "animes.db"


def criar_conexao():
    """Cria e devolve uma conexão com o banco SQLite."""
    CAMINHO_BANCO.parent.mkdir(exist_ok=True)

    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row

    return conexao


def criar_tabelas(conexao):
    """Cria as tabelas necessárias para o funcionamento do sistema."""
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animes (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            status TEXT NOT NULL,
            episodios INTEGER,
            ultimo_episodio INTEGER,
            data_ultimo_episodio TEXT,
            data_finalizacao TEXT,
            adicionado_em INTEGER NOT NULL
        )
    """)

    conexao.commit()


def inicializar_banco():
    """Inicializa o banco e garante que as tabelas existam."""
    conexao = criar_conexao()

    try:
        criar_tabelas(conexao)
    finally:
        conexao.close()


def converter_data_finalizacao_para_banco(data):
    """Converte a data da AniList para o formato YYYY-MM-DD."""
    if not data:
        return None

    ano = data.get("year")
    mes = data.get("month")
    dia = data.get("day")

    if not ano or not mes or not dia:
        return None

    return f"{ano:04d}-{mes:02d}-{dia:02d}"


def converter_data_finalizacao_para_anilist(data):
    """Converte YYYY-MM-DD para o dicionário usado no projeto."""
    if not data:
        return None

    try:
        ano, mes, dia = map(int, data.split("-"))
    except (AttributeError, TypeError, ValueError):
        return None

    return {
        "year": ano,
        "month": mes,
        "day": dia,
    }


def linha_para_anime(linha):
    """Converte uma linha do SQLite para o formato usado pelo projeto."""
    anime = {
        "id": linha["id"],
        "nome": linha["nome"],
        "tipo": linha["tipo"],
        "status": linha["status"],
        "episodios": linha["episodios"],
        "ultimo_episodio_lancado": linha["ultimo_episodio"] or 0,
    }

    if linha["data_ultimo_episodio"]:
        anime["data_ultimo_episodio"] = linha["data_ultimo_episodio"]

    data_finalizacao = converter_data_finalizacao_para_anilist(
        linha["data_finalizacao"]
    )

    if data_finalizacao:
        anime["data_finalizacao"] = data_finalizacao

    return anime


def buscar_todos_animes():
    """Busca e devolve todos os animes cadastrados no SQLite."""
    inicializar_banco()
    conexao = criar_conexao()

    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM animes ORDER BY nome COLLATE NOCASE")
        linhas = cursor.fetchall()

        return [linha_para_anime(linha) for linha in linhas]
    finally:
        conexao.close()


def salvar_todos_animes(animes):
    """
    Sincroniza a lista recebida com o banco.

    Insere novos animes, atualiza os existentes e remove do banco
    os que não estiverem mais na lista.
    """
    inicializar_banco()
    conexao = criar_conexao()
    cursor = conexao.cursor()

    try:
        ids_atuais = []

        for anime in animes:
            anime_id = anime["id"]
            ids_atuais.append(anime_id)

            cursor.execute("""
                INSERT INTO animes (
                    id,
                    nome,
                    tipo,
                    status,
                    episodios,
                    ultimo_episodio,
                    data_ultimo_episodio,
                    data_finalizacao,
                    adicionado_em
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    nome = excluded.nome,
                    tipo = excluded.tipo,
                    status = excluded.status,
                    episodios = excluded.episodios,
                    ultimo_episodio = excluded.ultimo_episodio,
                    data_ultimo_episodio = excluded.data_ultimo_episodio,
                    data_finalizacao = excluded.data_finalizacao
            """, (
                anime_id,
                anime["nome"],
                anime["tipo"],
                anime["status"],
                anime.get("episodios"),
                anime.get(
                    "ultimo_episodio_lancado",
                    anime.get("ultimo_episodio", 0),
                ),
                anime.get("data_ultimo_episodio"),
                converter_data_finalizacao_para_banco(
                    anime.get("data_finalizacao")
                ),
                int(time.time()),
            ))

        if ids_atuais:
            marcadores = ", ".join("?" for _ in ids_atuais)
            cursor.execute(
                f"DELETE FROM animes WHERE id NOT IN ({marcadores})",
                ids_atuais,
            )
        else:
            cursor.execute("DELETE FROM animes")

        conexao.commit()

    except (KeyError, sqlite3.Error, TypeError) as erro:
        conexao.rollback()
        raise RuntimeError(
            f"Não foi possível salvar os animes no banco: {erro}"
        ) from erro

    finally:
        conexao.close()


if __name__ == "__main__":
    inicializar_banco()
