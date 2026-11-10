class Usuario:
    """
    Modelo que representa um usuário do sistema Proton.
    Mapeia exatamente as colunas da tabela 'usuarios_sistema'.
    """
    def __init__(self, id_usuario, username, senha, nivel_acesso, status, data_criacao):
        self.id = id_usuario
        self.username = username
        self.senha = senha
        self.nivel_acesso = nivel_acesso
        self.status = status
        self.data_criacao = data_criacao
        