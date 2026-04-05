# 📚 My Book List - Python GUI

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

Um gerenciador de biblioteca pessoal moderno e portátil desenvolvido em **Python**.  
O diferencial deste projeto é a interface gráfica dinâmica com sistema de **temas customizados** e a capacidade de rodar como um arquivo único (.exe).

---

## 📸 Interface do Aplicativo
<h2 align="center">🎨 Temas Disponíveis</h2>

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/bf0e63ba-acd9-48dd-9122-0ceda2018abf" width="350px"/><br/>
      <b>Tema Dracula</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/320002d1-90a8-4a66-88b1-692ceb812850" width="350px"/><br/>
      <b>Tema Cyberpunk</b>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/ca3e94a2-7470-4860-86d5-40a526c2db55" width="350px"/><br/>
      <b>Tema Cafe-Expresso</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/e1457a32-c27f-4ab3-b6d2-f45b2b518117" width="350px"/><br/>
      <b>Tema Ocean-Night</b>
    </td>
  </tr>
</table>

> *As imagens utilizadas nas capturas de tela são apenas para fins demonstrativos e pertencem aos seus respectivos detentores de direitos autorais.*

---

## 🎨 Temas e Personalização
O projeto utiliza a biblioteca **CustomTkinter** com uma lógica de temas customizados para garantir conforto visual em qualquer ambiente:
* 🧛 **Dracula:** O clássico de alto contraste para programadores.
* ⚡ **Cyberpunk:** Tons neon (roxo e rosa) para uma estética futurista.
* ☕ **Café-Expresso:** Tons terrosos e aconchegantes para leituras prolongadas.
* 🌊 **Ocean-Night:** Um azul profundo e relaxante para uso noturno.
* 🖼️ **Capas Automáticas:** Sistema inteligente que gerencia o redimensionamento de capas e imagens padrão.

---

## 📂 Funcionalidades
* 📝 **Cadastro de Livros/Mangás:** Nome, Autor, Capítulos e Capa.
* 🔍 **Busca Inteligente:** Filtro por ID, Nome ou Autor em tempo real.
* ✏️ **Edição e Exclusão:** Gestão completa do acervo.
* 💾 **Persistência de Dados:** Salva tudo automaticamente em `livros.json`.
* 📦 **Portabilidade:** Funciona como um executável único que gera sua própria estrutura de pastas.

---

## 🛠️ Tecnologias Utilizadas
* **Python 3.10+**
* **CustomTkinter** (Interface Moderna)
* **Pillow (PIL)** (Processamento de Imagens)
* **JSON** (Banco de Dados NoSQL leve)
* **PyInstaller** (Compilação para .exe)

---

## 🚀 Como Executar
### Opção 1: Executável (Para Usuários)
1. Vá na aba [Releases](https://github.com/AngeloTreptow/MyBookList/releases/latest) deste repositório.
2. Baixe o arquivo `MyBookList.zip`.
3. Extraia e execute o `.exe`.

### Opção 2: Código Fonte (Para Desenvolvedores)
1. Clone o repositório.
2. Instale as dependências: `pip install customtkinter pillow`.
3. Execute: `python main.py`.
