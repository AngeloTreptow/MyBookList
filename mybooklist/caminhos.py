"""Resolução de caminhos de dados da aplicação."""

import os
import sys


def dir_base() -> str:
    """Diretório onde os dados da aplicação residem (livros.json, capas/, config do tema).

    Empacotado pelo PyInstaller, é a pasta do executável (app portátil);
    em desenvolvimento, é a raiz do projeto (pai do pacote mybooklist).
    Assim os dados não dependem do diretório de onde o programa foi iniciado.
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
