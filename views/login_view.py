import tkinter as tk
from tkinter import messagebox
import os

# Importamos as nossas regras de negócio e utilitários
from dao.usuario_dao import UsuarioDAO
from util.seguranca import Seguranca
from util.logger import LoggerAuditoria

class LoginView:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Proton - Autenticação")
        self.root.geometry("400x400")
        self.root.configure(bg="#f8f9fa") # Fundo cinza claro
        
        self.centralizar_janela()

        self.var_username = tk.StringVar()
        self.var_senha = tk.StringVar()
        self.var_lembrar = tk.BooleanVar()

        self.construir_interface()

    def centralizar_janela(self):
        self.root.update_idletasks()
        largura = 700
        altura = 500
        x = (self.root.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.root.winfo_screenheight() // 2) - (altura // 2)
        self.root.geometry(f'{largura}x{altura}+{x}+{y}')

    def construir_interface(self):
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # O Frame principal que vai conter tudo (simulando a caixa central com sombra)
        box_principal = tk.Frame(self.root, bg='#ffffff', bd=0)

        # Padding no grid do root para criar espaço à volta
        box_principal.grid(row=0, column=0, sticky='nsew', padx=15, pady=35)

        # O box_principal será dividido em 2 colunas: 
        # Coluna 0 (Esquerda - 40% do espaço) e Coluna 1 (Direita - 60% do espaço)
        box_principal.rowconfigure(0, weight=1)
        box_principal.columnconfigure(0, weight=4)
        box_principal.columnconfigure(1, weight=6)

        # =================================================================
        # LADO ESQUERDO (Logotipo e Títulos) - Usando Grid
        # =================================================================
        box_esquerda = tk.Frame(box_principal, background='#f8f9fa')
        box_esquerda.grid(row=0, column=0, sticky='nsew')

        # COnfigurar as linhas do lado esquerdo para empurrar o rodapé para baixo
        box_esquerda.columnconfigure(0, weight=1)
        box_esquerda.rowconfigure(0, weight=1) # Espaço em cima
        box_esquerda.rowconfigure(1, weight=0) # Logo
        box_esquerda.rowconfigure(2, weight=0) # Título
        box_esquerda.rowconfigure(3, weight=0) # Subtítulo
        box_esquerda.rowconfigure(4, weight=1) # Espaço no meio
        box_esquerda.rowconfigure(5, weight=0) # Rodapé

        # Logotipo
        caminho_imagem = os.path.join('images', 'icone.png')
        if os.path.exists(caminho_imagem):
            self.img_logo = tk.PhotoImage(file=caminho_imagem)
            self.img_logo = self.img_logo.subsample(2,2)
            lbl_img = tk.Label(box_esquerda, image=self.img_logo, bg='#f8f9fa')
            lbl_img.grid(row=1, column=0, pady=(0, 10))
        else:
            lbl_img = tk.Label(box_esquerda, text="[ LOGO ]", font='Helvetica 30', bg="#f8f9fa", fg='#adb5bd')
            lbl_img.grid(row=1, column=0, pady=(0, 10))

        tk.Label(box_esquerda, text="PROTON", font=("Helvetica", 32, "bold"), bg="#f8f9fa", fg="#2b3035").grid(row=2, column=0, pady=(10, 0))
        tk.Label(box_esquerda, text="ERP & Cloud Management", font=("Helvetica", 14), bg="#f8f9fa", fg="#6c757d").grid(row=3, column=0)

        # Rodapé Esquerdo
        tk.Label(box_esquerda, text="© 2026 - Desenvolvido por Gabriel Levi\nTodos os direitos reservados.", 
                 font=("Helvetica", 9), bg="#f8f9fa", fg="#adb5bd").grid(row=5, column=0, pady=20)


        # =================================================================
        # LADO DIREITO (Formulário) - Usando Grid
        # =================================================================
        box_direita = tk.Frame(box_principal, bg='#ffffff')
        box_direita.grid(row=0, column=1, sticky='nsew', padx=40)

        # Configurar as linhas para centrar o formulário verticalmente
        box_direita.columnconfigure(0, weight=1)
        box_direita.rowconfigure(0, weight=1) # Espaçador topo
        box_direita.rowconfigure(1, weight=0) # Título
        box_direita.rowconfigure(2, weight=0) # Label Usuário
        box_direita.rowconfigure(3, weight=0) # Entry Usuário
        box_direita.rowconfigure(4, weight=0) # Label Senha
        box_direita.rowconfigure(5, weight=0) # Entry Senha
        box_direita.rowconfigure(6, weight=0) # Frame de Opções (Lembrar/Esqueci)
        box_direita.rowconfigure(7, weight=0) # Botão Entrar
        box_direita.rowconfigure(8, weight=0) # Botão Sair
        box_direita.rowconfigure(9, weight=1) # Espaçador meio
        box_direita.rowconfigure(10, weight=0) # Rodapé Banco

        tk.Label(box_direita, text='Autenticação Corporativa', font='Helvetica 20 bold', bg='#ffffff', fg='#495057').grid(row=1, column=0, pady= (0,30))

        # Campo Usuario
        tk.Label(box_direita, text='Usuário:', font='Helvetica 10 bold', bg='#ffffff', fg='#495057').grid(row=2, column=0, sticky='w')
        ent_user = tk.Entry(box_direita, textvariable=self.var_username, font='Helvetica 12', bg='#f8f9fa', relief='solid', bd=1)
        ent_user.grid(row=3, column=0, sticky='ew', pady=(2,15), ipady=8)

        # Campo senha
        tk.Label(box_direita, text='Senha de Acesso:', font='Helvetica 10 bold', bg="#ffffff", fg="#495057").grid(row=4, column=0, sticky='w')
        ent_senha = tk.Entry(box_direita, textvariable=self.var_senha, font='Helvetica 12', bg="#f8f9fa", relief="solid", bd=1, show="*")
        ent_senha.grid(row=5, column=0, sticky='ew', pady=(2,5), ipady=8)


        # Opções (Lembrar / Esqueci) - Criamos um sub-frame apenas para organizar as duas colunas internas
        box_opcoes = tk.Frame(box_direita, bg='#ffffff')
        box_opcoes.grid(row=6, column=0, sticky='ew', pady=(0,20))
        box_opcoes.columnconfigure(0,weight=1)
        box_opcoes.rowconfigure(1, weight=1)

        chk_lembrar = tk.Checkbutton(box_opcoes, text='Lembrar meu usuario', variable=self.var_lembrar, bg="#ffffff", fg="#495057", activebackground="#ffffff")
        chk_lembrar.grid(row=0, column=0, sticky='w')

        lbl_esqueci = tk.Label(box_opcoes, text='Esqueci a senha', font=("Helvetica", 9, "underline"), bg="#ffffff", fg="#0d6efd", cursor="hand2")
        lbl_esqueci.grid(row=0, column=1, sticky='e')
        lbl_esqueci.bind('<Button-1>', lambda e: messagebox.showinfo('Aviso', 'Essa funcionalidade está em fase de desenvolvimento'))

        # Botão acessar
        btn_entrar = tk.Button(box_direita, text='Acessa Sistema', bg="#0d6efd", fg="white", font=("Helvetica", 13, "bold"), relief="flat", cursor="hand2", command=self.efetuar_login)
        btn_entrar.grid(row=7, column=0, sticky='ew', pady=(10,10), ipady=6)

        # botão sair
        btn_sair = tk.Button(box_direita, text='Sair / Fechar', bg="#ffffff", fg="#6c757d", font=("Helvetica", 12, "bold"), relief="solid", bd=1, cursor="hand2", command=self.root.destroy)
        btn_sair.grid(row=8, column=0, sticky='ew', ipady=5)

        # Rodapé Direito (Configurar Banco)
        lbl_config = tk.Label(box_direita, text="⚙ Configurar Acesso ao Banco de Dados", font=("Helvetica", 10), bg="#ffffff", fg="#6c757d", cursor="hand2")
        lbl_config.grid(row=10, column=0, pady=20)
        lbl_config.bind("<Button-1>", lambda e: messagebox.showinfo("Configuração", "Abre o FormConfiguracoes!"))

        # Permite dar Enter para logar
        self.root.bind('<Return>', lambda event: self.efetuar_login())


    def efetuar_login(self):
        username_digitado = self.var_username.get().strip()
        senha_digitada = self.var_senha.get().strip()

        if not username_digitado or not senha_digitada:
            messagebox.showwarning("Atenção", "Preencha o usuário e a senha!")
            return

        dao = UsuarioDAO()
        usuario = dao.buscar_por_username(username_digitado)

        if usuario:
            if Seguranca.verificar_senha(senha_digitada, usuario.senha):
                LoggerAuditoria.registrar(usuario.username, "LOGIN", "Usuário acessou o sistema com sucesso.")
                messagebox.showinfo("Sucesso", f"Bem-vindo(a), {usuario.username}!")
                # 1. Limpando todos os elementos do Login da tela
                for widget in self.root.winfo_children():
                    widget.destroy()
                from views.main_view import MainView
                MainView(self.root, usuario)
            else:
                messagebox.showerror("Acesso Negado", "Usuário ou senha incorretos.")
                LoggerAuditoria.registrar(username_digitado, "LOGIN_FALHO", "Tentativa de acesso com senha inválida.")
        else:
            messagebox.showerror("Acesso Negado", "Usuário ou senha incorretos.")
            LoggerAuditoria.registrar(username_digitado, "LOGIN_FALHO", "Usuário inexistente.")