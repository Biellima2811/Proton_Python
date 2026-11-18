from util.database import DatabaseConnection
from util.logger import LoggerAuditoria
from models.cliente_dedicado import ClienteDedicado

class ClienteDedicadoDAO:
    def listar_todos(self):
        sql = "SELECT id, cliente, cnpj_cpf, qnt_de_servs, ad, ambiente, vpn FROM clientes_dedicados ORDER BY id"
        clientes = []
        conexao = DatabaseConnection.get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql)
                linhas = cursor.fetchall()
                for linha in linhas:
                    clientes.append(ClienteDedicado(
                        id_cliente=linha[0], cliente=linha[1], cnpj_cpf=linha[2],
                        qnt_de_servs=linha[3], ad=linha[4], ambiente=linha[5], vpn=linha[6]
                    ))
                cursor.close()
            except Exception as e:
                LoggerAuditoria.erro(f'Erro ao listar clientes dedicados: {e}')
            finally:
                conexao.close()
        return clientes
        
    def buscar_por_termo(self, termo):
        sql = """
            SELECT id, cliente, cnpj_cpf, qnt_de_servs, ad, ambiente, vpn 
            FROM clientes_dedicados 
            WHERE cliente ILIKE %s OR cnpj_cpf ILIKE %s 
            ORDER BY id
        """
        clientes = []
        conexao = DatabaseConnection.get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                like_termo = f"%{termo}%"
                cursor.execute(sql, (like_termo, like_termo))
                linhas = cursor.fetchall()
                for linha in linhas:
                    clientes.append(ClienteDedicado(
                        id_cliente=linha[0], cliente=linha[1], cnpj_cpf=linha[2],
                        qnt_de_servs=linha[3], ad=linha[4], ambiente=linha[5], vpn=linha[6]
                    ))
                cursor.close()
            except Exception as e:
                LoggerAuditoria.erro(f'Erro na busca de clientes dedicados: {e}')
            finally:
                conexao.close()
        return clientes
        
    def salvar_com_servidores(self, cliente, lista_servidores):
        conexao = DatabaseConnection.get_connection()
        if not conexao:
            raise Exception("Falha ao conectar com o banco de dados.")
        try:
            conexao.autocommit = False
            cursor = conexao.cursor()
            id_cliente = getattr(cliente, 'id', 0)
            
            if id_cliente == 0:
                sql_cliente = """
                    INSERT INTO clientes_dedicados (cliente, cnpj_cpf, qnt_de_servs, ad, ambiente, vpn, sgbd, criado_por) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                """
                cursor.execute(sql_cliente, (
                    cliente.cliente, cliente.cnpj_cpf, cliente.qnt_de_servs, 
                    cliente.ad, cliente.ambiente, cliente.vpn, getattr(cliente, 'sgbd', ''), 'Sistema'
                ))
                id_cliente = cursor.fetchone()[0]
            else:
                sql_cliente = """
                    UPDATE clientes_dedicados SET cliente=%s, cnpj_cpf=%s, qnt_de_servs=%s, ad=%s, ambiente=%s, vpn=%s, sgbd=%s WHERE id=%s
                """
                cursor.execute(sql_cliente, (
                    cliente.cliente, cliente.cnpj_cpf, cliente.qnt_de_servs, 
                    cliente.ad, cliente.ambiente, cliente.vpn, getattr(cliente, 'sgbd', ''), id_cliente
                ))
                cursor.execute("DELETE FROM servidores_clientes_dedicados WHERE cliente_id = %s", (id_cliente,))
                cursor.execute("DELETE FROM bancos_dedicados WHERE id_cliente = %s", (id_cliente,))

            if lista_servidores:
                sql_servidor = """
                    INSERT INTO servidores_clientes_dedicados (cliente_id, tipo_servidor, hostname, ip_privado, ip_publico, porta, usuario, senha) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                dados_servidores = [(id_cliente, serv.tipo, serv.hostname, serv.ip_privado, serv.ip_publico, getattr(serv, 'porta', ''), serv.usuario, serv.senha) for serv in lista_servidores]
                cursor.executemany(sql_servidor, dados_servidores)

            if hasattr(cliente, 'sgbd') and cliente.sgbd:
                sql_banco = """
                    INSERT INTO bancos_dedicados (id_cliente, sgbd, hqbird, versao, usuario_banco, senha_banco) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_banco, (id_cliente, cliente.sgbd, getattr(cliente, 'sgbd_hqbird', 'Não'), getattr(cliente, 'sgbd_versao', ''), getattr(cliente, 'sgbd_user', ''), getattr(cliente, 'sgbd_senha', '')))

            conexao.commit()
            cursor.close()
        except Exception as e:
            conexao.rollback()
            LoggerAuditoria.erro(f'Erro na transação de salvar cliente dedicado: {e}')
            raise Exception(f"Falha ao gravar no banco. Detalhe: {e}")
        finally:
            if conexao:
                conexao.autocommit = True
                conexao.close()

    def deletar(self, id_cliente):
        conexao = DatabaseConnection.get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM clientes_dedicados WHERE id = %s", (id_cliente,))
                conexao.commit()
                cursor.close()
            except Exception as e:
                conexao.rollback()
                LoggerAuditoria.erro(f'Erro ao deletar cliente: {e}')
                raise e
            finally:
                conexao.close()

    def buscar_por_id(self, id_cliente):
        conexao = DatabaseConnection.get_connection()
        cliente_dados = None
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """
                    SELECT c.id, c.cliente, c.cnpj_cpf, c.qnt_de_servs, c.ad, c.ambiente, c.vpn, c.sgbd,
                           b.versao, b.usuario_banco, b.senha_banco, b.hqbird
                    FROM clientes_dedicados c
                    LEFT JOIN bancos_dedicados b ON c.id = b.id_cliente
                    WHERE c.id = %s
                """
                cursor.execute(sql, (id_cliente,))
                linha = cursor.fetchone()
                if linha:
                    cliente_dados = {
                        'id': linha[0], 'nome': linha[1], 'cnpj_cpf': linha[2], 'qnt_servs': linha[3],
                        'ad': linha[4], 'ambiente': linha[5], 'vpn': linha[6], 
                        'sgbd': linha[7] if linha[7] else "", 'versao': linha[8] if linha[8] else "",
                        'usuario_banco': linha[9] if linha[9] else "", 'senha_banco': linha[10] if linha[10] else "",
                        'hqbird': linha[11] if linha[11] else "Não"
                    }
                cursor.close()
            except Exception as e:
                LoggerAuditoria.erro(f'Erro ao buscar por ID: {e}')
            finally:
                conexao.close()
        return cliente_dados

    def buscar_servidores(self, id_cliente):
        conexao = DatabaseConnection.get_connection()
        servidores = []
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("SELECT tipo_servidor, hostname, ip_privado, ip_publico, porta, usuario, senha FROM servidores_clientes_dedicados WHERE cliente_id = %s", (id_cliente,))
                linhas = cursor.fetchall()
                for l in linhas:
                    servidores.append({'tipo': l[0], 'hostname': l[1], 'ip_privado': l[2], 'ip_publico': l[3], 'porta': l[4], 'usuario': l[5], 'senha': l[6]})
                cursor.close()
            except Exception as e:
                LoggerAuditoria.erro(f'Erro ao buscar servidores: {e}')
            finally:
                conexao.close()
        return servidores