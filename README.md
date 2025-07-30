# 📂 Organizador de Arquivos Automatizado

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Um aplicativo de desktop para Windows, desenvolvido em Python, que organiza de forma inteligente os arquivos de uma pasta (como a de Downloads) em subpastas categorizadas por tipo e extensão.

Este projeto foi criado como parte de um estudo aprofundado de Programação Orientada a Objetos (OOP), design de software e criação de aplicações robustas com interface gráfica.

---

### 🚀 Como Usar

Existem duas maneiras de utilizar este programa: baixando o executável pronto ou executando a partir do código-fonte.

#### Opção 1: Baixar o Programa Pronto (Recomendado para Usuários)

A forma mais fácil de usar, sem precisar instalar nada.

1.  Navegue até a pasta `dist` neste repositório.
2.  Clique no arquivo `OrganizadorDeArquivos.exe`.
3.  Na página seguinte, clique no botão **"Download"** para baixar o arquivo.
4.  Execute o arquivo baixado no seu computador.

#### Opção 2: Executar a partir do Código-Fonte (Para Desenvolvedores)

Se você é um desenvolvedor e deseja executar ou modificar o código.

**Pré-requisitos:**
* Python 3.x instalado.

**Passos:**
1.  Clone o repositório para a sua máquina local:
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)](https://github.com/Nicholas-UFC/Organizador-de-Pastas.git)
    ```
2.  Navegue até a pasta do projeto:
    ```bash
    cd seu-repositorio
    ```
3.  Execute o script principal:
    ```bash
    python main.py
    ```

---

### ✨ Funcionalidades Principais

* **Interface Gráfica Simples:** Permite que o usuário selecione facilmente a pasta a ser organizada.
* **Organização por Categoria:** Move arquivos para pastas principais com base em seu tipo (Imagens, Documentos, Vídeos, etc.).
* **Criação de Subpastas por Extensão:** Para uma organização ainda mais detalhada, o programa cria subpastas dentro das categorias para cada tipo de arquivo (ex: `.../Imagens/jpg/`, `.../Documentos/pdf/`).
* **Lógica Anti-Colisão:** Se um arquivo com o mesmo nome já existir no destino, a aplicação renomeia o novo arquivo de forma inteligente (ex: `arquivo (1).ext`, `arquivo (2).ext`) para evitar a perda de dados.
* **Feedback ao Usuário:** Exibe mensagens de sucesso, informação ou erro após a conclusão do processo.

---

### 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Interface Gráfica:** Tkinter (biblioteca padrão do Python)
* **Manipulação de Arquivos:** Módulos `os` e `shutil`
* **Princípios:** Programação Orientada a Objetos (OOP), com clara separação entre a lógica de negócio e a interface.

---

### 🏗️ Estrutura do Projeto

O código é modularizado para facilitar a manutenção e a legibilidade:

* **`main.py`**: Ponto de entrada da aplicação. Responsável apenas por instanciar e iniciar a interface gráfica.
* **`interface.py`**: Contém a classe `AppOrganizador`, responsável por toda a construção da janela, widgets e interação com o usuário.
* **`organizador.py`**: Contém a classe `OrganizadorDeArquivos`, que encapsula toda a lógica de negócio (regras, verificação e movimentação de arquivos).
* **`dist/`**: Contém o executável final do programa (`.exe`), pronto para uso em sistemas Windows.

---

### 📄 Licença

Distribuído sob a licença MIT.
