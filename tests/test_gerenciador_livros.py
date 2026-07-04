"""Testes do GerenciadorLivros: CRUD, buscas, capas e persistência."""

import json
import os

import pytest

from mybooklist.core.gerenciador_livros import GerenciadorLivros


@pytest.fixture
def caminhos(tmp_path):
    """Caminhos isolados em diretório temporário, para não tocar os dados reais."""
    return {
        "arquivo_dados": str(tmp_path / "livros.json"),
        "dir_capas": str(tmp_path / "capas"),
    }


@pytest.fixture
def gerenciador(caminhos):
    return GerenciadorLivros(**caminhos)


@pytest.fixture
def capa_origem(tmp_path):
    """Arquivo de imagem fictício para simular uma capa escolhida pelo usuário."""
    caminho = tmp_path / "minha_capa.png"
    caminho.write_bytes(b"conteudo png falso")
    return str(caminho)


class TestCadastrar:

    def test_retorna_livro_com_todos_os_campos(self, gerenciador):
        livro = gerenciador.cadastrar_livro("Dom Casmurro", "Machado de Assis", 148)

        assert livro["id"] == 1
        assert livro["nome"] == "Dom Casmurro"
        assert livro["autor"] == "Machado de Assis"
        assert livro["capitulo"] == 148
        assert livro["capa"] == gerenciador.capa_padrao

    def test_ids_sao_incrementais(self, gerenciador):
        primeiro = gerenciador.cadastrar_livro("Livro A", "Autor A", 1)
        segundo = gerenciador.cadastrar_livro("Livro B", "Autor B", 2)

        assert (primeiro["id"], segundo["id"]) == (1, 2)

    @pytest.mark.parametrize("titulo, autor", [("", "Autor"), ("Título", ""), ("", "")])
    def test_titulo_ou_autor_vazio_levanta_erro(self, gerenciador, titulo, autor):
        with pytest.raises(ValueError):
            gerenciador.cadastrar_livro(titulo, autor, 10)

    def test_persiste_no_arquivo_json(self, gerenciador, caminhos):
        gerenciador.cadastrar_livro("Livro", "Autor", 5)

        with open(caminhos["arquivo_dados"], encoding="utf-8") as f:
            dados = json.load(f)

        assert len(dados) == 1
        assert dados[0]["nome"] == "Livro"

    def test_capa_personalizada_e_copiada_para_dir_capas(self, gerenciador, capa_origem):
        livro = gerenciador.cadastrar_livro("Livro", "Autor", 5, capa=capa_origem)

        esperado = os.path.join(gerenciador.dir_capas, "livro_1.png")
        assert livro["capa"] == esperado
        assert os.path.exists(esperado)

    def test_capa_inexistente_usa_capa_padrao(self, gerenciador):
        livro = gerenciador.cadastrar_livro("Livro", "Autor", 5, capa="nao/existe.png")

        assert livro["capa"] == gerenciador.capa_padrao


class TestBuscar:

    @pytest.fixture(autouse=True)
    def acervo(self, gerenciador):
        gerenciador.cadastrar_livro("Dom Casmurro", "Machado de Assis", 148)
        gerenciador.cadastrar_livro("Memórias Póstumas", "Machado de Assis", 160)
        gerenciador.cadastrar_livro("Vidas Secas", "Graciliano Ramos", 13)

    def test_buscar_por_id(self, gerenciador):
        livro = gerenciador.buscar_por_id(2)

        assert livro is not None
        assert livro["nome"] == "Memórias Póstumas"

    def test_buscar_por_id_inexistente_retorna_none(self, gerenciador):
        assert gerenciador.buscar_por_id(99) is None

    def test_buscar_por_autor_e_parcial_e_ignora_caixa(self, gerenciador):
        resultado = gerenciador.buscar_por_autor("machado")

        assert len(resultado) == 2

    def test_buscar_por_nome_e_parcial_e_ignora_caixa(self, gerenciador):
        resultado = gerenciador.buscar_por_nome("SECAS")

        assert len(resultado) == 1
        assert resultado[0]["nome"] == "Vidas Secas"

    def test_busca_sem_correspondencia_retorna_lista_vazia(self, gerenciador):
        assert gerenciador.buscar_por_autor("Tolkien") == []
        assert gerenciador.buscar_por_nome("Hobbit") == []


class TestListar:

    def test_retorna_copia_da_lista_interna(self, gerenciador):
        gerenciador.cadastrar_livro("Livro", "Autor", 5)

        lista = gerenciador.listar_livros()
        lista.clear()

        assert len(gerenciador.listar_livros()) == 1


class TestEditar:

    def test_atualiza_os_campos(self, gerenciador):
        gerenciador.cadastrar_livro("Nome Velho", "Autor Velho", 1)

        assert gerenciador.editar_livro(1, "Nome Novo", "Autor Novo", 42) is True

        livro = gerenciador.buscar_por_id(1)
        assert livro["nome"] == "Nome Novo"
        assert livro["autor"] == "Autor Novo"
        assert livro["capitulo"] == 42

    def test_id_inexistente_retorna_false(self, gerenciador):
        assert gerenciador.editar_livro(99, "Nome", "Autor", 1) is False

    def test_sem_nova_capa_mantem_a_atual(self, gerenciador, capa_origem):
        gerenciador.cadastrar_livro("Livro", "Autor", 5, capa=capa_origem)
        capa_anterior = gerenciador.buscar_por_id(1)["capa"]

        gerenciador.editar_livro(1, "Livro", "Autor", 6)

        assert gerenciador.buscar_por_id(1)["capa"] == capa_anterior
        assert os.path.exists(capa_anterior)

    def test_trocar_capa_por_extensao_diferente_remove_a_antiga(self, gerenciador, capa_origem, tmp_path):
        gerenciador.cadastrar_livro("Livro", "Autor", 5, capa=capa_origem)
        capa_antiga = gerenciador.buscar_por_id(1)["capa"]

        nova_origem = tmp_path / "outra_capa.jpg"
        nova_origem.write_bytes(b"conteudo jpg falso")
        gerenciador.editar_livro(1, "Livro", "Autor", 5, nova_capa=str(nova_origem))

        capa_nova = gerenciador.buscar_por_id(1)["capa"]
        assert capa_nova.endswith("livro_1.jpg")
        assert os.path.exists(capa_nova)
        assert not os.path.exists(capa_antiga)

    def test_trocar_capa_de_mesma_extensao_nao_apaga_o_arquivo_novo(self, gerenciador, capa_origem, tmp_path):
        # Regressão: a nova capa é copiada sobre o mesmo caminho da antiga
        # (livro_1.png); o arquivo não pode ser removido em seguida.
        gerenciador.cadastrar_livro("Livro", "Autor", 5, capa=capa_origem)

        nova_origem = tmp_path / "outra_capa.png"
        nova_origem.write_bytes(b"novo conteudo png")
        gerenciador.editar_livro(1, "Livro", "Autor", 5, nova_capa=str(nova_origem))

        capa = gerenciador.buscar_por_id(1)["capa"]
        assert os.path.exists(capa)
        with open(capa, "rb") as f:
            assert f.read() == b"novo conteudo png"


class TestRemover:

    def test_remove_o_livro(self, gerenciador):
        gerenciador.cadastrar_livro("Livro", "Autor", 5)

        assert gerenciador.remover_livro(1) is True
        assert gerenciador.buscar_por_id(1) is None

    def test_id_inexistente_retorna_false(self, gerenciador):
        assert gerenciador.remover_livro(99) is False

    def test_remove_a_capa_personalizada_do_disco(self, gerenciador, capa_origem):
        gerenciador.cadastrar_livro("Livro", "Autor", 5, capa=capa_origem)
        capa = gerenciador.buscar_por_id(1)["capa"]

        gerenciador.remover_livro(1)

        assert not os.path.exists(capa)

    def test_nao_remove_a_capa_padrao(self, gerenciador):
        gerenciador.cadastrar_livro("Livro", "Autor", 5)

        gerenciador.remover_livro(1)

        assert os.path.exists(gerenciador.capa_padrao)


class TestPersistencia:

    def test_nova_instancia_recarrega_os_dados_do_disco(self, gerenciador, caminhos):
        gerenciador.cadastrar_livro("Livro", "Autor", 5)

        recarregado = GerenciadorLivros(**caminhos)

        assert len(recarregado.listar_livros()) == 1
        assert recarregado.buscar_por_id(1)["nome"] == "Livro"

    def test_proximo_id_continua_apos_recarga(self, gerenciador, caminhos):
        gerenciador.cadastrar_livro("Livro A", "Autor", 1)
        gerenciador.cadastrar_livro("Livro B", "Autor", 2)
        gerenciador.remover_livro(1)

        recarregado = GerenciadorLivros(**caminhos)
        novo = recarregado.cadastrar_livro("Livro C", "Autor", 3)

        assert novo["id"] == 3

    def test_arquivo_inexistente_inicia_acervo_vazio(self, caminhos):
        gerenciador = GerenciadorLivros(**caminhos)

        assert gerenciador.listar_livros() == []
