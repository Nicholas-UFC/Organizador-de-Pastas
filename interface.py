from typing import Dict, Tuple
import tkinter as tk
from tkinter import filedialog, messagebox
from organizador import OrganizadorDeArquivos

class AppOrganizador(tk.Tk):
    """Cria a interface gráfica para o usuário interagir com o organizador."""

    # Atributos de classe com tipos definidos
    REGRAS: Dict[str, Tuple[str, ...]] = {
        "Imagens": ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'),
        "Documentos": ('.pdf', '.docx', '.doc', '.txt', '.xlsx', '.xls', '.pptx', '.ppt',  '.epub', '.odt'),
        "Vídeos": ('.mp4', '.mov', '.avi', '.mkv'),
        "Músicas": ('.mp3', '.wav', '.aac'),
        "Compactados": ('.zip', '.rar', '.7z'),
        "Executáveis": ('.exe', '.msi'),
        "Programas": ('.py', '.ipynb', '.java', '.c', '.cpp', '.js', '.html', '.css'),
        "Tabelas": ('.csv', '.tsv', '.json', '.xlsm'),
        "Projetos": ('.dwg', '.bak', '.psd', '.ai', '.indd', '.sketch'),
        "Apresentações": ('.pptx', '.ppt', '.ppsx', '.potx'),
    }
    organizador: OrganizadorDeArquivos
    pasta_selecionada: tk.StringVar

    def __init__(self) -> None:
        super().__init__()
        # Configurações da janela principal
        self.title("Organizador de Arquivos")
        self.geometry("600x250")
        
        # Instancia a classe de lógica. O tipo do atributo 'self.organizador'
        # é a nossa própria classe 'OrganizadorDeArquivos'.
        self.organizador = OrganizadorDeArquivos(self.REGRAS)
        
        # tk.StringVar é um tipo especial do Tkinter para variáveis de interface.
        self.pasta_selecionada = tk.StringVar()

        # Cria os widgets da interface
        self._criar_widgets()

    def _criar_widgets(self) -> None:
        """Cria e posiciona todos os widgets da interface."""
        main_frame: tk.Frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(main_frame, text="Selecione a pasta que deseja organizar:", font=('Arial', 12)).pack(pady=(0, 10))
        
        # Frame para a entrada de texto e botão de seleção
        frame_selecao: tk.Frame = tk.Frame(main_frame)
        frame_selecao.pack(fill=tk.X, expand=True)

        # Entrada de texto para o caminho da pasta
        entry_pasta: tk.Entry = tk.Entry(frame_selecao, textvariable=self.pasta_selecionada, font=('Arial', 10), state='readonly', width=50)
        entry_pasta.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        # Botão para abrir o diálogo de seleção de pasta
        btn_selecionar: tk.Button = tk.Button(frame_selecao, text="Procurar...", command=self.selecionar_pasta)
        btn_selecionar.pack(side=tk.LEFT, padx=(10, 0))

        # Botão para iniciar a organização
        btn_organizar: tk.Button = tk.Button(main_frame, text="Organizar Agora!", font=('Arial', 14, 'bold'), bg="#2a9d8f", fg="white", command=self.iniciar_organizacao, height=2)
        btn_organizar.pack(pady=(20, 0), fill=tk.X, expand=True)

    # Método para selecionar a pasta através de um diálogo
    def selecionar_pasta(self) -> None:
        """Abre uma caixa de diálogo para o usuário escolher uma pasta."""
        caminho_pasta: str = filedialog.askdirectory(title="Selecione uma pasta")
        if caminho_pasta:
            self.pasta_selecionada.set(caminho_pasta)

    # Método para iniciar a organização dos arquivos
    def iniciar_organizacao(self) -> None:
        """Chama a lógica de organização e exibe o resultado."""
        pasta: str = self.pasta_selecionada.get()
        if not pasta:
            messagebox.showwarning("Aviso", "Por favor, selecione uma pasta primeiro.")
            return

        try:
            movidos: int = self.organizador.organizar(pasta)
            if movidos > 0:
                messagebox.showinfo("Sucesso", f"{movidos} arquivo(s) foram organizados com sucesso!")
            else:
                messagebox.showinfo("Informação", "Nenhum arquivo para organizar foi encontrado.")
        except Exception as e:
            # A variável 'e' na exceção é do tipo Exception
            messagebox.showerror("Erro", f"Ocorreu um erro durante a organização:\n{e}")