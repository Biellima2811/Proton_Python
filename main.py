import tkinter as tk
from ttkthemes import ThemedTk
from views.login_view import LoginView
def iniciar_sistema():
    # 1. Cria a janela principal escondida do Tkinter
    root = ThemedTk(theme='arc')

    # 2. Chama a nossa View de Login
    app_login = LoginView(root)

    # 3. Inicia o "loop" que mantém a janela aberta
    root.mainloop()

if __name__ == "__main__":
    iniciar_sistema()