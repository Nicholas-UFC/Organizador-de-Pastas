from typing import Dict, List
import os
import shutil
import logging

class OrganizadorDeArquivos:
    """Encapsula a lógica para organizar arquivos em uma pasta."""
    
    # Atributos da classe com seus tipos definidos
    regras: Dict[str, List[str]]

    def __init__(self, regras: Dict[str, List[str]]) -> None:
        """Inicializa o organizador com um conjunto de regras."""
        self.regras = regras

    def organizar(self, caminho_pasta: str) -> int:
        """Organiza os arquivos na pasta especificada de acordo com as regras."""
        arquivos_movidos: int = 0

        # LOG ADICIONADO: Registra o início da operação
        logging.info(f"Iniciando organização da pasta: '{caminho_pasta}'") 

        if not caminho_pasta:
            # LOG ADICIONADO: Registra um erro crítico antes de levantar a exceção
            logging.error("Tentativa de organizar com um caminho de pasta vazio.")
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
                extensoes: List[str]
                # Itera sobre as regras para encontrar a pasta de destino
                for pasta, extensoes in self.regras.items():
                    if extensao in extensoes:
                        pasta_destino_nome = pasta
                        break
                # Se encontrou uma pasta de destino, move o arquivo
                if pasta_destino_nome:
                    nome_subpasta: str = extensao.replace('.', '')
                    caminho_pasta_destino: str = os.path.join(caminho_pasta, pasta_destino_nome, nome_subpasta)
                    # LOG ADICIONADO: Registra a criação de uma nova pasta
                    if not os.path.exists(caminho_pasta_destino):
                        logging.info(f"Criando pasta de destino: '{caminho_pasta_destino}'")
                        os.makedirs(caminho_pasta_destino)

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

                    # LOG ADICIONADO: Registra cada arquivo movido individualmente
                    logging.info(f"Moveu '{arquivo}' para '{caminho_destino_final}'")
                    arquivos_movidos += 1
        
        # LOG ADICIONADO: Registra a conclusão e o total de arquivos
        logging.info(f"Organização concluída. Total de arquivos movidos: {arquivos_movidos}.")
        return arquivos_movidos