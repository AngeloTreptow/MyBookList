from tkinter import filedialog, messagebox
from PIL import Image
import customtkinter as ctk
import os
import json

from livro import GerenciadorLivros

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("My Book List")
        self.geometry("1200x800")
        self.minsize(800, 500)

        self.temas = {
            "Dracula": {
                "menu_esquerdo": "#21222C", "fundo_direito": "#282A36", "card_livro": "#44475A",
                "texto_secundario": "#6272A4", "texto_destaque": "#FF79C6",
                "botao_remover": "#FF5555", "botao_remover_hover": "#FF6E6E"
            },
            "Cyberpunk": {
                "menu_esquerdo": "#0D0D0D", "fundo_direito": "#000000", "card_livro": "#1A1A24",
                "texto_secundario": "#A6A6A6", "texto_destaque": "#00FFCC",
                "botao_remover": "#FF0055", "botao_remover_hover": "#CC0044"
            },
            "Café Expresso": {
                "menu_esquerdo": "#2C221E", "fundo_direito": "#1F1815", "card_livro": "#3A2F2B",
                "texto_secundario": "#BCAAA4", "texto_destaque": "#FFB300",
                "botao_remover": "#D84315", "botao_remover_hover": "#BF360C"
            },
            "Ocean Night": {
                "menu_esquerdo": "#0F172A", "fundo_direito": "#020617", "card_livro": "#1E293B",
                "texto_secundario": "#94A3B8", "texto_destaque": "#38BDF8",
                "botao_remover": "#E11D48", "botao_remover_hover": "#BE123C"
            }
        }

        tema_salvo = "Ocean Night"
        try:
            with open("config_tema.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                tema_salvo = dados.get("tema", "Ocean Night")
        except FileNotFoundError:
            pass

        self.tema_atual = tema_salvo
        self.cores = self.temas.get(self.tema_atual, self.temas["Ocean Night"])

        self.config(bg=self.cores["fundo_direito"])
        self.configure(fg_color=self.cores["fundo_direito"])

        self.db = GerenciadorLivros()
        self.caminho_capa_atual = self.db.capa_padrao

        self.botoes_remover_cards = []
        self.cards_widgets = []

        # ===================================================
        # DECLARAÇÃO DE VARIÁVEIS
        # ===================================================
        self.frame_fundo = None
        self.frame_esquerda = None
        self.frame_direita = None
        self.frame_busca = None
        self.frame_lista = None

        self.entry_nome = None
        self.entry_autor = None
        self.entry_capitulo = None
        self.entry_editar_id = None
        self.entry_remover = None
        self.entry_busca_id = None
        self.entry_busca_autor = None
        self.entry_busca_nome = None

        self.label_capa = None
        self.botao_cadastrar = None
        self.botao_carregar = None
        self.botao_remover_livro = None
        self.menu_temas = None
        # ===================================================

        self.construir_layout()
        self.atualizar_lista()

    def construir_layout(self):
        self.frame_esquerda = ctk.CTkScrollableFrame(self, width=320, corner_radius=20,
                                                     fg_color=self.cores["menu_esquerdo"])
        self.frame_esquerda.pack(side="left", fill="y", padx=15, pady=15)

        self.frame_esquerda._parent_canvas.pack_propagate(False)

        self.frame_direita = ctk.CTkFrame(self, corner_radius=20, fg_color=self.cores["fundo_direito"])
        self.frame_direita.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=15)

        self.construir_menu_esquerdo()
        self.construir_menu_direito()

    def mudar_tema(self, escolha):
        self.tema_atual = escolha
        self.cores = self.temas[escolha]

        with open("config_tema.json", "w", encoding="utf-8") as f:
            json.dump({"tema": escolha}, f)

        self.config(bg=self.cores["fundo_direito"])
        self.configure(fg_color=self.cores["fundo_direito"])

        self.frame_esquerda.configure(fg_color=self.cores["menu_esquerdo"])
        self.frame_direita.configure(fg_color=self.cores["fundo_direito"])

        # ← atualização dos frames filhos
        self.frame_lista.configure(fg_color=self.cores["fundo_direito"])
        self.frame_busca.configure(fg_color=self.cores["fundo_direito"])

        for refs in self.cards_widgets:
            refs["card"].configure(fg_color=self.cores["card_livro"])
            refs["id"].configure(text_color=self.cores["texto_secundario"])
            refs["autor"].configure(text_color=self.cores["texto_secundario"])
            refs["cap"].configure(text_color=self.cores["texto_destaque"])
            refs["btn"].configure(fg_color=self.cores["botao_remover"], hover_color=self.cores["botao_remover_hover"])

    def construir_menu_esquerdo(self):
        ctk.CTkLabel(self.frame_esquerda, text="Cadastrar / Editar Livro", font=("Arial", 20, "bold")).pack(
            pady=(15, 20))

        ctk.CTkLabel(self.frame_esquerda, text="Nome").pack(anchor="w", padx=15)
        self.entry_nome = ctk.CTkEntry(self.frame_esquerda, width=250)
        self.entry_nome.pack(padx=15, pady=(0, 10))

        ctk.CTkLabel(self.frame_esquerda, text="Autor").pack(anchor="w", padx=15)
        self.entry_autor = ctk.CTkEntry(self.frame_esquerda, width=250)
        self.entry_autor.pack(padx=15, pady=(0, 10))

        ctk.CTkLabel(self.frame_esquerda, text="Capítulos").pack(anchor="w", padx=15)
        self.entry_capitulo = ctk.CTkEntry(self.frame_esquerda, width=250)
        self.entry_capitulo.pack(padx=15, pady=(0, 15))

        self.label_capa = ctk.CTkLabel(self.frame_esquerda, text="Sem capa")
        self.label_capa.pack(pady=(5, 10))
        self.mostrar_capa(self.caminho_capa_atual)

        ctk.CTkButton(self.frame_esquerda, text="Escolher Capa", command=self.escolher_capa).pack(padx=15, pady=(0, 15))
        self.botao_cadastrar = ctk.CTkButton(self.frame_esquerda, text="Cadastrar Livro", command=self.acao_cadastrar)
        self.botao_cadastrar.pack(padx=15, pady=5)

        ctk.CTkLabel(self.frame_esquerda, text="ID para editar").pack(anchor="w", padx=15, pady=(20, 0))
        self.entry_editar_id = ctk.CTkEntry(self.frame_esquerda, width=250)
        self.entry_editar_id.pack(padx=15, pady=(0, 10))

        self.botao_carregar = ctk.CTkButton(self.frame_esquerda, text="Carregar Dados",
                                            command=self.preencher_para_editar)
        self.botao_carregar.pack(padx=15, pady=5)

        ctk.CTkButton(self.frame_esquerda, text="Salvar Edição", command=self.acao_editar).pack(padx=15, pady=5)

        ctk.CTkLabel(self.frame_esquerda, text="ID para remover").pack(anchor="w", padx=15, pady=(20, 0))
        self.entry_remover = ctk.CTkEntry(self.frame_esquerda, width=250)
        self.entry_remover.pack(padx=15, pady=(0, 10))

        self.botao_remover_livro = ctk.CTkButton(self.frame_esquerda, text="Remover Livro", fg_color="red",
                                                 hover_color="#8b0000", command=self.acao_remover)
        self.botao_remover_livro.pack(padx=15, pady=5)

        ctk.CTkFrame(self.frame_esquerda, height=2, fg_color="#333333").pack(fill="x", padx=15, pady=(20, 10))
        ctk.CTkLabel(self.frame_esquerda, text="Tema Visual").pack(anchor="w", padx=15)

        self.menu_temas = ctk.CTkOptionMenu(
            self.frame_esquerda,
            values=list(self.temas.keys()),
            command=self.mudar_tema
        )
        self.menu_temas.pack(padx=15, pady=(5, 30))
        self.menu_temas.set(self.tema_atual)

        # Espaçamento para o final
        ctk.CTkLabel(self.frame_esquerda, text="").pack(pady=10)

        # Link do GitHub
        link_github = ctk.CTkLabel(
            self.frame_esquerda,
            text="GitHub",
            font=("Arial", 16, "underline"),
            cursor="hand2",
            text_color=self.cores["texto_secundario"]
        )
        link_github.pack(pady=10)

        import webbrowser
        link_github.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/AngeloTreptow"))

    def construir_menu_direito(self):
        # ← Guardando referência de busca e aplicando a cor fixa em vez de transparent
        self.frame_busca = ctk.CTkFrame(self.frame_direita, fg_color=self.cores["fundo_direito"])
        self.frame_busca.pack(fill="x", padx=10, pady=10)

        self.entry_busca_id = ctk.CTkEntry(self.frame_busca, placeholder_text="Buscar ID", width=100)
        self.entry_busca_id.pack(side="left", padx=5)
        ctk.CTkButton(self.frame_busca, text="Buscar ID", width=90, command=self.acao_buscar_id).pack(side="left",
                                                                                                      padx=5)

        self.entry_busca_autor = ctk.CTkEntry(self.frame_busca, placeholder_text="Buscar Autor", width=140)
        self.entry_busca_autor.pack(side="left", padx=(15, 5))
        ctk.CTkButton(self.frame_busca, text="Buscar Autor", width=100, command=self.acao_buscar_autor).pack(
            side="left", padx=5)

        self.entry_busca_nome = ctk.CTkEntry(self.frame_busca, placeholder_text="Buscar Nome", width=140)
        self.entry_busca_nome.pack(side="left", padx=(15, 5))
        ctk.CTkButton(self.frame_busca, text="Buscar Nome", width=100, command=self.acao_buscar_nome).pack(side="left",
                                                                                                           padx=5)

        ctk.CTkButton(self.frame_busca, text="Mostrar Todos", width=110, command=self.acao_mostrar_todos).pack(
            side="right", padx=5)

        # ← Aplicando a cor fixa na lista em vez de transparent
        self.frame_lista = ctk.CTkScrollableFrame(self.frame_direita, fg_color=self.cores["fundo_direito"])
        self.frame_lista.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # ---------- FUNÇÕES DE AÇÃO ----------

    def atualizar_lista(self, livros=None):
        self.botoes_remover_cards.clear()
        self.cards_widgets.clear()

        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        if livros is None:
            livros = self.db.listar_livros()

        if not livros:
            ctk.CTkLabel(self.frame_lista, text="Nenhum livro encontrado.", font=("Arial", 16)).pack(pady=20)
            return

        for livro in livros:
            self.criar_card_livro(livro)

    def criar_card_livro(self, livro):
        card = ctk.CTkFrame(self.frame_lista, corner_radius=18, fg_color=self.cores["card_livro"])
        card.pack(fill="x", padx=8, pady=8)

        try:
            caminho = livro.get("capa")
            if not caminho or not os.path.exists(caminho):
                caminho = self.db.capa_padrao

            imagem = Image.open(caminho)
            imagem.thumbnail((80, 120))
            capa = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=imagem.size)

            label_img = ctk.CTkLabel(card, image=capa, text="")
            label_img.image = capa
            label_img.pack(side="left", padx=12, pady=12)
        except Exception as e:
            print(f"Erro ao mostrar capa: {e}")
            ctk.CTkLabel(card, text="Sem capa", width=80).pack(side="left", padx=12)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=5, pady=10)

        ctk.CTkLabel(info, text=livro["nome"], font=("Arial", 20, "bold")).pack(anchor="w")

        label_id = ctk.CTkLabel(info, text=f"ID: {livro['id']}", text_color=self.cores["texto_secundario"],
                                font=("Arial", 14))
        label_id.pack(anchor="w", pady=(5, 0))

        label_autor = ctk.CTkLabel(info, text=f"Autor: {livro['autor']}", text_color=self.cores["texto_secundario"],
                                   font=("Arial", 14))
        label_autor.pack(anchor="w", pady=(5, 0))

        label_cap = ctk.CTkLabel(info, text=f"{livro['capitulo']} capítulos", text_color=self.cores["texto_destaque"],
                                 font=("Arial", 14, "bold"))
        label_cap.pack(anchor="w", pady=(5, 10))

        botoes = ctk.CTkFrame(info, fg_color="transparent")
        botoes.pack(anchor="w")

        ctk.CTkButton(botoes, text="Editar", width=90, fg_color="#2563eb",
                      command=lambda i=livro["id"]: self.carregar_edicao(i)).pack(side="left", padx=(0, 10))

        btn_remover = ctk.CTkButton(botoes, text="Remover", width=90, fg_color=self.cores["botao_remover"],
                                    hover_color=self.cores["botao_remover_hover"],
                                    command=lambda i=livro["id"]: self.remover_por_card(i))
        btn_remover.pack(side="left")

        self.botoes_remover_cards.append(btn_remover)

        self.cards_widgets.append({
            "card": card,
            "id": label_id,
            "autor": label_autor,
            "cap": label_cap,
            "btn": btn_remover
        })

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
            messagebox.showwarning("Erro", "Capítulos deve ser um número.")
            return

        self.db.cadastrar_livro(nome, autor, capitulo, self.caminho_capa_atual)
        self.limpar_campos_cadastro()
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")

    def acao_buscar_id(self):
        try:
            id_livro = int(self.entry_busca_id.get().strip())
            livro = self.db.buscar_por_id(id_livro)
            if livro:
                self.atualizar_lista([livro])
            else:
                messagebox.showwarning("Erro", "Livro não encontrado.")
        except ValueError:
            messagebox.showwarning("Erro", "Digite um ID válido.")

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
            messagebox.showwarning("Erro", "Digite o começo do nome do livro.")

    def acao_mostrar_todos(self):
        self.atualizar_lista()

    def preencher_para_editar(self):
        try:
            id_livro = int(self.entry_editar_id.get().strip())
            livro = self.db.buscar_por_id(id_livro)
            if livro:
                self.limpar_campos_cadastro()
                self.entry_nome.insert(0, livro["nome"])
                self.entry_autor.insert(0, livro["autor"])
                self.entry_capitulo.insert(0, str(livro["capitulo"]))

                self.caminho_capa_atual = livro.get("capa", self.db.capa_padrao)
                self.mostrar_capa(self.caminho_capa_atual)

                self.botao_cadastrar.configure(state="disabled")
                self.entry_editar_id.configure(state="disabled")
                self.botao_carregar.configure(state="disabled")
                self.entry_remover.configure(state="disabled")
                self.botao_remover_livro.configure(state="disabled")

                for btn in self.botoes_remover_cards:
                    if btn.winfo_exists():
                        btn.configure(state="disabled")
            else:
                messagebox.showwarning("Erro", "Livro não encontrado.")
        except ValueError:
            messagebox.showwarning("Erro", "Digite um ID válido.")

    def acao_editar(self):
        try:
            id_livro = int(self.entry_editar_id.get().strip())
            capitulo = int(self.entry_capitulo.get())
            nome = self.entry_nome.get().strip()
            autor = self.entry_autor.get().strip()

            if not nome or not autor:
                messagebox.showwarning("Erro", "Preencha nome e autor.")
                return

            if self.db.editar_livro(id_livro, nome, autor, capitulo, self.caminho_capa_atual):
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", "Livro editado com sucesso!")
                self.limpar_campos_cadastro()
                self.entry_editar_id.delete(0, "end")
            else:
                messagebox.showwarning("Erro", "Livro não encontrado.")
        except ValueError:
            messagebox.showwarning("Erro", "ID e capítulos devem ser números.")

    def acao_remover(self):
        try:
            id_livro = int(self.entry_remover.get().strip())
            if self.db.remover_livro(id_livro):
                self.atualizar_lista()
                self.entry_remover.delete(0, "end")
                messagebox.showinfo("Sucesso", "Livro removido com sucesso!")
            else:
                messagebox.showwarning("Erro", "Livro não encontrado.")
        except ValueError:
            messagebox.showwarning("Erro", "Digite um ID válido.")

    def remover_por_card(self, id_livro):
        if messagebox.askyesno("Remover", "Tem certeza que deseja remover este livro?"):
            self.db.remover_livro(id_livro)
            self.atualizar_lista()

    def escolher_capa(self):
        arquivo = filedialog.askopenfilename(title="Escolher capa", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if arquivo:
            self.caminho_capa_atual = arquivo
            self.mostrar_capa(arquivo)

    def mostrar_capa(self, caminho):
        try:
            if not os.path.exists(caminho):
                caminho = self.db.capa_padrao
            imagem_original = Image.open(caminho)
            imagem_original.thumbnail((120, 180))
            imagem = ctk.CTkImage(light_image=imagem_original, dark_image=imagem_original, size=imagem_original.size)
            self.label_capa.configure(image=imagem, text="")
            self.label_capa.image = imagem
        except Exception as e:
            print(f"Erro ao criar card da capa: {e}")
            self.label_capa.configure(text="Erro ao carregar capa", image="")

    def carregar_edicao(self, id_livro):
        self.entry_editar_id.configure(state="normal")
        self.entry_editar_id.delete(0, "end")
        self.entry_editar_id.insert(0, str(id_livro))
        self.preencher_para_editar()

    def limpar_campos_cadastro(self):
        self.entry_nome.delete(0, "end")
        self.entry_autor.delete(0, "end")
        self.entry_capitulo.delete(0, "end")
        self.caminho_capa_atual = self.db.capa_padrao
        self.mostrar_capa(self.caminho_capa_atual)

        self.botao_cadastrar.configure(state="normal")
        self.entry_editar_id.configure(state="normal")
        self.botao_carregar.configure(state="normal")
        self.entry_remover.configure(state="normal")
        self.botao_remover_livro.configure(state="normal")

        for btn in self.botoes_remover_cards:
            if btn.winfo_exists():
                btn.configure(state="normal")


if __name__ == "__main__":
    app = App()
    app.mainloop()
