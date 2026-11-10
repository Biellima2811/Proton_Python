import tkinter as tk
from tkinter import ttk, messagebox


class MainView:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario

        # Configuração da Janela principal
        self.root.title('Proton - Gestão de Infraestrutura')
        self.root.geometry('1200x700')
        self.root.configure(bg='#f4f6f9')

        try:
            self.root.state('zoomed')
        except:
            pass

        # Configurar Estilos Globais do ttk (já que o ARC gerencia as cores de forma centralizada)
        self.estilos = ttk.Style()

        # Estilo para os botões do menu lateral (Fundo Escuro)
        self.estilos.configure("Menu.TButton", font=("Helvetica", 11, "bold"), padding=10)

        # Estilo para os títulos da área central
        self.estilos.configure("Titulo.TLabel", font=("Helvetica", 22, "bold"), background="#f4f6f9", foreground="#212529")

        self.construir_interface()

    def construir_interface(self):
        # =================================================================
        # GRID DA JANELA PRINCIPAL
        # =================================================================
        # A janela terá 2 linhas:
        # Linha 0 -> Cabeçalho Superior (Header)
        # Linha 1 -> Corpo (Menu Lateral + Área Central)
        self.root.rowconfigure(0, weight=0) # Cabeçalho não vai esticar na vertical
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        # =================================================================
        # 1. CABEÇALHO (Top Bar)
        # =================================================================
        frame_topo = tk.Frame(self.root, bg='#1e2229', height=40)
        frame_topo.grid(row=0, column=0, sticky='nsew')

        # Configura grid do cabeçalho
        frame_topo.columnconfigure(0, weight=1) # Espaço vazio à esquerda
        frame_topo.columnconfigure(1, weight=0) # Info do usuario
        frame_topo.columnconfigure(2, weight=0) # Botão de sair
        frame_topo.rowconfigure(0, weight=1)

        lbl_sessao = tk.Label(frame_topo, text=f'🟢 Sessão Ativa: {self.usuario.username}', 
                              bg="#1e2229", fg="white", 
                              font=("Helvetica", 10, "bold"))
        lbl_sessao.grid(row=0, column=1, padx=20)

        btn_sair = tk.Button(frame_topo, text="Sair / Logoff", bg="#dc3545", fg="white", 
                             font=("Helvetica", 9, "bold"), relief="flat", cursor="hand2",
                             command=self.fazer_logoff)
        btn_sair.grid(row=0, column=2, padx=(0,20), pady=5, sticky='e')

        # =================================================================
        # 2. CORPO (Menu Lateral e Área Central)
        # =================================================================

        frame_corpo = tk.Frame(self.root, bg='#f8f9fa')
        frame_corpo.grid(row=1, column=0, sticky='nsew')
        # Grid do Corpo: 
        # Coluna 0 (Menu Lateral Fixo), 
        # Coluna 1 (Área Central Dinâmica)

        frame_corpo.rowconfigure(0, weight=1)
        frame_corpo.columnconfigure(0, weight=0, minsize=240)
        frame_corpo.columnconfigure(1, weight=1) # Área central

        # --- MENU LATERAL (Sidebar) ---
        frame_menu = tk.Frame(frame_corpo, bg='#0b0e14')
        frame_menu.grid(row=0, column=0, sticky='nsew')
        frame_menu.columnconfigure(0, weight=1)

        # Titulo do Menu
        lbl_logo_menu = tk.Label(frame_menu, text='Proton', bg="#0b0e14", fg="white", font=("Helvetica", 20, "bold"))
        lbl_logo_menu.grid(row=0, column=0, pady=(20,30))

        # Criação dos botões função auxilar
        self.criar_botao_menu(frame_menu, 'Dashboard (BI)', 1, self.abrir_dashboard)
        self.criar_botao_menu(frame_menu, 'Nuvem Dedicada', 2, self.abrir_dedicados)
        self.criar_botao_menu(frame_menu, 'Nuvem Compartilhada', 3, self.abrir_compartilhados)
        self.criar_botao_menu(frame_menu, 'Gestao FortesRH', 4, self.abrir_fortesrh)
        self.criar_botao_menu(frame_menu, 'Dashboard (BI)', 5, self.abrir_cancelamentos)
        self.criar_botao_menu(frame_menu, 'Dashboard (BI)', 6, self.abrir_configuracoes)

        # --- ÁREA CENTRAL (Content) ---
        self.area_central = tk.Frame(frame_corpo, bg='#f8f9fa')
        self.area_central.grid(row=0, column=1, sticky='nsew', padx=30, pady=30)
        self.area_central.rowconfigure(0, weight=1)
        self.area_central.columnconfigure(0, weight=1)

        # Inicia mostrando o Dashboard por padrão
        self.abrir_dashboard()

    def criar_botao_menu(self, pai, texto, linha, comando):
        """Função auxiliar para criar os botões do menu lateral (Grid) sem repetir código"""
        btn = ttk.Button(pai, text=texto, style="Menu.TButton", command=comando)
        btn.grid(row=linha, column=0, sticky='ew', padx=10, pady=2)

    def limpar_area_central(self):
        for widget in self.area_central.winfo_children():
            widget.destroy()

    # --- Controladores das Abas ---
    # --- Controladores das Abas ---
    def abrir_dashboard(self):
        self.limpar_area_central()
        ttk.Label(self.area_central, text="Dashboard de Inteligência (BI)", style="Titulo.TLabel").grid(row=0, column=0, sticky="nw")
                 
    def abrir_dedicados(self):
        self.limpar_area_central()
        ttk.Label(self.area_central, text="Módulo: Clientes Dedicados", style="Titulo.TLabel").grid(row=0, column=0, sticky="nw")
                 
    def abrir_compartilhados(self):
        self.limpar_area_central()
        ttk.Label(self.area_central, text="Módulo: Clientes Compartilhados", style="Titulo.TLabel").grid(row=0, column=0, sticky="nw")
                 
    def abrir_fortesrh(self):
        self.limpar_area_central()
        ttk.Label(self.area_central, text="Módulo: FortesRH", style="Titulo.TLabel").grid(row=0, column=0, sticky="nw")
                 
    def abrir_cancelamentos(self):
        self.limpar_area_central()
        ttk.Label(self.area_central, text="Módulo: Cancelamentos", style="Titulo.TLabel").grid(row=0, column=0, sticky="nw")
                 
    def abrir_configuracoes(self):
        self.limpar_area_central()
        ttk.Label(self.area_central, text="Configurações e Infraestrutura", style="Titulo.TLabel").grid(row=0, column=0, sticky="nw")

    def fazer_logoff(self):
        if messagebox.askyesno("Sair", "Deseja realmente encerrar a sessão?"):
            for widget in self.root.winfo_children():
                widget.destroy()
            from views.login_view import LoginView
            LoginView(self.root)