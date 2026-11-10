from util.database import DatabaseConnection
from models.usuario import Usuario
from util.logger import LoggerAuditoria

class UsuarioDAO:
    """
    Classe responsável pelas operações de banco de dados da tabela 'usuarios_sistema'.
    """
    
    def buscar_por_username(self, username):
        """
        Procura um usuário pelo 'username' e devolve um objeto 'Usuario'.
        Retorna None se o usuário não existir.
        """
        # Comando SQL de pesquisa ajustado para 'username'
        sql = "SELECT id, username, senha, nivel_acesso, status, data_criacao FROM usuarios_sistema WHERE username = %s"
        
        # 1. Abre a conexão
        conexao = DatabaseConnection.get_connection()
        if conexao is None:
            LoggerAuditoria.erro(f'Falha ao tentar conexão com banco de Dados...')
            return None
            
        usuario_encontrado = None
        
        try:
            # 2. Cria o cursor (a ferramenta que executa o comando no banco de dados)
            cursor = conexao.cursor()
            
            # 3. Executa o SQL. 
            # Dica: Passamos o username na tupla (username,) em vez de concatenar a string (f"... {username}").
            # Isso bloqueia 100% ataques de 'SQL Injection'.
            cursor.execute(sql, (username,))
            
            # 4. Lê o resultado (fetchone traz a primeira linha encontrada)
            linha = cursor.fetchone()
            
            # 5. Se a linha existir (encontrou usuário), construímos o objeto
            if linha:
                usuario_encontrado = Usuario(
                    id_usuario=linha[0],
                    username=linha[1],
                    senha=linha[2],
                    nivel_acesso=linha[3],
                    status=linha[4],
                    data_criacao=linha[5]
                )
                
            # Fecha o cursor
            cursor.close()
            
        except Exception as e:
            LoggerAuditoria.erro(f"Erro ao procurar usuário: {e}")
        finally:
            # 6. Bloco FINALLY: Roda SEMPRE, mesmo que o código dê erro.
            # É aqui que garantimos que a conexão é fechada para não travar o PostgreSQL.
            if conexao:
                conexao.close()
                
        return usuario_encontrado