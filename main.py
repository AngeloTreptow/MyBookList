import os
import json
import webbrowser
import platform

from tkinter import filedialog, messagebox
from PIL import Image
import customtkinter as ctk

from gerenciador_livros import GerenciadorLivros
from temas import TEMAS

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ARQUIVO_CONFIG_TEMA = "config_tema.json"
TEMA_PADRAO = "Ocean Night"


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("My Book List")
        self.geometry("900x600")
        self.minsize(800, 500)

        if platform.system() == "Windows":
            self.after(0, lambda: self.state("zoomed"))
        else:
            self.after(0, lambda: self.attributes("-zoomed", True))

        # Frames estruturais
        self.frame_esquerda = None
        self.frame_direita = None
        self.frame_busca = None
        self.frame_lista = None

        # Campos de entrada — Menu Esquerdo
        self.entry_nome = None
        self.entry_autor = None
        self.entry_capitulo = None
        self.entry_editar_id = None
        self.entry_remover = None

        # Campos de entrada — Barra de Busca
        self.entry_busca_id = None
        self.entry_busca_autor = None
        self.entry_busca_nome = None

        # Outros widgets
        self.label_capa = None
        self.botao_cadastrar = None
        self.botao_carregar = None
        self.botao_remover_livro = None
        self.menu_temas = None

        # Controle de Estado e Banco de Dados
        self.tema_atual = self._carregar_tema_salvo()
        self.cores = TEMAS[self.tema_atual]
        self.db = GerenciadorLivros()
        self._editando = False
        self.caminho_capa_atual = self.db.capa_padrao

        # Rastreamento para temas
        self.botoes_remover_cards: list[ctk.CTkButton] = []
        self.cards_widgets: list[dict] = []

        # INICIALIZAÇÃO DA INTERFACE

        # Aplica cor de fundo da janela raiz
        self.configure(fg_color=self.cores["fundo_direito"])

        # Constrói a interface e exibe os livros
        self.construir_layout()
        self.atualizar_lista()

    def _carregar_tema_salvo(self) -> str:
        try:
            with open(ARQUIVO_CONFIG_TEMA, "r", encoding="utf-8") as f:
                dados = json.load(f)
                tema = dados.get("tema", TEMA_PADRAO)
                # Valida que o tema existe; caso contrário usa o padrão
                return tema if tema in TEMAS else TEMA_PADRAO
        except FileNotFoundError:
            return TEMA_PADRAO

    def _salvar_tema(self, nome_tema: str):
        with open(ARQUIVO_CONFIG_TEMA, "w", encoding="utf-8") as f:
            json.dump({"tema": nome_tema}, f)

    def construir_layout(self):
        self.frame_esquerda = ctk.CTkScrollableFrame(
            self, width=320, corner_radius=20,
            fg_color=self.cores["menu_esquerdo"]
        )
        self.frame_esquerda.pack(side="left", fill="y", padx=15, pady=15)

        self.frame_direita = ctk.CTkFrame(
            self, corner_radius=20,
            fg_color=self.cores["fundo_direito"]
        )
        self.frame_direita.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=15)

        self._construir_menu_esquerdo()
        self._construir_menu_direito()

    def _construir_menu_esquerdo(self):
        fe = self.frame_esquerda

        # Titulo
        ctk.CTkLabel(fe, text="Cadastrar / Editar Livro",
                     font=("Arial", 20, "bold")).pack(pady=(15, 20))

        # Campos do formulario
        self.entry_nome = self._criar_campo(fe, "Nome")
        self.entry_autor = self._criar_campo(fe, "Autor")
        self.entry_capitulo = self._criar_campo(fe, "Capítulos")

        # Previa da capa
        self.label_capa = ctk.CTkLabel(fe, text="Sem capa")
        self.label_capa.pack(pady=(5, 10))
        self.mostrar_capa(self.caminho_capa_atual)

        ctk.CTkButton(fe, text="Escolher Capa",
                      command=self.escolher_capa).pack(padx=15, pady=(0, 15))

        # Botao de cadastro
        self.botao_cadastrar = ctk.CTkButton(
            fe, text="Cadastrar Livro", command=self.acao_cadastrar
        )
        self.botao_cadastrar.pack(padx=15, pady=5)

        # Seção Editar por ID
        ctk.CTkLabel(fe, text="ID para editar").pack(anchor="w", padx=15, pady=(20, 0))
        self.entry_editar_id = ctk.CTkEntry(fe, width=250)
        self.entry_editar_id.pack(padx=15, pady=(0, 10))

        self.botao_carregar = ctk.CTkButton(
            fe, text="Carregar Dados", command=self.preencher_para_editar
        )
        self.botao_carregar.pack(padx=15, pady=5)

        ctk.CTkButton(fe, text="Salvar Edição",
                      command=self.acao_editar).pack(padx=15, pady=5)

        # Seção de Deletar por ID
        ctk.CTkLabel(fe, text="ID para remover").pack(anchor="w", padx=15, pady=(20, 0))
        self.entry_remover = ctk.CTkEntry(fe, width=250)
        self.entry_remover.pack(padx=15, pady=(0, 10))

        self.botao_remover_livro = ctk.CTkButton(
            fe, text="Remover Livro",
            fg_color="red", hover_color="#8b0000",
            command=self.acao_remover
        )
        self.botao_remover_livro.pack(padx=15, pady=5)

        # Separador visual
        ctk.CTkFrame(fe, height=2, fg_color="#333333").pack(fill="x", padx=15, pady=(20, 10))

        # Seletor de Tema
        ctk.CTkLabel(fe, text="Tema Visual").pack(anchor="w", padx=15)
        self.menu_temas = ctk.CTkOptionMenu(
            fe,
            values=list(TEMAS.keys()),
            command=self.mudar_tema
        )
        self.menu_temas.set(self.tema_atual)
        self.menu_temas.pack(padx=15, pady=(5, 10))

        # Link do Repositorio
        ctk.CTkLabel(fe, text="").pack(pady=5)  # espaçamento

        link_github = ctk.CTkLabel(
            fe, text="GitHub",
            font=("Arial", 16, "underline"),
            cursor="hand2",
            text_color=self.cores["texto_secundario"]
        )
        link_github.pack(pady=10)
        link_github.bind(
            "<Button-1>",
            lambda e: webbrowser.open_new("https://github.com/AngeloTreptow/MyBookList")
        )

    def _criar_campo(self, parent, rotulo: str) -> ctk.CTkEntry:
        ctk.CTkLabel(parent, text=rotulo).pack(anchor="w", padx=15)
        entry = ctk.CTkEntry(parent, width=250)
        entry.pack(padx=15, pady=(0, 10))
        return entry

    def _construir_menu_direito(self):
        # Barra de busca
        self.frame_busca = ctk.CTkFrame(
            self.frame_direita, fg_color=self.cores["fundo_direito"]
        )
        self.frame_busca.pack(fill="x", padx=10, pady=10)

        # Busca por ID
        self.entry_busca_id = ctk.CTkEntry(self.frame_busca, placeholder_text="Buscar ID", width=100)
        self.entry_busca_id.pack(side="left", padx=5)
        ctk.CTkButton(self.frame_busca, text="Buscar ID", width=90,
                      command=self.acao_buscar_id).pack(side="left", padx=5)

        # Busca por Autor
        self.entry_busca_autor = ctk.CTkEntry(self.frame_busca, placeholder_text="Buscar Autor", width=140)
        self.entry_busca_autor.pack(side="left", padx=(15, 5))
        ctk.CTkButton(self.frame_busca, text="Buscar Autor", width=100,
                      command=self.acao_buscar_autor).pack(side="left", padx=5)

        # Busca por Nome
        self.entry_busca_nome = ctk.CTkEntry(self.frame_busca, placeholder_text="Buscar Nome", width=140)
        self.entry_busca_nome.pack(side="left", padx=(15, 5))
        ctk.CTkButton(self.frame_busca, text="Buscar Nome", width=100,
                      command=self.acao_buscar_nome).pack(side="left", padx=5)

        # Botão para resetar a busca
        ctk.CTkButton(self.frame_busca, text="Mostrar Todos", width=110,
                      command=self.acao_mostrar_todos).pack(side="right", padx=5)

        # Area de listagem
        self.frame_lista = ctk.CTkScrollableFrame(
            self.frame_direita, fg_color=self.cores["fundo_direito"]
        )
        self.frame_lista.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def mudar_tema(self, escolha: str):
        """
        Troca o tema visual sem reiniciar a aplicação.
        Atualiza todos os widgets já renderizados e persiste a escolha em disco.
        """
        self.tema_atual = escolha
        self.cores = TEMAS[escolha]
        self._salvar_tema(escolha)

        self.configure(fg_color=self.cores["fundo_direito"])
        self.frame_esquerda.configure(fg_color=self.cores["menu_esquerdo"])
        self.frame_direita.configure(fg_color=self.cores["fundo_direito"])

        self.frame_lista.configure(fg_color=self.cores["fundo_direito"])
        self.frame_busca.configure(fg_color=self.cores["fundo_direito"])

        for refs in self.cards_widgets:
            refs["card"].configure(fg_color=self.cores["card_livro"])
            refs["id"].configure(text_color=self.cores["texto_secundario"])
            refs["autor"].configure(text_color=self.cores["texto_secundario"])
            refs["cap"].configure(text_color=self.cores["texto_destaque"])
            refs["btn"].configure(
                fg_color=self.cores["botao_remover"],
                hover_color=self.cores["botao_remover_hover"]
            )

    def atualizar_lista(self, livros=None):

        self.botoes_remover_cards.clear()
        self.cards_widgets.clear()

        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        if livros is None:
            livros = self.db.listar_livros()

        if not livros:
            ctk.CTkLabel(self.frame_lista, text="Nenhum livro encontrado.",
                         font=("Arial", 16)).pack(pady=20)
            return

        for livro in livros:
            self._criar_card_livro(livro)

        if self._editando:
            for btn in self.botoes_remover_cards:
                if btn.winfo_exists():
                    btn.configure(state="disabled")

    def _criar_card_livro(self, livro: dict):
        # Container do card
        card = ctk.CTkFrame(self.frame_lista, corner_radius=18,
                            fg_color=self.cores["card_livro"])
        card.pack(fill="x", padx=8, pady=8)

        # Imagem da capa
        self._renderizar_capa_no_card(card, livro.get("capa"))

        # Informações textuais
        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=5, pady=10)

        ctk.CTkLabel(info, text=livro["nome"],
                     font=("Arial", 20, "bold")).pack(anchor="w")

        label_id = ctk.CTkLabel(
            info, text=f"ID: {livro['id']}",
            text_color=self.cores["texto_secundario"], font=("Arial", 14)
        )
        label_id.pack(anchor="w", pady=(5, 0))

        label_autor = ctk.CTkLabel(
            info, text=f"Autor: {livro['autor']}",
            text_color=self.cores["texto_secundario"], font=("Arial", 14)
        )
        label_autor.pack(anchor="w", pady=(5, 0))

        label_cap = ctk.CTkLabel(
            info, text=f"{livro['capitulo']} capítulos",
            text_color=self.cores["texto_destaque"], font=("Arial", 14, "bold")
        )
        label_cap.pack(anchor="w", pady=(5, 10))

        # Botões de ação do Card
        frame_botoes = ctk.CTkFrame(info, fg_color="transparent")
        frame_botoes.pack(anchor="w")

        ctk.CTkButton(
            frame_botoes, text="Editar", width=90, fg_color="#2563eb",
            command=lambda i=livro["id"]: self.carregar_edicao(i)
        ).pack(side="left", padx=(0, 10))

        btn_remover = ctk.CTkButton(
            frame_botoes, text="Remover", width=90,
            fg_color=self.cores["botao_remover"],
            hover_color=self.cores["botao_remover_hover"],
            command=lambda i=livro["id"]: self.remover_por_card(i)
        )
        btn_remover.pack(side="left")

        # Registra referências para atualização de tema
        self.botoes_remover_cards.append(btn_remover)
        self.cards_widgets.append({
            "card": card,
            "id": label_id,
            "autor": label_autor,
            "cap": label_cap,
            "btn": btn_remover,
        })

    def _renderizar_capa_no_card(self, card: ctk.CTkFrame, caminho_capa: str | None):
        try:
            caminho = caminho_capa if caminho_capa and os.path.exists(caminho_capa) \
                else self.db.capa_padrao

            imagem = Image.open(caminho)
            imagem.thumbnail((80, 120))
            capa_ctk = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=imagem.size)

            label_img = ctk.CTkLabel(card, image=capa_ctk, text="")
            label_img.image = capa_ctk
            label_img.pack(side="left", padx=12, pady=12)

        except Exception as e:
            print(f"[AVISO] Erro ao renderizar capa no card: {e}")
            ctk.CTkLabel(card, text="Sem capa", width=80).pack(side="left", padx=12)

    # AÇÕES — CADASTRO, EDIÇÃO E REMOÇÃO

    def acao_cadastrar(self):
        nome = self.entry_nome.get().strip()
        autor = self.entry_autor.get().strip()
        cap_texto = self.entry_capitulo.get().strip()

        if not nome or not autor or not cap_texto:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return

        try:
            capitulo = int(cap_texto)
        except ValueError:
            messagebox.showwarning("Erro", "Capítulos deve ser um número inteiro.")
            return

        self.db.cadastrar_livro(nome, autor, capitulo, self.caminho_capa_atual)
        self._limpar_campos_cadastro()
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")

    def preencher_para_editar(self):
        try:
            id_livro = int(self.entry_editar_id.get().strip())
        except ValueError:
            messagebox.showwarning("Erro", "Digite um ID válido.")
            return

        livro = self.db.buscar_por_id(id_livro)
        if not livro:
            messagebox.showwarning("Erro", "Livro não encontrado.")
            return

        # Preenche os campos com os dados atuais do livro
        self._limpar_campos_cadastro()
        self.entry_nome.insert(0, livro["nome"])
        self.entry_autor.insert(0, livro["autor"])
        self.entry_capitulo.insert(0, str(livro["capitulo"]))

        self.caminho_capa_atual = livro.get("capa", self.db.capa_padrao)
        self.mostrar_capa(self.caminho_capa_atual)

        # Desativa controles para evitar conflitos durante a edição
        self._set_estado_edicao(editando=True)

    def acao_editar(self):
        try:
            id_livro = int(self.entry_editar_id.get().strip())
            capitulo = int(self.entry_capitulo.get())
        except ValueError:
            messagebox.showwarning("Erro", "ID e capítulos devem ser números inteiros.")
            return

        nome = self.entry_nome.get().strip()
        autor = self.entry_autor.get().strip()

        if not nome or not autor:
            messagebox.showwarning("Erro", "Preencha nome e autor.")
            return

        if self.db.editar_livro(id_livro, nome, autor, capitulo, self.caminho_capa_atual):
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Livro editado com sucesso!")
            self._limpar_campos_cadastro()
            self.entry_editar_id.delete(0, "end")
        else:
            messagebox.showwarning("Erro", "Livro não encontrado.")

    def acao_remover(self):
        try:
            id_livro = int(self.entry_remover.get().strip())
        except ValueError:
            messagebox.showwarning("Erro", "Digite um ID válido.")
            return

        if self.db.remover_livro(id_livro):
            self.atualizar_lista()
            self.entry_remover.delete(0, "end")
            messagebox.showinfo("Sucesso", "Livro removido com sucesso!")
        else:
            messagebox.showwarning("Erro", "Livro não encontrado.")

    def remover_por_card(self, id_livro: int):
        if messagebox.askyesno("Remover", "Tem certeza que deseja remover este livro?"):
            self.db.remover_livro(id_livro)
            self.atualizar_lista()

    def carregar_edicao(self, id_livro: int):
        self.entry_editar_id.configure(state="normal")
        self.entry_editar_id.delete(0, "end")
        self.entry_editar_id.insert(0, str(id_livro))
        self.preencher_para_editar()

    # AÇÕES — BUSCA

    def acao_buscar_id(self):
        try:
            id_livro = int(self.entry_busca_id.get().strip())
        except ValueError:
            messagebox.showwarning("Erro", "Digite um ID válido.")
            return

        livro = self.db.buscar_por_id(id_livro)
        if livro:
            self.atualizar_lista([livro])
        else:
            messagebox.showwarning("Erro", "Livro não encontrado.")

    def acao_buscar_autor(self):
        autor = self.entry_busca_autor.get().strip()
        if autor:
            self.atualizar_lista(self.db.buscar_por_autor(autor))
        else:
            messagebox.showwarning("Erro", "Digite o nome do autor.")

    def acao_buscar_nome(self):
        nome = self.entry_busca_nome.get().strip()
        if nome:
            self.atualizar_lista(self.db.buscar_por_nome(nome))
        else:
            messagebox.showwarning("Erro", "Digite o início do nome do livro.")

    def acao_mostrar_todos(self):
        self.atualizar_lista()

    # CAPA — SELEÇÃO E EXIBIÇÃO

    def escolher_capa(self):
        arquivo = filedialog.askopenfilename(
            title="Escolher capa",
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")]
        )
        if arquivo:
            self.caminho_capa_atual = arquivo
            self.mostrar_capa(arquivo)

    def mostrar_capa(self, caminho: str):
        try:
            if not os.path.exists(caminho):
                caminho = self.db.capa_padrao

            imagem_original = Image.open(caminho)
            imagem_original.thumbnail((120, 180))
            imagem_ctk = ctk.CTkImage(
                light_image=imagem_original,
                dark_image=imagem_original,
                size=imagem_original.size
            )
            self.label_capa.configure(image=imagem_ctk, text="")
            self.label_capa.image = imagem_ctk  # referência para evitar coleta pelo GC

        except Exception as e:
            print(f"[AVISO] Erro ao exibir capa: {e}")
            self.label_capa.configure(text="Erro ao carregar capa", image=None)

    # UTILITÁRIOS INTERNOS

    def _limpar_campos_cadastro(self):

        self.entry_nome.delete(0, "end")
        self.entry_autor.delete(0, "end")
        self.entry_capitulo.delete(0, "end")

        self.caminho_capa_atual = self.db.capa_padrao
        self.mostrar_capa(self.caminho_capa_atual)

        # Reabilita todos os controles que foram bloqueados durante a edição
        self._set_estado_edicao(editando=False)

    def _set_estado_edicao(self, editando: bool):
        self._editando = editando

        estado = "disabled" if editando else "normal"

        self.botao_cadastrar.configure(state=estado)
        self.entry_editar_id.configure(state=estado)
        self.botao_carregar.configure(state=estado)
        self.entry_remover.configure(state=estado)
        self.botao_remover_livro.configure(state=estado)

        for btn in self.botoes_remover_cards:
            if btn.winfo_exists():
                btn.configure(state=estado)


if __name__ == "__main__":
    app = App()
    app.mainloop()
