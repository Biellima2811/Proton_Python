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
    
    def salvar_com_servidores(self, cliente, lista_servidores):
        """
        Salva o cliente (Aba 1) e a sua lista de servidores (Aba 2) usando uma transação.
        """
        conexao = DatabaseConnection.get_connection()
        if not conexao:
            raise Exception("Falha ao conectar com o banco de dados.")

        try:
            # 1. Inicia a transação
            conexao.autocommit = False
            cursor = conexao.cursor()

            id_cliente = getattr(cliente, 'id', 0)

            if id_cliente == 0:
                # INSERÇÃO (NOVO CLIENTE) - inclui 'sgbd'
                sql_cliente = """
                    INSERT INTO clientes_dedicados 
                    (cliente, cnpj_cpf, qnt_de_servs, ad, ambiente, vpn, sgbd, criado_por) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                """
                criado_por = 'Sistema'
                
                cursor.execute(sql_cliente, (
                    cliente.cliente, cliente.cnpj_cpf, cliente.qnt_de_servs, 
                    cliente.ad, cliente.ambiente, cliente.vpn, 
                    getattr(cliente, 'sgbd', ''), criado_por
                ))
                id_cliente = cursor.fetchone()[0]
                
            else:
                # ATUALIZAÇÃO (EDIÇÃO)
                sql_cliente = """
                    UPDATE clientes_dedicados 
                    SET cliente=%s, cnpj_cpf=%s, qnt_de_servs=%s, ad=%s, ambiente=%s, vpn=%s, sgbd=%s 
                    WHERE id=%s
                """
                cursor.execute(sql_cliente, (
                    cliente.cliente, cliente.cnpj_cpf, cliente.qnt_de_servs, 
                    cliente.ad, cliente.ambiente, cliente.vpn, 
                    getattr(cliente, 'sgbd', ''), id_cliente
                ))
                
                # Apagamos os servidores antigos antes de inserir a lista nova
                cursor.execute("DELETE FROM servidores_clientes_dedicados WHERE cliente_id = %s", (id_cliente,))

            # 2. Gravar a lista de servidores (Aba 2) - Agora com TODOS os campos
            if lista_servidores:
                sql_servidor = """
                    INSERT INTO servidores_clientes_dedicados 
                    (cliente_id, tipo_servidor, hostname, ip_privado, ip_publico, porta, usuario, senha) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                dados_servidores = [
                    (id_cliente, serv.tipo, serv.hostname, serv.ip_privado, serv.ip_publico, getattr(serv, 'porta', ''), serv.usuario, serv.senha) 
                    for serv in lista_servidores
                ]
                cursor.executemany(sql_servidor, dados_servidores)

            # 3. Confirma a gravação (Commit)
            conexao.commit()
            cursor.close()

        except Exception as e:
            conexao.rollback()
            from util.logger import LoggerAuditoria
            LoggerAuditoria.erro(f'Erro na transação de salvar cliente dedicado: {e}')
            raise Exception(f"Falha ao gravar no banco. Detalhe: {e}")
        
        finally:
            if conexao:
                conexao.autocommit = True
                conexao.close()