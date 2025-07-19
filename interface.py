from typing import Dict, List
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from organizador import OrganizadorDeArquivos
import logging
import json
import os 
import sys 

def resolver_caminho(caminho_relativo):
    """ Obtém o caminho absoluto para um recurso, funciona para dev e para PyInstaller """
    try:
        # PyInstaller cria uma pasta temp e armazena o caminho em _MEIPASS
        # Foi adicionado o " type: ignore ", porque o pylance estava apontando erro, por não achar o _MEIPASS no sys, porque ele só existe quando é usado junto do pyinstaller.
        caminho_base = sys._MEIPASS # type: ignore
    except Exception:
        # _MEIPASS não existe, então estamos no ambiente de desenvolvimento
        caminho_base = os.path.abspath(".")

    return os.path.join(caminho_base, caminho_relativo)

class AppOrganizador(tk.Tk):
    """
    Classe principal da aplicação, que herda de tk.Tk para se tornar a janela principal.
    Ela gerencia todos os elementos visuais e as interações do usuário.
    """

    # Anotações de tipo para os atributos da classe, definindo a "forma" dos dados.
    REGRAS: Dict[str, List[str]]  # Dicionário que armazena as regras de organização
    organizador: OrganizadorDeArquivos  # Instância da classe que contém a lógica de negócio para mover os arquivos.
    pasta_selecionada: tk.StringVar  # Variável especial do Tkinter que armazena o caminho da pasta selecionada pelo usuário.

    def __init__(self) -> None:
        """
        Método construtor, executado uma única vez ao criar a aplicação.
        É responsável por configurar a janela e inicializar os componentes.
        """
        super().__init__()
        
        # Carrega as regras de organização do arquivo externo 'regras.json'.
        # Esta é a primeira etapa para garantir que a aplicação tenha as instruções necessárias para funcionar.
        self.carregar_regras()

        # Configurações básicas da janela principal.
        self.title("Organizador de Arquivos")
        self.geometry("600x300")
        
        # Cria uma instância da nossa classe de lógica, passando as regras que foram carregadas.
        # Este é um exemplo de Composição, um pilar importante da OOP.
        self.organizador = OrganizadorDeArquivos(self.REGRAS)
        
        # Cria uma variável especial do Tkinter que será vinculada ao campo de texto da interface.
        # Qualquer alteração nesta variável reflete na tela, e vice-versa.
        self.pasta_selecionada = tk.StringVar()

        # Chama o método responsável por criar todos os botões, labels, etc.
        self._criar_widgets()

    def carregar_regras(self) -> None:
        """Lê o arquivo de configuração JSON e carrega as regras para a aplicação."""

        caminho_regras = resolver_caminho('regras.json')

        try:
            with open(caminho_regras, 'r', encoding='utf-8') as f:
                self.REGRAS = json.load(f)
            logging.info("Arquivo 'regras.json' carregado com sucesso.")
        except FileNotFoundError:
            # ... resto do método continua igual
            logging.error("ERRO CRÍTICO: O arquivo 'regras.json' não foi encontrado.")
            messagebox.showerror("Erro Crítico", "O arquivo de configuração 'regras.json' não foi encontrado!\nA aplicação não pode continuar.")
            self.destroy()
        except json.JSONDecodeError:
            logging.error("ERRO CRÍTICO: O arquivo 'regras.json' contém um erro de sintaxe.")
            messagebox.showerror("Erro Crítico", "O arquivo 'regras.json' está mal formatado!\nVerifique a sintaxe do JSON.")
            self.destroy()

    def _criar_widgets(self) -> None:
        """
        Método dedicado à criação e posicionamento de todos os elementos visuais (widgets) na janela.
        Isso mantém o construtor (__init__) mais limpo e organizado.
        """
        main_frame: tk.Frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(main_frame, text="Selecione a pasta que deseja organizar:", font=('Arial', 12)).pack(pady=(0, 10))
        
        frame_selecao: tk.Frame = tk.Frame(main_frame)
        frame_selecao.pack(fill=tk.X, expand=True)

        entry_pasta: tk.Entry = tk.Entry(frame_selecao, textvariable=self.pasta_selecionada, font=('Arial', 10), state='readonly', width=50)
        entry_pasta.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        # Salva os botões como atributos da instância (self.btn_...) para que possamos
        # desabilitá-los e reabilitá-los posteriormente em outros métodos.
        self.btn_selecionar: tk.Button = tk.Button(frame_selecao, text="Procurar...", command=self.selecionar_pasta)
        self.btn_selecionar.pack(side=tk.LEFT, padx=(10, 0))

        self.btn_organizar: tk.Button = tk.Button(main_frame, text="Organizar Agora!", font=('Arial', 14, 'bold'), bg="#2a9d8f", fg="white", command=self.iniciar_organizacao, height=2)
        self.btn_organizar.pack(pady=(20, 0), fill=tk.X, expand=True)

        # Cria os widgets de feedback (label e barra de progresso) que serão exibidos
        # durante a operação de organização.
        self.status_label: tk.Label = tk.Label(main_frame, text="", font=('Arial', 10), pady=10)
        self.status_label.pack(fill=tk.X, expand=True)
        
        self.progressbar: ttk.Progressbar = ttk.Progressbar(main_frame, mode='indeterminate')

    def selecionar_pasta(self) -> None:
        """
        Chamado pelo botão "Procurar...". Abre uma janela de diálogo padrão do sistema
        operacional para que o usuário possa escolher uma pasta de forma segura e intuitiva.
        """
        caminho_pasta: str = filedialog.askdirectory(title="Selecione uma pasta")
        if caminho_pasta: # Apenas atualiza o caminho se o usuário selecionou uma pasta (não clicou em 'Cancelar')
            self.pasta_selecionada.set(caminho_pasta)
            logging.info(f"Pasta selecionada pelo usuário: '{caminho_pasta}'")

    def iniciar_organizacao(self) -> None:
        """
        Este método é o "disparador" da ação principal. Ele não faz o trabalho pesado,
        mas prepara a interface para a tarefa e inicia uma nova thread para executar a organização.
        Isso evita que a interface do usuário congele.
        """
        pasta: str = self.pasta_selecionada.get()
        logging.info("Botão 'Organizar Agora!' clicado.")
        
        if not pasta:
            logging.warning("Tentativa de organização sem selecionar uma pasta.")
            messagebox.showwarning("Aviso", "Por favor, selecione uma pasta primeiro.")
            return
        
        # Bloqueia a interface para prevenir ações múltiplas e informa o usuário que o trabalho começou.
        self.btn_organizar.config(state="disabled", text="Organizando...")
        self.btn_selecionar.config(state="disabled")
        self.status_label.config(text="Iniciando verificação dos arquivos...")
        self.progressbar.pack(fill=tk.X, expand=True, pady=(5,0))
        self.progressbar.start(10)

        # Cria a thread que executará a tarefa demorada (organizar arquivos) em segundo plano.
        thread = threading.Thread(target=self._thread_organizar, args=(pasta,))
        thread.start()

    def _thread_organizar(self, pasta: str) -> None:
        """
        Este método é executado na thread de segundo plano para não travar a interface.
        Ele chama a lógica de negócio (o organizador) e captura o resultado (sucesso ou erro).
        """
        resultado = None
        try:
            resultado = self.organizador.organizar(pasta)
        except Exception as e:
            resultado = e
        
        # Ponto CRÍTICO: Comunicação segura entre threads.
        # Agenda a execução do método '_organizacao_concluida' de volta na thread principal da interface,
        # passando o resultado da operação. Isso é necessário porque widgets do Tkinter
        # só podem ser modificados com segurança a partir da sua thread principal.
        self.after(0, self._organizacao_concluida, resultado)

    def _organizacao_concluida(self, resultado) -> None:
        """
        Executado de volta na thread principal após a conclusão da organização.
        Este método é responsável por "limpar" a interface e mostrar o resultado final ao usuário.
        """
        # Restaura a interface ao seu estado normal.
        self.progressbar.stop()
        self.progressbar.pack_forget()
        self.btn_organizar.config(state="normal", text="Organizar Agora!")
        self.btn_selecionar.config(state="normal")
        
        # Analisa o resultado recebido da thread e exibe a mensagem apropriada.
        if isinstance(resultado, Exception):
            logging.error(f"Ocorreu uma exceção não tratada durante a organização.", exc_info=resultado)
            self.status_label.config(text="Ocorreu um erro!")
            messagebox.showerror("Erro", f"Ocorreu um erro durante a organização:\n{resultado}")
        else:
            movidos = resultado
            self.status_label.config(text=f"Organização concluída! {movidos} arquivo(s) movido(s).")
            if movidos > 0:
                messagebox.showinfo("Sucesso", f"{movidos} arquivo(s) foram organizados com sucesso!")
            else:
                messagebox.showinfo("Informação", "Nenhum arquivo para organizar foi encontrado.")