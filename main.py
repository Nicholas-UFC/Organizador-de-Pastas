from interface import AppOrganizador
import logging

# Configuração do módulo de logging para registrar eventos da aplicação
logging.basicConfig(
    level=logging.INFO, # Define o nível mínimo de severidade para registrar (INFO, WARNING, ERROR, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s', # Define o formato de cada linha de log
    filename='registro.log', # Nome do arquivo onde os logs serão salvos
    encoding='utf-8', # Garante que caracteres especiais sejam salvos corretamente
    filemode='w' # 'w' para sobrescrever o log a cada execução, 'a' para adicionar no final
)

if __name__ == "__main__":
    logging.info("Aplicação iniciada.")
    app: AppOrganizador = AppOrganizador()
    app.mainloop()
    logging.info("Aplicação encerrada.")