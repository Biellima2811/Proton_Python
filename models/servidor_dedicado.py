class ServidorDedicado:
    """
    Representa um servidor vinculado a um Cliente Dedicado.
    """
    def __init__(self, tipo, hostname, ip_privado, ip_publico, usuario, senha):
        self.tipo = tipo
        self.hostname = hostname
        self.ip_privado = ip_privado
        self.ip_publico = ip_publico
        self.usuario = usuario
        self.senha = senha