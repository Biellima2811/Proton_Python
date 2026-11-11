import tkinter as tk
from ttkthemes import ThemedTk

from views.login_view import LoginView
from views.main_view import MainView
from models.usuario import Usuario
def iniciar_sistema():
    # 1. Cria a janela principal escondida do Tkinter
    root = ThemedTk(theme='arc')
    
    # =========================================================
    # MODO DE DESENVOLVIMENTO (Ativo: Pula o Login)
    # =========================================================
    usuario_mock = Usuario(id_usuario=1, username="admin_teste", senha="", nivel_acesso="MASTER", status="ATIVO", data_criacao="")
    app = MainView(root, usuario_mock)
    
    # =========================================================
    # MODO DE PRODUÇÃO (Inativo: Comente o bloco acima e descomente a linha abaixo)
    # =========================================================
    # app = LoginView(root)

    # 3. Inicia o "loop" que mantém a janela aberta
    root.mainloop()

if __name__ == "__main__":
    iniciar_sistema()