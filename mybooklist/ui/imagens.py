"""Utilitários de carregamento de imagens para a interface."""

import customtkinter as ctk
from PIL import Image


def criar_imagem_ctk(caminho: str, tamanho_maximo: tuple[int, int]) -> ctk.CTkImage:
    """Abre uma imagem do disco, redimensiona mantendo a proporção e converte para CTkImage."""
    imagem = Image.open(caminho)
    imagem.thumbnail(tamanho_maximo)
    return ctk.CTkImage(light_image=imagem, dark_image=imagem, size=imagem.size)
