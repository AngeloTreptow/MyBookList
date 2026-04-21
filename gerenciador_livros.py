import json
import os
import shutil
import sys

NOME_CAPA_PADRAO = "padrao.png"
NOME_ARQUIVO_DADOS = "livros.json"


class GerenciadorLivros:

    def __init__(
            self,
            arquivo_dados: str = NOME_ARQUIVO_DADOS,
            dir_capas: str = "capas",
    ):
        self.arquivo_dados = arquivo_dados
        self.dir_capas = dir_capas
        self.capa_padrao = os.path.join(self.dir_capas, NOME_CAPA_PADRAO)

        self.livros: list[dict] = []
        self._proximo_id: int = 0

        self._garantir_dir_capas()
        self._carregar()

    # Interface pública
    def cadastrar_livro(self, titulo: str, autor: str, capitulo: int, capa: str = None) -> dict:
        if not titulo or not autor:
            raise ValueError("Título e autor são obrigatórios.")

        self._proximo_id += 1
        caminho_capa = self._resolver_capa(capa, self._proximo_id)

        livro = {
            "id": self._proximo_id,
            "nome": titulo,
            "autor": autor,
            "capitulo": capitulo,
            "capa": caminho_capa,
        }

        self.livros.append(livro)
        self._salvar()
        return livro

    def listar_livros(self) -> list[dict]:
        return self.livros

    def buscar_por_id(self, id_livro: int) -> dict | None:
        return next((livro for livro in self.livros if livro["id"] == id_livro), None)

    def buscar_por_autor(self, autor: str) -> list[dict]:
        return [livro for livro in self.livros if autor.lower() in livro["autor"].lower()]

    def buscar_por_nome(self, nome: str) -> list[dict]:
        return [livro for livro in self.livros if nome.lower() in livro["nome"].lower()]

    def editar_livro(
            self,
            id_livro: int,
            titulo: str,
            autor: str,
            capitulo: int,
            nova_capa: str = None,
    ) -> bool:
        livro = self.buscar_por_id(id_livro)
        if not livro:
            return False

        livro["nome"] = titulo
        livro["autor"] = autor
        livro["capitulo"] = capitulo

        if nova_capa and nova_capa != livro["capa"]:
            capa_antiga = livro["capa"]
            livro["capa"] = self._resolver_capa(nova_capa, id_livro)
            self._remover_capa_personalizada(capa_antiga)

        self._salvar()
        return True

    def remover_livro(self, id_livro: int) -> bool:
        livro = self.buscar_por_id(id_livro)
        if not livro:
            return False

        self._remover_capa_personalizada(livro.get("capa"))
        self.livros.remove(livro)
        self._salvar()
        return True

    # Métodos privados

    def _garantir_dir_capas(self) -> None:
        os.makedirs(self.dir_capas, exist_ok=True)

        if not os.path.exists(self.capa_padrao):
            self._extrair_capa_padrao()

    def _extrair_capa_padrao(self) -> None:
        origem = self._encontrar_capa_padrao_original()
        if not origem:
            print("Aviso: capa padrão não encontrada.")
            return
        try:
            shutil.copy(origem, self.capa_padrao)
        except Exception as erro:
            print(f"Aviso: não foi possível copiar a capa padrão – {erro}")

    def _encontrar_capa_padrao_original(self) -> str | None:
        dir_script = os.path.dirname(os.path.abspath(__file__))

        candidatos = []

        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            candidatos.append(os.path.join(meipass, "capas", NOME_CAPA_PADRAO))

        candidatos += [
            os.path.join(dir_script, "capas", NOME_CAPA_PADRAO),
            os.path.join(dir_script, NOME_CAPA_PADRAO),
        ]

        return next((c for c in candidatos if os.path.exists(c)), None)

    def _resolver_capa(self, caminho_capa: str | None, id_livro: int) -> str:
        if not caminho_capa or caminho_capa == self.capa_padrao:
            return self.capa_padrao

        if not os.path.exists(caminho_capa):
            return self.capa_padrao

        return self._copiar_capa(caminho_capa, id_livro)

    def _copiar_capa(self, origem: str, id_livro: int) -> str:
        extensao = os.path.splitext(origem)[1]
        destino = os.path.join(self.dir_capas, f"livro_{id_livro}{extensao}")
        shutil.copy(origem, destino)
        return destino

    def _remover_capa_personalizada(self, caminho_capa: str | None) -> None:
        if caminho_capa and caminho_capa != self.capa_padrao and os.path.exists(caminho_capa):
            try:
                os.remove(caminho_capa)
            except OSError:
                pass

    def _salvar(self) -> None:
        """Persiste a lista de livros no disco."""
        with open(self.arquivo_dados, "w", encoding="utf-8") as arquivo:
            json.dump(self.livros, arquivo, ensure_ascii=False, indent=4)

    def _carregar(self) -> None:
        """Carrega a lista de livros do disco, ou inicia vazia se o arquivo não existir."""
        try:
            with open(self.arquivo_dados, "r", encoding="utf-8") as arquivo:
                self.livros = json.load(arquivo)
            self._proximo_id = max((livro["id"] for livro in self.livros), default=0)
        except FileNotFoundError:
            self.livros = []
            self._proximo_id = 0
