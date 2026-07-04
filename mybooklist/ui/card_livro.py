"""Componente visual de um livro na listagem."""

import os
from typing import Callable

import customtkinter as ctk

from mybooklist.ui.imagens import criar_imagem_ctk

COR_BOTAO_EDITAR = "#2563eb"
TAMANHO_CAPA_CARD = (80, 120)


class CardLivro(ctk.CTkFrame):
    """Card com capa, dados do livro e botões de Editar/Remover.

    Mantém referências apenas aos widgets que mudam com o tema,
    expostos via `aplicar_tema` e `definir_remocao_habilitada`.
    """

    def __init__(
            self,
            master,
            livro: dict,
            cores: dict,
            capa_padrao: str,
            ao_editar: Callable[[int], None],
            ao_remover: Callable[[int], None],
    ):
        super().__init__(master, corner_radius=18, fg_color=cores["card_livro"])

        self._renderizar_capa(livro.get("capa"), capa_padrao)

        # Informações textuais
        info = ctk.CTkFrame(self, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=5, pady=10)

        ctk.CTkLabel(info, text=livro["nome"],
                     font=("Arial", 20, "bold")).pack(anchor="w")

        self.label_id = ctk.CTkLabel(
            info, text=f"ID: {livro['id']}",
            text_color=cores["texto_secundario"], font=("Arial", 14)
        )
        self.label_id.pack(anchor="w", pady=(5, 0))

        self.label_autor = ctk.CTkLabel(
            info, text=f"Autor: {livro['autor']}",
            text_color=cores["texto_secundario"], font=("Arial", 14)
        )
        self.label_autor.pack(anchor="w", pady=(5, 0))

        self.label_capitulos = ctk.CTkLabel(
            info, text=f"{livro['capitulo']} capítulos",
            text_color=cores["texto_destaque"], font=("Arial", 14, "bold")
        )
        self.label_capitulos.pack(anchor="w", pady=(5, 10))

        # Botões de ação do card
        frame_botoes = ctk.CTkFrame(info, fg_color="transparent")
        frame_botoes.pack(anchor="w")

        ctk.CTkButton(
            frame_botoes, text="Editar", width=90, fg_color=COR_BOTAO_EDITAR,
            command=lambda: ao_editar(livro["id"])
        ).pack(side="left", padx=(0, 10))

        self.botao_remover = ctk.CTkButton(
            frame_botoes, text="Remover", width=90,
            fg_color=cores["botao_remover"],
            hover_color=cores["botao_remover_hover"],
            command=lambda: ao_remover(livro["id"])
        )
        self.botao_remover.pack(side="left")

    def _renderizar_capa(self, caminho_capa: str | None, capa_padrao: str):
        try:
            caminho = caminho_capa if caminho_capa and os.path.exists(caminho_capa) \
                else capa_padrao

            capa_ctk = criar_imagem_ctk(caminho, TAMANHO_CAPA_CARD)
            label_img = ctk.CTkLabel(self, image=capa_ctk, text="")
            label_img.image = capa_ctk  # referência para evitar coleta pelo GC
            label_img.pack(side="left", padx=12, pady=12)

        except Exception as e:
            print(f"[AVISO] Erro ao renderizar capa no card: {e}")
            ctk.CTkLabel(self, text="Sem capa", width=80).pack(side="left", padx=12)

    def aplicar_tema(self, cores: dict):
        self.configure(fg_color=cores["card_livro"])
        self.label_id.configure(text_color=cores["texto_secundario"])
        self.label_autor.configure(text_color=cores["texto_secundario"])
        self.label_capitulos.configure(text_color=cores["texto_destaque"])
        self.botao_remover.configure(
            fg_color=cores["botao_remover"],
            hover_color=cores["botao_remover_hover"]
        )

    def definir_remocao_habilitada(self, habilitada: bool):
        if self.botao_remover.winfo_exists():
            self.botao_remover.configure(state="normal" if habilitada else "disabled")
