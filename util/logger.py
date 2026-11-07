import os
from datetime import datetime

class LoggerAuditoria:
    @staticmethod
    def registrar(usuario, acao, detalhes):
        """
        Grava uma ação no ficheiro de log local (auditoria_proton.log).
        """
        # Formata a data/hora exata do momento (Ex: 05/11/2026 21:38:00)
        agora = datetime.now()
        data_hora_str = agora.strftime("%d/%m/%Y - %H:%M:%S")

        # Mensagem padrão
        mensagem = f"[{data_hora_str}] Usuario: {usuario} | ACAO: {acao} | DETALHES: {detalhes}\n"

        # Nome do arquivo local
        nome_ficheiro = "auditoria_proton.log"

        try:
            # Abre o ficheiro em modo de "append" ('a'). 
            # Isso significa que vai adicionar texto ao fim, sem apagar o que lá estava.
            with open(nome_ficheiro, 'a', encoding='utf-8') as f:
                f.write(mensagem)
        except Exception as e:
            print(f'Erro ao gravar log local: {e}')