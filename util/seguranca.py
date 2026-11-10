import bcrypt
from util.logger import LoggerAuditoria

class Seguranca:
    @staticmethod
    def hash_senha(senha_pura):
        """
        Recebe uma senha em texto (ex: '123456') 
        e cria um hash seguro usando bcrypt.
        """
        senha_bytes = senha_pura.encode('utf-8')
        hash_bytes = bcrypt.hashpw(senha_bytes, bcrypt.gensalt(12))
        return hash_bytes.decode('utf-8')

    @staticmethod
    def verificar_senha(senha_pura, hash_salvo):
        """
        Verifica se a senha digitada pelo utilizador 
        bate certo com o hash (ou texto puro) salvo no banco.
        """
        try:
            # Se a senha no banco não começar com '$', significa que é uma senha antiga em texto puro
            if not hash_salvo.startswith('$'):
                return senha_pura == hash_salvo

            # Se começar com '$', é um hash do bcrypt, então fazemos a verificação criptografada
            senha_bytes = senha_pura.encode('utf-8')
            hash_bytes = hash_salvo.encode('utf-8')
            return bcrypt.checkpw(senha_bytes, hash_bytes)
            
        except Exception as e:
            LoggerAuditoria.erro(f'Erro ao verificar senha: {e}')
            return False