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

        lbl_status = tk.Label(frame_topo, text="●", bg="#1e2229", fg="#20c997", font=("Helvetica", 14))
        lbl_status.grid(row=0, column=1, padx=(20, 5))

        lbl_sessao = tk.Label(frame_topo, text=f'Sessão Ativa: {self.usuario.username}', 
                              bg="#1e2229", fg="white", font=("Helvetica", 10, "bold"))
        lbl_sessao.grid(row=0, column=2, sticky="w")

        btn_sair = tk.Button(frame_topo, text="Sair / Logoff", bg="#dc3545", fg="white", 
                             font=("Helvetica", 9, "bold"), relief="flat", cursor="hand2",
                             command=self.fazer_logoff)
        btn_sair.grid(row=0, column=3, padx=(20, 20), pady=5, sticky='e')

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
    def abrir_dashboard(self):
        self.limpar_area_central()
        ttk.Label(self.area_central, text="Dashboard de Inteligência (BI)", style="Titulo.TLabel").grid(row=0, column=0, sticky="nw")
                 
    def abrir_dedicados(self):
        self.limpar_area_central()
        
        # 1. Título
        ttk.Label(self.area_central, text="Módulo: Clientes Dedicados", style="Titulo.TLabel").grid(row=0, column=0, sticky="nw", pady=(0, 15))
        
        # 2. Barra de Ferramentas (Buscador e Botões)
        frame_ferramentas = tk.Frame(self.area_central, bg='#f8f9fa')
        frame_ferramentas.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        self.var_pesquisa = tk.StringVar()
        ent_pesquisa = ttk.Entry(frame_ferramentas, textvariable=self.var_pesquisa, width=50, font=("Helvetica", 11))
        ent_pesquisa.grid(row=0, column=0, padx=(0, 10))

        # --- Lógica do Placeholder (Texto de Dica) ---
        texto_dica = 'Pesquise por Nome do Cliente, CNPJ/CPF, etc...'
        ent_pesquisa.insert(0, texto_dica)
        ent_pesquisa.config(foreground='gray')

        def on_focus_in(event):
            if ent_pesquisa.get() == texto_dica:
                ent_pesquisa.delete(0, 'end')
                ent_pesquisa.config(foreground='black')
        
        def on_focus_out(event):
            if ent_pesquisa.get() == '':
                ent_pesquisa.delete(0, 'end')
                ent_pesquisa.config(foreground='gray')
        ent_pesquisa.bind('<FocusIn>', on_focus_in)
        ent_pesquisa.bind('<FocusOut>', on_focus_out)
        # ----------------------------------------------

        # O botão Buscar agora chama um método
        btn_buscar = ttk.Button(frame_ferramentas, text="🔍 Buscar", command=self.buscar_dedicado)
        btn_buscar.grid(row=0, column=1, padx=(0, 20))
        
        # Botões de Ação
        btn_novo = ttk.Button(frame_ferramentas, text="+ Cadastrar Novo", command=self.novo_dedicado)
        btn_novo.grid(row=0, column=2, padx=5)
        
        btn_detalhes = ttk.Button(frame_ferramentas, text="Detalhar Cliente", command=self.detalhar_dedicado)
        btn_detalhes.grid(row=0, column=3, padx=5)

        btn_editar = ttk.Button(frame_ferramentas, text="Editar Dados", command=self.editar_dedicado)
        btn_editar.grid(row=0, column=4, padx=5)
        
        btn_excluir = tk.Button(frame_ferramentas, text="Deletar", bg="#dc3545", fg="white", relief="flat", command=self.deletar_dedicado)
        btn_excluir.grid(row=0, column=5, padx=5, ipady=3, ipadx=5)
        
        # 3. Criar a Tabela(Treeview)
        colunas = ('ID', 'Cliente', 'CNPJ/CPF', 'Servidores', 'AD', 'Ambiente', 'VPN')
        self.tabela_dedicado = ttk.Treeview(self.area_central, columns=colunas, show='headings', selectmode='browse')
        self.tabela_dedicado.grid(row=2, column=0, sticky='nsew')
        
        larguras = [50, 300, 150, 80, 150, 100, 50] 
        for i, col in enumerate(colunas):
            self.tabela_dedicado.heading(col, text=col)
            self.tabela_dedicado.column(col, width=larguras[i], anchor='center')
            
        scrollbar = ttk.Scrollbar(self.area_central, orient='vertical', command=self.tabela_dedicado.yview)
        self.tabela_dedicado.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky='ns')
        
        self.area_central.rowconfigure(0, weight=0) # Título não estica
        self.area_central.rowconfigure(1, weight=0) # Frame Ferramentas não esticam
        self.area_central.rowconfigure(2, weight=1) # Tabela estica para preencher toda a tela
        
        self.carregar_tabela_dedicados()

    def carregar_tabela_dedicados(self):
        # Importação feita aqui para evitar dependências circulares no topo do arquivo
        from dao.cliente_dedicado_dao import ClienteDedicadoDAO

        # 1. Limpar dos dados antigos da tabela
        for item in self.tabela_dedicado.get_children():
            self.tabela_dedicado.delete(item)

        # 2. Buscar os dados no banco
        dao = ClienteDedicadoDAO()
        lista_clientes = dao.listar_todos()

        # 3. Inserir na interface
        for c in lista_clientes:
            vpn_formatado = 'Sim' if c.vpn else 'Não'
            self.tabela_dedicado.insert("", "end", values=(
                c.id, c.cliente, c.cnpj_cpf, c.qnt_de_servs, c.ad, c.ambiente, vpn_formatado
            ))

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
    # ----------------------------------------------
    
    # =================================================================
    # AÇÕES DO MÓDULO: CLIENTES DEDICADOS
    # =================================================================
    def buscar_dedicado(self):
        termo = self.var_pesquisa.get().strip()
        if termo == "Pesquise por Nome do Cliente, CNPJ/CPF, etc..." or termo == "":
            self.carregar_tabela_dedicados() # Se estiver vazio, recarrega todos
        else:
            # Aqui faremos o DAO buscar com filtro "LIKE %termo%"
            messagebox.showinfo("Buscador", f"Buscando por: {termo}\n(Lógica do DAO em breve!)")

    def novo_dedicado(self):
        from views.form_cliente_view import FromClienteView
        FromClienteView(self.root, tabela_atualizacao=self.carregar_tabela_dedicados)
    def detalhar_dedicado(self):
        selecionado = self.tabela_dedicado.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela para detalhar.")
            return
        # Pega o ID do cliente selecionado (é a coluna 0)
        item = self.tabela_dedicado.item(selecionado)
        id_cliente = item['values'][0]
        messagebox.showinfo("Detalhes", f"Mostrando detalhes do Cliente ID: {id_cliente}")

    def editar_dedicado(self):
        selecionado = self.tabela_dedicado.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela para editar.")
            return
        item = self.tabela_dedicado.item(selecionado)
        id_cliente = item['values'][0]
        messagebox.showinfo("Edição", f"Abrindo edição para o Cliente ID: {id_cliente}")

    def deletar_dedicado(self):
        selecionado = self.tabela_dedicado.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela para deletar.")
            return
            
        item = self.tabela_dedicado.item(selecionado)
        id_cliente = item['values'][0]
        nome_cliente = item['values'][1]
        
        # Confirmação de exclusão
        if messagebox.askyesno("Confirmar Exclusão", f"Tem a certeza que deseja excluir o cliente '{nome_cliente}'?"):
            messagebox.showinfo("Deletado", f"O cliente {id_cliente} seria deletado agora. (Lógica do DAO em breve!)")