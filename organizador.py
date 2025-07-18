from typing import Dict, Tuple
import os
import shutil

class OrganizadorDeArquivos:
    """Encapsula a lógica para organizar arquivos em uma pasta."""
    
    # Atributos da classe com seus tipos definidos
    regras: Dict[str, Tuple[str, ...]]

    def __init__(self, regras: Dict[str, Tuple[str, ...]]) -> None:
        """Inicializa o organizador com um conjunto de regras."""
        self.regras = regras

    def organizar(self, caminho_pasta: str) -> int:
        """Organiza os arquivos na pasta especificada de acordo com as regras."""
        arquivos_movidos: int = 0
        if not caminho_pasta:
            raise ValueError("O caminho da pasta não pode ser vazio.")
            
        arquivo: str
        for arquivo in os.listdir(caminho_pasta):
            # Cria o caminho completo do arquivo
            caminho_completo_arquivo: str = os.path.join(caminho_pasta, arquivo)

            # Verifica se é um arquivo (e não uma pasta)
            if os.path.isfile(caminho_completo_arquivo):
                # Obtém a extensão do arquivo
                extensao: str
                nome_base, extensao = os.path.splitext(arquivo)
                extensao = extensao.lower()

                # Verifica se a extensão está nas regras
                pasta_destino_nome: str | None = None
                pasta: str
                extensoes: Tuple[str, ...]
                # Itera sobre as regras para encontrar a pasta de destino
                for pasta, extensoes in self.regras.items():
                    if extensao in extensoes:
                        pasta_destino_nome = pasta
                        break

                # Se encontrou uma pasta de destino, move o arquivo
                if pasta_destino_nome:
                    nome_subpasta: str = extensao.replace('.', '')
                    caminho_pasta_destino: str = os.path.join(caminho_pasta, pasta_destino_nome, nome_subpasta)
                    os.makedirs(caminho_pasta_destino, exist_ok=True)

                    # Lógica anti-colisão: verifica se o arquivo já existe na pasta de destino
                    caminho_destino_final: str = os.path.join(caminho_pasta_destino, arquivo)

                    # Contador para evitar colisões de nomes
                    contador: int = 1

                    # Loop: enquanto o caminho de destino já existir...
                    while os.path.exists(caminho_destino_final):
                        novo_nome: str = f"{nome_base} ({contador}){extensao}"
                        caminho_destino_final = os.path.join(caminho_pasta_destino, novo_nome)
                        contador += 1

                    # Move o arquivo para o caminho final, que agora é garantido ser único
                    shutil.move(caminho_completo_arquivo, caminho_destino_final)
                    arquivos_movidos += 1
        
        return arquivos_movidos