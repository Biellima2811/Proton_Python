from util.database import DatabaseConnection
from util.logger import LoggerAuditoria
from models.cliente_dedicado import ClienteDedicado

class ClienteDedicadoDAO:
    def listar_todos(self):
        """
        Busca todos os clientes dedicados ordenados pelo ID.
        """
        sql = "SELECT id, cliente, cnpj_cpf, qnt_de_servs, ad, ambiente, vpn FROM clientes_dedicados ORDER BY id"
        clientes = []

        conexao = DatabaseConnection.get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql)
                linhas = cursor.fetchall()

                for linha in linhas:
                    # Converte cada linha em objeto ClienteDedicado
                    clientes.append(ClienteDedicado(
                        id_cliente=linha[0],
                        cliente=linha[1],
                        cnpj_cpf=linha[2],
                        qnt_de_servs=linha[3],
                        ad=linha[4],
                        ambiente=linha[5],
                        vpn=linha[6],
                    ))
                cursor.close()
            except Exception as e:
                LoggerAuditoria.erro(f'Erro ao listar clientes dedicados: {e}')
            finally:
                conexao.close()
        return clientes