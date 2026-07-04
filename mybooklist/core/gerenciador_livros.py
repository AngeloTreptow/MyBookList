import json
import os
import shutil
import sys

from mybooklist.caminhos import dir_base

NOME_CAPA_PADRAO = "padrao.png"
NOME_ARQUIVO_DADOS = "livros.json"
NOME_DIR_CAPAS = "capas"


class GerenciadorLivros:

    def __init__(
            self,
            arquivo_dados: str | None = None,
            dir_capas: str | None = None,
    ):
        # Caminhos padrão ancorados no diretório base da aplicação, para que
        # os dados não mudem conforme o diretório de onde o programa é iniciado.
        self.arquivo_dados = arquivo_dados or os.path.join(dir_base(), NOME_ARQUIVO_DADOS)
        self.dir_capas = dir_capas or os.path.join(dir_base(), NOME_DIR_CAPAS)
        self.capa_padrao = os.path.join(self.dir_capas, NOME_CAPA_PADRAO)

        self.livros: list[dict] = []
        self._proximo_id: int = 0

        self._garantir_dir_capas()
        self._carregar()

    # Interface pública
    def cadastrar_livro(self, titulo: str, autor: str, capitulo: int, capa: str | None = None) -> dict:
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
        # Cópia da lista para que quem chama não altere o estado interno
        # sem passar pelos métodos que persistem em disco.
        return list(self.livros)

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
            nova_capa: str | None = None,
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
            # A nova capa pode ter sido copiada sobre o mesmo caminho da antiga
            # (mesma extensão); nesse caso não há arquivo antigo a remover.
            if capa_antiga != livro["capa"]:
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
        dir_raiz = dir_base()

        candidatos = []

        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            candidatos.append(os.path.join(meipass, NOME_DIR_CAPAS, NOME_CAPA_PADRAO))

        candidatos += [
            os.path.join(dir_raiz, NOME_DIR_CAPAS, NOME_CAPA_PADRAO),
            os.path.join(dir_raiz, NOME_CAPA_PADRAO),
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
        """Persiste a lista de livros no disco.

        Em caso de falha de escrita (disco cheio, sem permissão), avisa e
        segue: os dados permanecem em memória e a próxima operação tenta
        salvar novamente.
        """
        try:
            with open(self.arquivo_dados, "w", encoding="utf-8") as arquivo:
                json.dump(self.livros, arquivo, ensure_ascii=False, indent=4)
        except OSError as erro:
            print(f"Aviso: não foi possível salvar os livros – {erro}")

    def _carregar(self) -> None:
        """Carrega a lista de livros do disco, ou inicia vazia se o arquivo não existir."""
        try:
            with open(self.arquivo_dados, encoding="utf-8") as arquivo:
                self.livros = json.load(arquivo)
            self._proximo_id = max((livro["id"] for livro in self.livros), default=0)
        except FileNotFoundError:
            self.livros = []
            self._proximo_id = 0
