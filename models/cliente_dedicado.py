class ClienteDedicado:
    """
    Modelo que representa um cliente com infraestrutura dedicada.
    """
    def __init__(self, id_cliente, cliente, cnpj_cpf, qnt_de_servs, ad, ambiente, vpn):
        self.id = id_cliente
        self.cliente = cliente
        self.cnpj_cpf = cnpj_cpf
        self.qnt_de_servs = qnt_de_servs
        self.ad = ad
        self.ambiente = ambiente
        self.vpn = vpn