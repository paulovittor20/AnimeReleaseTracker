import json
from datetime import datetime, timedelta
from pathlib import Path


ARQUIVO_CACHE = Path(__file__).parent / "data" / "cache.json"
TEMPO_CACHE = timedelta(minutes=30)


def carregar_cache():
    """
    Carrega e devolve os dados armazenados na cache.

    Caso o arquivo ainda não exista, cria uma cache vazia.
    """
    if not ARQUIVO_CACHE.exists():
        salvar_cache({})
        return {}

    try:
        with ARQUIVO_CACHE.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except json.JSONDecodeError:
        print("\n⚠️ O arquivo cache.json está vazio ou corrompido.")
        return {}


def salvar_cache(cache):
    """Salva todos os dados da cache no arquivo JSON."""
    ARQUIVO_CACHE.parent.mkdir(parents=True, exist_ok=True)

    with ARQUIVO_CACHE.open("w", encoding="utf-8") as arquivo:
        json.dump(
            cache,
            arquivo,
            indent=4,
            ensure_ascii=False,
        )


def cache_expirou(registro):
    """
    Verifica se um registro da cache ultrapassou
    o tempo máximo de validade.
    """
    atualizado_em = registro.get("atualizado_em")

    if not atualizado_em:
        return True

    try:
        data_atualizacao = datetime.fromisoformat(atualizado_em)

    except ValueError:
        return True

    return datetime.now() - data_atualizacao >= TEMPO_CACHE


def buscar_cache(chave):
    """
    Busca um registro válido na cache.

    Retorna os dados encontrados ou None quando:
    - a chave não existe;
    - o registro está expirado.
    """
    cache = carregar_cache()
    registro = cache.get(chave)

    if not registro:
        return None

    if cache_expirou(registro):
        return None

    return registro.get("dados")


def atualizar_cache(chave, dados):
    """Adiciona ou atualiza um registro da cache."""
    cache = carregar_cache()

    cache[chave] = {
        "atualizado_em": datetime.now().isoformat(),
        "dados": dados,
    }

    salvar_cache(cache)