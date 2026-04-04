import json
import os
import shutil
import sys


class GerenciadorLivros:
    def __init__(self, arquivo_json="livros.json", dir_capas="capas"):
        self.arquivo_json = arquivo_json
        self.dir_capas = dir_capas
        self.lista_livro = []
        self.id_global = 0
        self.capa_padrao = os.path.join(self.dir_capas, "padrao.png")

        os.makedirs(self.dir_capas, exist_ok=True)

        if not os.path.exists(self.capa_padrao):
            try:
                pasta_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
                caminho_interno = os.path.join(pasta_base, "padrao.png")

                if os.path.exists(caminho_interno):
                    shutil.copy(caminho_interno, self.capa_padrao)
            except Exception as e:
                print(f"Aviso interno na extração: {e}")

        self.carregar_livros()

    def cadastrar_livro(self, nome, autor, capitulo, capa=None):
        self.id_global += 1
        capa_final = capa if capa else self.capa_padrao

        if capa_final != self.capa_padrao and os.path.exists(capa_final):
            extensao = os.path.splitext(capa_final)[1]
            novo_caminho = os.path.join(self.dir_capas, f"livro_{self.id_global}{extensao}")
            shutil.copy(capa_final, novo_caminho)
            capa_final = novo_caminho

        livro = {
            "id": self.id_global,
            "nome": nome,
            "autor": autor,
            "capitulo": capitulo,
            "capa": capa_final
        }

        self.lista_livro.append(livro)
        self.salvar_livros()
        return livro

    def listar_livros(self):
        return self.lista_livro

    def buscar_por_id(self, id_livro):
        # Uso de gerador (next) para busca otimizada: para de procurar assim que encontra
        return next((livro for livro in self.lista_livro if livro["id"] == id_livro), None)

    def buscar_por_autor(self, autor):
        # List comprehension com busca flexível (in em vez de igualdade exata)
        return [livro for livro in self.lista_livro if autor.lower() in livro["autor"].lower()]

    def buscar_por_nome(self, nome):
        return [livro for livro in self.lista_livro if nome.lower() in livro["nome"].lower()]

    def editar_livro(self, id_livro, nome, autor, capitulo, nova_capa):
        livro = self.buscar_por_id(id_livro)
        if not livro:
            return False

        livro["nome"] = nome
        livro["autor"] = autor
        livro["capitulo"] = capitulo

        capa_antiga = livro["capa"]

        if nova_capa and nova_capa != capa_antiga:

            if nova_capa == self.capa_padrao:
                livro["capa"] = self.capa_padrao
                if capa_antiga != self.capa_padrao and os.path.exists(capa_antiga):
                    os.remove(capa_antiga)
            else:
                extensao = os.path.splitext(nova_capa)[1]
                novo_caminho = os.path.join(self.dir_capas, f"livro_{id_livro}{extensao}")

                shutil.copy(nova_capa, novo_caminho)
                livro["capa"] = novo_caminho

                if capa_antiga != self.capa_padrao and capa_antiga != novo_caminho and os.path.exists(capa_antiga):
                    os.remove(capa_antiga)

        self.salvar_livros()
        return True

    def remover_livro(self, id_livro):
        livro = self.buscar_por_id(id_livro)
        if not livro:
            return False

        # Se o livro for apagado, apaga tambem a capa (se não for a padrao)
        if livro.get("capa") != self.capa_padrao and os.path.exists(livro["capa"]):
            try:
                os.remove(livro["capa"])
            except OSError:
                pass

        self.lista_livro.remove(livro)
        self.salvar_livros()
        return True

    def salvar_livros(self):
        with open(self.arquivo_json, "w", encoding="utf-8") as arquivo:
            json.dump(self.lista_livro, arquivo, ensure_ascii=False, indent=4)

    def carregar_livros(self):
        try:
            with open(self.arquivo_json, "r", encoding="utf-8") as arquivo:
                self.lista_livro = json.load(arquivo)
            if self.lista_livro:
                self.id_global = max(livro["id"] for livro in self.lista_livro)
            else:
                self.id_global = 0
        except FileNotFoundError:
            self.lista_livro = []
            self.id_global = 0
