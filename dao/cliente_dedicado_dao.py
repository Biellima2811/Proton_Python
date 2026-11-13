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
        Salva o cliente e a sua lista de servidores usando uma transação.
        Se cliente.id == 0, é um novo registro. Senão, é uma edição.
        """
        conexao = DatabaseConnection.get_connection()
        if not conexao:
            raise Exception("Falha ao conectar com o banco de dados.")

        try:
            # 1. Inicia a transação (se der erro, cancela tudo)
            conexao.autocommit = False
            cursor = conexao.cursor()

            id_cliente = cliente.id

            if id_cliente == 0:
                # INSERÇÃO (NOVO CLIENTE)
                # Usamos RETURNING id para o banco nos devolver qual o ID que acabou de ser gerado
                sql_cliente = """
                    INSERT INTO clientes_dedicados (cliente, cnpj_cpf, qnt_de_servs, ad, ambiente, vpn, criado_por) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
                """
                # No futuro, podemos pegar o usuário logado via variável global. Por agora, 'Sistema'.
                criado_por = 'Sistema'
                
                cursor.execute(sql_cliente, (
                    cliente.cliente, cliente.cnpj_cpf, cliente.qnt_de_servs, 
                    cliente.ad, cliente.ambiente, cliente.vpn, criado_por
                ))
                id_cliente = cursor.fetchone()[0] # Pega o ID devolvido
                
            else:
                # ATUALIZAÇÃO (EDIÇÃO DE CLIENTE EXISTENTE)
                sql_cliente = """
                    UPDATE clientes_dedicados 
                    SET cliente=%s, cnpj_cpf=%s, qnt_de_servs=%s, ad=%s, ambiente=%s, vpn=%s 
                    WHERE id=%s
                """
                cursor.execute(sql_cliente, (
                    cliente.cliente, cliente.cnpj_cpf, cliente.qnt_de_servs, 
                    cliente.ad, cliente.ambiente, cliente.vpn, id_cliente
                ))
                
                # Para garantir que os servidores não fiquem duplicados na edição,
                # apagamos os antigos e gravamos os novos (como estava no JavaFX)
                cursor.execute("DELETE FROM servidores_clientes_dedicados WHERE cliente_id = %s", (id_cliente,))

            # 2. Gravar a lista de servidores vinculados a este cliente
            if lista_servidores:
                sql_servidor = """
                    INSERT INTO servidores_clientes_dedicados (cliente_id, tipo_servidor, ip_servidor, usuario, senha) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                # Usamos executemany para inserir vários de uma vez (mais rápido)
                dados_servidores = [
                    (id_cliente, serv.tipo, serv.ip, serv.usuario, serv.senha) 
                    for serv in lista_servidores
                ]
                cursor.executemany(sql_servidor, dados_servidores)

            # 3. Confirma a gravação (Commit)
            conexao.commit()
            cursor.close()

        except Exception as e:
            # Se deu qualquer erro no cliente ou no servidor, cancela a gravação
            conexao.rollback()
            LoggerAuditoria.erro(f'Erro na transação de salvar cliente dedicado: {e}')
            raise Exception("Falha ao gravar no banco. Transação revertida.")
        
        finally:
            # Restaura a conexão para o modo normal e fecha
            conexao.autocommit = True
            conexao.close()