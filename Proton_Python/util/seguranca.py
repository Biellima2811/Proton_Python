import bcrypt
class Seguranca:
    @staticmethod
    def hash_senha(senha_pura):
        """
        Recebe uma senha em texto (ex: '123456') 
        e cria um hash seguro usando bcrypt.
        """

        # bcrypt exige que as strings sejam convertidas para bytes.
        senha_bytes = senha_pura.encode('utf-8')

        # Gera o 'salt' (um valor aletorio) e faz o hash
        hash_bytes = bcrypt.hashpw(senha_bytes, bcrypt.gensalt(12))

        # Converte de volta para String normal para gravar na base de dados
        return hash_bytes.decode('utf-8')

    @staticmethod
    def verificar_senha(senha_pura, hash_salvo):
        """
        Verifica se a senha digitada pelo utilizador 
        bate certo com o hash salvo no banco.
        """
        try:
            # Convertendo ambos para bytes
            senha_bytes = senha_pura.encode('utf-8')
            hash_bytes = hash_salvo.encode('utf-8')

            # Checkpw faz a comparação
            return bcrypt.checkpw(senha_bytes, hash_bytes)
        except Exception as e:
            print(f'Erro ao verificar senha: {e}')
            return False
        