<div align="center">

# 📚 My Book List

### *Sua biblioteca pessoal. Bonita, rápida e offline.*

> Um gerenciador de livros e mangás feito em Python que leva a sério a experiência visual — porque organizar sua leitura deveria ser tão prazeroso quanto ler.

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blue?style=for-the-badge)
![Pillow](https://img.shields.io/badge/Pillow-PIL-orange?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/status-estável-brightgreen?style=for-the-badge)

[📥 Baixar .exe](#-como-executar) · [🎨 Ver Temas](#-temas-e-personalização)

</div>

---

## 📸 Demonstração do App

<div align="center">
  <img src="https://github.com/user-attachments/assets/d7d6162e-022d-4089-a960-0be49169c4c1" alt="Demonstração do MyBookList" width="900" style="border-radius: 10px;"/>
</div>

---

## 🎨 Temas e Personalização

O MyBookList não tem um tema: ele tem **quatro personalidades**. Cada uma foi projetada para um momento diferente de leitura — do terminal escuro às madrugadas aconchegantes.

<div align="center">

<table border="0">
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/bf0e63ba-acd9-48dd-9122-0ceda2018abf" width="460px"/><br/>
      <b>🧛 Dracula</b><br/>
      <small>O clássico de alto contraste para programadores que também leem.</small>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/320002d1-90a8-4a66-88b1-692ceb812850" width="460px"/><br/>
      <b>⚡ Cyberpunk</b><br/>
      <small>Neon roxo e rosa para uma estética que veio do futuro.</small>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/ca3e94a2-7470-4860-86d5-40a526c2db55" width="460px"/><br/>
      <b>☕ Café-Expresso</b><br/>
      <small>Tons terrosos para sessões longas e sem pressa.</small>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/e1457a32-c27f-4ab3-b6d2-f45b2b518117" width="460px"/><br/>
      <b>🌊 Ocean-Night</b><br/>
      <small>Azul profundo e relaxante para uso noturno.</small>
    </td>
  </tr>
</table>

</div>

> *As imagens utilizadas nas capturas de tela são apenas para fins demonstrativos e pertencem aos seus respectivos detentores de direitos autorais.*

---

## 🧠 Por que este projeto existe?

Apps de gerenciamento de leitura costumam ser uma de duas coisas: ou são simples demais (uma planilha glorificada) ou são complexos demais (cheios de redes sociais e gamificação que distraem).

O **MyBookList** foi construído para um uso específico: **você, sua estante e nada mais**. Sem conta. Sem internet. Sem anúncios. Só você e sua lista — no seu computador, com a cara que você escolher.

A obsessão do projeto é a **experiência visual**: a interface precisa ser um lugar agradável de visitar, não apenas funcional. É por isso que os temas não são apenas trocas de cor — cada um tem paleta, contraste e atmosfera próprios.

---

## ✨ O que o app resolve

> Não é uma lista de features. É o que o produto **resolve** na prática.

| Solução | Como funciona |
|---|---|
| 📝 **Cadastro de livros e mangás** | Nome, autor, número de capítulos e capa personalizada em poucos cliques |
| 🔍 **Busca rápida** | Filtro por ID, nome ou autor com um clique — sem precisar rolar a lista |
| ✏️ **Edição e exclusão completas** | Gestão total do acervo sem fricção |
| 💾 **Dados que persistem** | Salvamento automático em `livros.json` — sem banco de dados, sem configuração |
| 🎨 **Quatro temas visuais** | Troca de tema com um clique, sem reiniciar o app |
| 🖼️ **Gerenciamento inteligente de capas** | Redimensionamento automático e imagem padrão quando a capa não está disponível |
| 📦 **Portabilidade total** | Roda como `.exe` único — copia a pasta e funciona em qualquer Windows |

---

## 🏗️ Decisões de Engenharia

> Por que essas tecnologias? Não foi acaso — foi escolha consciente.

### CustomTkinter — Interface moderna sem abrir mão do Python puro

O Tkinter padrão tem cara de 2003. O CustomTkinter resolve isso com widgets redesenhados, suporte nativo a temas dark/light e uma API familiar para quem já conhece Tkinter — sem exigir frameworks pesados como Electron ou Qt. Para um app desktop leve e portátil, é a escolha mais equilibrada entre **qualidade visual e simplicidade de distribuição**.

### JSON como banco de dados — Simples por design

O modelo de dados do MyBookList é direto: cada livro é um objeto independente, sem relacionamentos complexos. O JSON resolve isso de forma natural, sem configuração, sem servidor e sem dependências externas. O arquivo `livros.json` é legível, editável manualmente e fácil de fazer backup — o usuário tem controle total dos seus dados.

### Pillow (PIL) — Processamento de imagens no cliente

O gerenciamento de capas exige redimensionamento, normalização de formato e geração de imagens padrão. O Pillow faz tudo isso de forma confiável e leve, sem chamar APIs externas. As imagens ficam locais, carregam rápido e funcionam offline.

### PyInstaller — Um arquivo, zero instalação

O PyInstaller empacota Python, dependências e assets em um único executável. O usuário não precisa instalar Python, criar ambientes virtuais ou rodar comandos. **Baixa, extrai, executa.** Essa decisão prioriza acessibilidade sobre elegância técnica — e é a escolha certa para o público-alvo.

### Estrutura do projeto

```
MyBookList/
├── main.py                        # Ponto de entrada da aplicação
├── requirements.txt               # Dependências do projeto
├── livros.json                    # Banco de dados local (gerado na 1ª execução)
├── config_tema.json               # Preferência de tema (gerada na 1ª execução)
├── capas/
│   ├── padrao.png                 # Capa padrão para livros sem imagem
│   └── ...                        # Capas escolhidas pelo usuário
└── mybooklist/                    # Pacote da aplicação
    ├── app.py                     # Janela principal e handlers de eventos
    ├── caminhos.py                # Resolução dos caminhos de dados
    ├── ui/
    │   ├── card_livro.py          # Card visual de cada livro na listagem
    │   └── imagens.py             # Carregamento e redimensionamento de imagens
    ├── core/
    │   └── gerenciador_livros.py  # Lógica de negócio: CRUD e persistência
    └── config/
        ├── temas.py               # Paletas dos quatro temas visuais
        └── config_tema.py         # Persistência da preferência de tema
```

Os dados do usuário (`livros.json`, `config_tema.json` e a pasta `capas/`) são criados ao lado do programa na primeira execução, independente de onde ele for iniciado.

### Estrutura de dados (`livros.json`)

```json
[
  {
    "id": 1,
    "nome": "Nome do Livro",
    "autor": "Nome do Autor",
    "capitulo": 312,
    "capa": "capas/livro_1.jpg"
  }
]
```

---

## 🚀 Como Executar

### Opção 1: Executável — Para usuários

> Sem instalar nada. Funciona no Windows direto.

1. Acesse a aba [**Releases**](https://github.com/AngeloTreptow/MyBookList/releases/latest)
2. Baixe o arquivo `MyBookList.zip`
3. Extraia em qualquer pasta e execute o `.exe`

O app cria automaticamente sua própria estrutura de pastas na primeira execução.

---

### Opção 2: Código fonte — Para desenvolvedores

```bash
# 1. Clone o repositório
git clone https://github.com/AngeloTreptow/MyBookList.git
cd MyBookList

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute
python main.py
```

**Requisitos:** Python 3.10+

> 💡 **Linux:** o `tkinter` faz parte da biblioteca padrão do Python, mas em algumas distribuições precisa ser instalado à parte: `sudo apt install python3-tk` (Debian/Ubuntu).

---

### Opção 3: Gerar o executável você mesmo

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --add-data "capas/padrao.png;capas" main.py
```

O `.exe` será gerado na pasta `dist/`.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|---|---|---|
| Python | 3.10+ | Linguagem base |
| CustomTkinter | ~6.0 | Interface gráfica moderna |
| Pillow (PIL) | ~12.3 | Processamento de imagens e capas |
| JSON | nativo | Persistência de dados local |
| PyInstaller | latest | Compilação para executável único |

---

## 📄 Licença

Distribuído sob a licença MIT. Veja [`LICENSE`](LICENSE) para mais informações.

---

<div align="center">

*Feito com Python e a crença de que até um app de lista de livros merece ser bonito.*

</div>