import tkinter as tk
from tkinter import ttk, messagebox

class MainView:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.root.title('Proton - Gestão de Infraestrutura')
        self.root.geometry('1200x700')
        self.root.configure(bg='#f4f6f9')
        
        try:
            self.root.state('zoomed')
        except:
            pass
            
        self.estilos = ttk.Style()
        self.estilos.configure("Menu.TButton", font=("Segoe UI", 11, "bold"), padding=10)
        self.estilos.configure("Titulo.TLabel", font=("Segoe UI", 22, "bold"), background="#f4f6f9", foreground="#212529")
        
        self.construir_interface()

    def construir_interface(self):
        self.root.rowconfigure(0, weight=0) 
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        # 1. CABEÇALHO (Top Bar)
        frame_topo = tk.Frame(self.root, bg='#1e2229', height=40)
        frame_topo.grid(row=0, column=0, sticky='nsew')
        frame_topo.columnconfigure(0, weight=1) 
        frame_topo.columnconfigure(1, weight=0) 
        frame_topo.columnconfigure(2, weight=0) 
        frame_topo.rowconfigure(0, weight=1)
        
        lbl_status = tk.Label(frame_topo, text="●", bg="#1e2229", fg="#20c997", font=("Segoe UI", 14))
        lbl_status.grid(row=0, column=1, padx=(20, 5))
        
        lbl_sessao = tk.Label(frame_topo, text=f'Sessão Ativa: {self.usuario.username}', bg="#1e2229", fg="white", font=("Segoe UI", 10, "bold"))
        lbl_sessao.grid(row=0, column=2, sticky="w")
        
        btn_sair = tk.Button(frame_topo, text="Sair / Logoff", bg="#dc3545", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=self.fazer_logoff)
        btn_sair.grid(row=0, column=3, padx=(20, 20), pady=5, sticky='e')

        # 2. CORPO (Menu Lateral e Área Central)
        frame_corpo = tk.Frame(self.root, bg='#f8f9fa')
        frame_corpo.grid(row=1, column=0, sticky='nsew')
        frame_corpo.rowconfigure(0, weight=1)
        frame_corpo.columnconfigure(0, weight=0, minsize=240)
        frame_corpo.columnconfigure(1, weight=1) 

        # --- MENU LATERAL (Sidebar) ---
        frame_menu = tk.Frame(frame_corpo, bg='#0b0e14')
        frame_menu.grid(row=0, column=0, sticky='nsew')
        frame_menu.columnconfigure(0, weight=1)
        
        lbl_logo_menu = tk.Label(frame_menu, text='Proton', bg="#0b0e14", fg="white", font=("Segoe UI", 20, "bold"))
        lbl_logo_menu.grid(row=0, column=0, pady=(20,30))
        
        self.criar_botao_menu(frame_menu, 'Dashboard (BI)', 1, self.abrir_dashboard)
        self.criar_botao_menu(frame_menu, 'Nuvem Dedicada', 2, self.abrir_dedicados)
        self.criar_botao_menu(frame_menu, 'Nuvem Compartilhada', 3, self.abrir_compartilhados)
        self.criar_botao_menu(frame_menu, 'Gestao FortesRH', 4, self.abrir_fortesrh)
        self.criar_botao_menu(frame_menu, 'Clientes Cancelados', 5, self.abrir_cancelamentos)
        self.criar_botao_menu(frame_menu, 'Configurações', 6, self.abrir_configuracoes)

        # --- ÁREA CENTRAL (Content) ---
        self.area_central = tk.Frame(frame_corpo, bg='#f8f9fa')
        self.area_central.grid(row=0, column=1, sticky='nsew', padx=30, pady=30)
        self.area_central.rowconfigure(0, weight=1)
        self.area_central.columnconfigure(0, weight=1)
        
        self.abrir_dashboard()

    def criar_botao_menu(self, pai, texto, linha, comando):
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
        
        ttk.Label(self.area_central, text="Módulo: Clientes Dedicados", style="Titulo.TLabel").grid(row=0, column=0, sticky="nw", pady=(0, 15))
        
        frame_ferramentas = tk.Frame(self.area_central, bg='#f8f9fa')
        frame_ferramentas.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        self.var_pesquisa = tk.StringVar()
        ent_pesquisa = ttk.Entry(frame_ferramentas, textvariable=self.var_pesquisa, width=50, font=("Segoe UI", 11))
        ent_pesquisa.grid(row=0, column=0, padx=(0, 10))
        
        texto_dica = 'Pesquise por Nome do Cliente, CNPJ/CPF...'
        ent_pesquisa.insert(0, texto_dica)
        ent_pesquisa.config(foreground='gray')
        
        def on_focus_in(event):
            if ent_pesquisa.get() == texto_dica:
                ent_pesquisa.delete(0, 'end')
                ent_pesquisa.config(foreground='black')
                
        def on_focus_out(event):
            if ent_pesquisa.get() == '':
                ent_pesquisa.insert(0, texto_dica)
                ent_pesquisa.config(foreground='gray')
                
        ent_pesquisa.bind('<FocusIn>', on_focus_in)
        ent_pesquisa.bind('<FocusOut>', on_focus_out)
        # BIND MAGICO: Ao largar qualquer tecla na caixa de texto, ativa a busca!
        ent_pesquisa.bind('<KeyRelease>', lambda e: self.buscar_dedicado())
        
        # O botão continua a existir se preferir clicar
        btn_buscar = ttk.Button(frame_ferramentas, text="🔍 Buscar", command=self.buscar_dedicado)
        btn_buscar.grid(row=0, column=1, padx=(0, 20))
        
        btn_novo = ttk.Button(frame_ferramentas, text="+ Cadastrar Novo", command=self.novo_dedicado)
        btn_novo.grid(row=0, column=2, padx=5)
        
        btn_editar = ttk.Button(frame_ferramentas, text="Editar Dados", command=self.editar_dedicado)
        btn_editar.grid(row=0, column=3, padx=5)
        
        btn_excluir = tk.Button(frame_ferramentas, text="Deletar", bg="#dc3545", fg="white", relief="flat", command=self.deletar_dedicado)
        btn_excluir.grid(row=0, column=4, padx=5, ipady=3, ipadx=5)
        
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
        
        self.area_central.rowconfigure(0, weight=0)
        self.area_central.rowconfigure(1, weight=0)
        self.area_central.rowconfigure(2, weight=1)
        
        self.carregar_tabela_dedicados()

    def carregar_tabela_dedicados(self):
        for item in self.tabela_dedicado.get_children():
            self.tabela_dedicado.delete(item)
            
        from dao.cliente_dedicado_dao import ClienteDedicadoDAO
        try:
            dao = ClienteDedicadoDAO()
            lista_clientes = dao.listar_todos()
            for c in lista_clientes:
                vpn_formatado = 'Sim' if c.vpn else 'Não'
                nome_cliente = c.cliente if c.cliente else "Sem Nome"
                cnpj_cpf = c.cnpj_cpf if c.cnpj_cpf else "N/A"
                qnt_servs = c.qnt_de_servs if c.qnt_de_servs is not None else 0
                ad = c.ad if c.ad else "N/A"
                ambiente = c.ambiente if c.ambiente else "N/A"
                self.tabela_dedicado.insert("", "end", values=(
                    c.id, nome_cliente, cnpj_cpf, qnt_servs, ad, ambiente, vpn_formatado
                ))
        except Exception as e:
            from util.logger import LoggerAuditoria
            LoggerAuditoria.erro(f"Erro ao carregar tabela de dedicados: {e}")
            messagebox.showerror("Erro", "Não foi possível carregar os dados do banco.")

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
    # AÇÕES DO MÓDULO: CLIENTES DEDICADOS
    # ----------------------------------------------
    def buscar_dedicado(self):
        termo = self.var_pesquisa.get().strip()
        texto_dica = 'Pesquise por Nome do Cliente, CNPJ/CPF...'
        
        if termo == texto_dica or termo == "":
            self.carregar_tabela_dedicados()
        else:
            for item in self.tabela_dedicado.get_children():
                self.tabela_dedicado.delete(item)
            from dao.cliente_dedicado_dao import ClienteDedicadoDAO
            try:
                dao = ClienteDedicadoDAO()
                lista_clientes = dao.buscar_por_termo(termo)
                for c in lista_clientes:
                    vpn_formatado = 'Sim' if c.vpn else 'Não'
                    nome_cliente = c.cliente if c.cliente else "Sem Nome"
                    cnpj_cpf = c.cnpj_cpf if c.cnpj_cpf else "N/A"
                    qnt_servs = c.qnt_de_servs if c.qnt_de_servs is not None else 0
                    ad = c.ad if c.ad else "N/A"
                    ambiente = c.ambiente if c.ambiente else "N/A"
                    self.tabela_dedicado.insert("", "end", values=(
                        c.id, nome_cliente, cnpj_cpf, qnt_servs, ad, ambiente, vpn_formatado
                    ))
            except Exception as e:
                messagebox.showerror("Erro", f"Erro na pesquisa:\n{e}")

    def novo_dedicado(self):
        from views.form_cliente_view import FormClienteView
        FormClienteView(self.root, tabela_atualizacao=self.carregar_tabela_dedicados)
        
    def editar_dedicado(self):
        selecionado = self.tabela_dedicado.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela para editar.")
            return
        item = self.tabela_dedicado.item(selecionado)
        id_cliente = item['values'][0]
        
        from views.form_cliente_view import FormClienteView
        FormClienteView(self.root, tabela_atualizacao=self.carregar_tabela_dedicados, cliente_id=id_cliente)

    def deletar_dedicado(self):
        selecionado = self.tabela_dedicado.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela para deletar.")
            return
                     
        item = self.tabela_dedicado.item(selecionado)
        id_cliente = item['values'][0]
        nome_cliente = item['values'][1]
                 
        if messagebox.askyesno("Confirmar Exclusão", f"Tem a certeza que deseja excluir o cliente '{nome_cliente}'?\n\nIsto apagará permanentemente todos os servidores e bancos de dados associados a ele."):
            from dao.cliente_dedicado_dao import ClienteDedicadoDAO
            try:
                dao = ClienteDedicadoDAO()
                dao.deletar(id_cliente)
                messagebox.showinfo("Sucesso", f"O cliente '{nome_cliente}' foi deletado do sistema.")
                self.carregar_tabela_dedicados()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível excluir o cliente. Detalhes:\n{e}")