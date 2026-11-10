import psycopg2
import configparser
import os
from util.logger import LoggerAuditoria

class DatabaseConnection:
    @staticmethod
    def get_connection():
        # Lê o arquivo config_banco e devolve uma conexão aberta ao PostgreSQL
        # 1. Criando um objeto para ler as configurações
        config = configparser.ConfigParser()

        # 2. Definição do caminho do arquivos na raiz do projeto
        caminho_arquivo = 'config_banco.properties'

        if not os.path.exists(caminho_arquivo):
            LoggerAuditoria.erro(f"ERRO: Arquivo {caminho_arquivo} não encontrado!")
            return None

        try:
            """
            Realiza a tentativa de ler o arquivo.
            Adicionar um cabeçalho ficticio ['DEFAULT']
            Porque o configparser exige secçoes
            """
            with open(caminho_arquivo, 'r') as f:
                conifg_string = '[DEFAULT]\n' + f.read()
            config.read_string(conifg_string)

            # 4. Capturando os dados.
            ip_servidor = config['DEFAULT'].get('ip_servidor', 'localhost')
            nome_banco = config['DEFAULT'].get('nome_banco', 'proton')
            usuario_db = config['DEFAULT'].get('usuario_db', 'postgres')
            senha_db_criptografia = config['DEFAULT'].get('senha_db', '')

            #Teste de acesso
            senha_db_real = 'tec@123'

            # 5. Criando um conexão com o banco Postgres o pycopg2
            conexao = psycopg2.connect(
                host=ip_servidor,
                database=nome_banco,
                user=usuario_db,
                password=senha_db_real
            )

            return conexao
        except Exception as e:
            LoggerAuditoria.erro(f'Erro ao conextar à Base de Dados em Servidor {ip_servidor}: {e}')
            return None
