"""Persistência da preferência de tema do usuário."""

import json
import os

from mybooklist.caminhos import dir_base
from mybooklist.config.temas import TEMAS

# Ancorado no diretório base da aplicação, independente do CWD.
ARQUIVO_CONFIG_TEMA = os.path.join(dir_base(), "config_tema.json")
TEMA_PADRAO = "Ocean Night"


def carregar_tema_salvo() -> str:
    """Lê o tema salvo em disco; retorna o padrão se o arquivo não existir, estiver corrompido ou o tema for desconhecido."""
    try:
        with open(ARQUIVO_CONFIG_TEMA, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return TEMA_PADRAO

    tema = dados.get("tema", TEMA_PADRAO)
    return tema if tema in TEMAS else TEMA_PADRAO


def salvar_tema(nome_tema: str) -> None:
    with open(ARQUIVO_CONFIG_TEMA, "w", encoding="utf-8") as f:
        json.dump({"tema": nome_tema}, f)
