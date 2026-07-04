"""Janela principal do My Book List: construção da interface e handlers de eventos."""

import os
import webbrowser

from tkinter import filedialog, messagebox, TclError
import customtkinter as ctk

from mybooklist.ui.card_livro import CardLivro
from mybooklist.config.config_tema import carregar_tema_salvo, salvar_tema
from mybooklist.core.gerenciador_livros import GerenciadorLivros
from mybooklist.ui.imagens import criar_imagem_ctk
from mybooklist.config.temas import TEMAS

TAMANHO_CAPA_PREVIA = (120, 180)
URL_REPOSITORIO = "https://github.com/AngeloTreptow/MyBookList"


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("My Book List")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.after(0, self._maximizar_janela)

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
        self.tema_atual = carregar_tema_salvo()
        self.cores = TEMAS[self.tema_atual]
        self.db = GerenciadorLivros()
        self._editando = False
        self.caminho_capa_atual = self.db.capa_padrao

        # Cards renderizados (para atualização de tema e estado de edição)
        self.cards: list[CardLivro] = []

        # Aplica cor de fundo da janela raiz
        self.configure(fg_color=self.cores["fundo_direito"])

        # Constrói a interface e exibe os livros
        self.construir_layout()
        self.atualizar_lista()

    def _maximizar_janela(self):
        """Maximiza a janela de forma portátil.

        `state("zoomed")` cobre Windows e alguns ambientes Linux; `-zoomed`
        cobre a maioria dos window managers Linux. Se ambos falharem, cai no
        plano B universal: dimensiona a janela para ocupar a tela inteira.
        """
        try:
            self.state("zoomed")
            return
        except TclError:
            pass

        try:
            self.attributes("-zoomed", True)
            return
        except TclError:
            pass

        largura = self.winfo_screenwidth()
        altura = self.winfo_screenheight()
        self.geometry(f"{largura}x{altura}+0+0")

    # CONSTRUÇÃO DA INTERFACE

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
        link_github.bind("<Button-1>", lambda e: webbrowser.open_new(URL_REPOSITORIO))

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

    # TEMA

    def mudar_tema(self, escolha: str):
        """
        Troca o tema visual sem reiniciar a aplicação.
        Atualiza todos os widgets já renderizados e persiste a escolha em disco.
        """
        self.tema_atual = escolha
        self.cores = TEMAS[escolha]
        salvar_tema(escolha)

        self.configure(fg_color=self.cores["fundo_direito"])
        self.frame_esquerda.configure(fg_color=self.cores["menu_esquerdo"])
        self.frame_direita.configure(fg_color=self.cores["fundo_direito"])

        self.frame_lista.configure(fg_color=self.cores["fundo_direito"])
        self.frame_busca.configure(fg_color=self.cores["fundo_direito"])

        for card in self.cards:
            card.aplicar_tema(self.cores)

    # LISTAGEM

    def atualizar_lista(self, livros: list[dict] | None = None):
        self.cards.clear()

        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        if livros is None:
            livros = self.db.listar_livros()

        if not livros:
            ctk.CTkLabel(self.frame_lista, text="Nenhum livro encontrado.",
                         font=("Arial", 16)).pack(pady=20)
            return

        for livro in livros:
            card = CardLivro(
                self.frame_lista,
                livro=livro,
                cores=self.cores,
                capa_padrao=self.db.capa_padrao,
                ao_editar=self.carregar_edicao,
                ao_remover=self.remover_por_card,
            )
            card.pack(fill="x", padx=8, pady=8)
            self.cards.append(card)

        if self._editando:
            for card in self.cards:
                card.definir_remocao_habilitada(False)

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
        id_livro = self._ler_id(self.entry_editar_id)
        if id_livro is None:
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
        id_livro = self._ler_id(self.entry_remover)
        if id_livro is None:
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
        id_livro = self._ler_id(self.entry_busca_id)
        if id_livro is None:
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

            imagem_ctk = criar_imagem_ctk(caminho, TAMANHO_CAPA_PREVIA)
            self.label_capa.configure(image=imagem_ctk, text="")
            self.label_capa.image = imagem_ctk  # referência para evitar coleta pelo GC

        except Exception as e:
            print(f"[AVISO] Erro ao exibir capa: {e}")
            self.label_capa.configure(text="Erro ao carregar capa", image=None)

    # UTILITÁRIOS INTERNOS

    def _ler_id(self, entry: ctk.CTkEntry) -> int | None:
        """Lê um ID inteiro do campo; exibe aviso e retorna None se inválido."""
        try:
            return int(entry.get().strip())
        except ValueError:
            messagebox.showwarning("Erro", "Digite um ID válido.")
            return None

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

        for card in self.cards:
            card.definir_remocao_habilitada(not editando)
