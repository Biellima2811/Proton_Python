import tkinter as tk
from tkinter import ttk, messagebox

class FromClienteView:
    
    def __init__(self, root, tabela_atualizacao=None, cliente_id=None):
        self.root = root
        self.tabela_atualizacao = tabela_atualizacao
        self.cliente_id = cliente_id

        self.janela = tk.Toplevel(self.root)
        self.janela.title('Cadastro Novo Cliente Dedicado')
        self.janela.geometry('850x650')
        self.janela.configure(bg='#e9ecef')

        self.janela.grab_set()
        self.janela.focus_force()


        # Posicionamento da tela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (850 // 2)
        y = (self.janela.winfo_screenheight() //2) - (550 // 2)
        self.janela.geometry(f'+{x}+{y}')

        # Variaveis do Formulario Principal (aba1)
        self.var_nome = tk.StringVar()
        self.var_cnpj_cpf = tk.StringVar()
        self.var_qnt_servs = tk.StringVar(value='1')
        self.var_ad = tk.StringVar()
        self.var_ambiente = tk.StringVar()
        self.var_vpn = tk.BooleanVar()
        self.var_sgbd = tk.BooleanVar()
        
        # Variaveis para aba 2 - Informações dos servidores
        self.var_serv_tipo = tk.StringVar()
        self.var_serv_hostname = tk.StringVar()
        self.var_serv_ip_privado = tk.StringVar()
        self.var_serv_ip_publico = tk.StringVar()
        self.var_serv_user = tk.StringVar()
        self.var_serv_pass = tk.StringVar()

        self.construir_interface()

    def construir_interface(self):
        # Janela modal
        self.janela.rowconfigure(0, weight=1)
        self.janela.columnconfigure(0, weight=1)

        # Construir Container principal
        frame_bg = tk.Frame(self.janela, bg="#ffffff", bd=1, relief="solid")
        frame_bg.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        frame_bg.columnconfigure(0, weight=1)
        frame_bg.rowconfigure(2, weight=1) # O notebook se expande

        # Cabeçalho
        tk.Label(frame_bg, text="Triagem e Cadastro de Clientes - Nuvem Dedicada", 
                 font=("System", 18, "bold"), 
                 bg="#ffffff", fg="#212529").grid(row=0, column=0, sticky="w", padx=20, pady=(15, 0))
        
        tk.Label(frame_bg, text="Preencha as informações do novo cliente ou edite um registro existente.", 
                 font=("System", 12), bg="#ffffff", fg="#6c757d").grid(row=1, column=0, sticky="w", padx=20, pady=(0, 15))

        # Notebook (Abas)
        self.notebook = ttk.Notebook(frame_bg)
        self.notebook.grid(row=2, column=0, sticky='nsew', padx=20)

        self.aba_dados = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.aba_dados, text='Dados Principais do Cliente')

        self.aba_serv = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.aba_serv, text="Gestão de Servidores / Infra")

        self.construir_aba_dados()
        self.construir_aba_servidores()

        # Rodapé com Botões
        frame_botoes = tk.Frame(frame_bg, bg="#ffffff")
        frame_botoes.grid(row=3, column=0, sticky='e', padx=20, pady=15)

        btn_cancelar = tk.Button(frame_botoes, text='Cancelar', font='System 11 bold', 
                                 bg="#ffffff", fg="#dc3545", bd=1, relief="solid", 
                                 cursor="hand2", command=self.janela.destroy)
        btn_cancelar.grid(row=0, column=0, padx=10, ipadx=15, ipady=5)

        btn_salvar = tk.Button(frame_botoes, text='Salvar Cadastro ✔', font='System 11 bold', 
                               bg="#198754", fg="white", bd=0, cursor="hand2", command=self.salvar_cliente)
        btn_salvar.grid(row=0, column=1, ipadx=15, ipady=5)

    def construir_aba_dados(self):
        self.aba_dados.columnconfigure(0, weight=1)
        self.aba_dados.columnconfigure(1, weight=1)

        # Linha 0 e 1: Nome e CNPJ
        tk.Label(self.aba_dados, text='Nome / Cliente: ', 
                 font=("System", 9, "bold"), 
                 bg="#ffffff", fg="#495057").grid(row=0, column=0, sticky='w', padx=20, pady=(20,2))
        ttk.Entry(self.aba_dados, textvariable=self.var_nome, font=("System", 10)).grid(row=1, column=0, sticky='ew', padx=20, ipadx=4)

        tk.Label(self.aba_dados, text='CNPJ / CPF: ', 
                  font='System 9 bold', bg="#ffffff", 
                  fg="#495057").grid(row=0, column=1, sticky='w', padx=20, pady=(20,2))
        ttk.Entry(self.aba_dados, textvariable=self.var_cnpj_cpf, font='System 10').grid(row=1, column=1, sticky='ew', padx=20, ipadx=4)

        # Linha 2 e 3: Ambiente, VPN
        tk.Label(self.aba_dados, text="Ambiente:", font=("System", 9, "bold"), bg="#ffffff", fg="#495057").grid(row=2, column=0, sticky="w", padx=20, pady=(15, 2))
        cb_amb = ttk.Combobox(self.aba_dados, textvariable=self.var_ambiente, values=['Micro', 'Scaling'], font='System 10', state='readonly')
        cb_amb.grid(row=2, column=1, sticky='w', padx=15, ipady=4)

        tk.Label(self.aba_dados, text="Possui VPN:", font=("System", 9, "bold"), bg="#ffffff", fg="#495057").grid(row=2, column=2, sticky="w", padx=20, pady=(15, 2))
        cb_vpn = ttk.Combobox(self.aba_dados, textvariable=self.var_vpn, values=['Sim', 'Não'], font='System 10', state='readonly')
        cb_vpn.grid(row=2, column=3, sticky='w', padx=15, ipady=4)

        # Linha 4: AD e SGBD
        tk.Label(self.aba_dados, text='Active Diretory (AD):', font='System 9 bold', bg="#ffffff", fg="#495057").grid(row=4, column=0, sticky='w', padx=20, pady=(15,2))
        cb_AD = ttk.Combobox(self.aba_dados, textvariable=self.var_ad, values=['Fortes Tecnologia', 'Autos.Sky'], font='System 10', state='readonly')
        cb_AD.grid(row=4, column=1, sticky='w', padx=15, ipady=4)

        tk.Label(self.aba_dados, text='SGBD:', font='System 9 bold', bg="#ffffff", fg="#495057").grid(row=4, column=2, sticky='w', padx=20, pady=(15,2))
        cb_sgbd = ttk.Combobox(self.aba_dados, textvariable=self.var_sgbd, values=['Firebid', 'MSSQL'], font='System 10', state='readonly')
        cb_sgbd.grid(row=4, column=3, sticky='w', padx=15, ipady=4)

    def construir_aba_servidores(self):
        self.aba_serv.columnconfigure(0, weight=1)
        self.aba_serv.rowconfigure(2, weight=1)

        tk.Label(self.aba_serv, text="Adicione Máquinas vinculadas a este cliente:", 
                 font=("System", 12, "bold"), bg="#ffffff", fg="#212529").grid(row=0, column=0, sticky='w', padx=20, pady=(15,10))

        # Inputs de cadastro dos Servidores
        frame_inputs = tk.Frame(self.aba_serv, bg='#ffffff')
        frame_inputs.grid(row=1, column=0, sticky='ew', padx=20)

        # Linha 1 de Inputs (Tipo, Hostname, Botão +)
        tk.Label(frame_inputs, text='Tipo:', font='System 9 bold', bg="#ffffff", fg="#495057").grid(row=0, column=0, sticky='w', pady=(0,2))
        cb_tipo = ttk.Combobox(frame_inputs, textvariable=self.var_serv_tipo, 
                               values=['APP', 'BD', 'Repositorio', 'APP e BD', 'APP Fortes RH', 'BD Fortes RH', 'RH'], font='System 10', width=15)
        cb_tipo.grid(row=0, column=1, padx=(0,10), ipady=3)

        tk.Label(frame_inputs, text='Hostname:', font='System 9 bold', bg="#ffffff", fg="#495057").grid(row=0, column=2, sticky='w', pady=(0,2))
        tk.Entry(frame_inputs, textvariable=self.var_serv_hostname, font='System 10', width=20).grid(row=0, column=3, padx=(0,10), ipady=3)

        btn_add = tk.Button(frame_inputs, text='+', font='System 12 bold', bg="#0d6efd", fg="white", bd=0, cursor="hand2", command=self.adicionar_servidor)
        btn_add.grid(row=0, column=4, rowspan=3, sticky='ns', ipadx=10, pady=(10, 0)) # O botão ocupa várias linhas à direita

        # Linha 2 de Inputs (IP Privado e IP Público)
        tk.Label(frame_inputs, text='IP Privado:', font='System 9 bold', bg="#ffffff", fg="#495057").grid(row=1, column=0, sticky='w', pady=(5,2))
        tk.Entry(frame_inputs, textvariable=self.var_serv_ip_privado, font='System 10', width=20).grid(row=1, column=1, padx=(0,10), ipady=3, pady=(5,0))

        tk.Label(frame_inputs, text='IP Publico:', font='System 9 bold', bg="#ffffff", fg="#495057").grid(row=1, column=2, sticky='w', pady=(5,2))
        tk.Entry(frame_inputs, textvariable=self.var_serv_ip_publico, font='System 10', width=20).grid(row=1, column=3, padx=(0,10), ipady=3, pady=(5,0))

        # Linha 3 de Inputs (Usuário e Senha)
        tk.Label(frame_inputs, text='Usuário:', font='System 9 bold', bg="#ffffff", fg="#495057").grid(row=2, column=0, sticky='w', pady=(5,2))
        tk.Entry(frame_inputs, textvariable=self.var_serv_user, font='System 10', width=20).grid(row=2, column=1, padx=(0,10), ipady=3, pady=(5,0))

        tk.Label(frame_inputs, text='Senha:', font='System 9 bold', bg="#ffffff", fg="#495057").grid(row=2, column=2, sticky='w', pady=(5,2))
        tk.Entry(frame_inputs, textvariable=self.var_serv_pass, font='System 10', width=20).grid(row=2, column=3, padx=(0,10), ipady=3, pady=(5,0))


        # Tabela (Treeview)
        colunas = ('Tipo', 'Hostname', 'IP Privado', 'IP Publico', 'Usuário de Rede', 'Senha de Acesso')
        self.tabela_serv = ttk.Treeview(self.aba_serv, columns=colunas, show='headings', selectmode='browse')
        self.tabela_serv.grid(row=2, column=0, sticky='nsew', padx=20, pady=15)

        larguras = [100, 120, 120, 120, 120, 120]
        for i, col in enumerate(colunas):
            self.tabela_serv.heading(col, text=col)
            self.tabela_serv.column(col, width=larguras[i], anchor='center')

        # Adicionar barra de scroll à tabela
        scroll = ttk.Scrollbar(self.aba_serv, orient='vertical', command=self.tabela_serv.yview)
        self.tabela_serv.configure(yscrollcommand=scroll.set)
        scroll.grid(row=2, column=1, sticky='ns', pady=15)

        btn_del = tk.Button(self.aba_serv, text='Remover Servidor Selecionado', font='System 10 bold', bg="#dc3545", fg="white", bd=0, cursor="hand2", command=self.remover_servidor)

    def adicionar_servidor(self):
        tipo = self.var_serv_tipo.get().strip()
        hostname = self.var_serv_hostname.get().strip()
        ip_privado = self.var_serv_ip_privado.get().strip()
        ip_publico = self.var_serv_ip_publico.get().strip()
        user = self.var_serv_user.get().strip()
        senha = self.var_serv_pass.get().strip()

        if not tipo or not hostname:
            messagebox.showwarning('Aviso!', 'Preencha o Tipo e o Hostname.', parent=self.janela)
            return

        if not ip_privado or not ip_publico:
            messagebox.showwarning('Aviso!', 'Preencha o IP Privado e o Publico.', parent=self.janela)
            return

        if not user or not senha:
            messagebox.showwarning('Aviso', 'Preencha o Usuario e Senha do servidor', parent=self.janela)

        self.tabela_serv.insert('', 'end', values=(tipo, hostname, ip_privado, ip_publico, user, senha))

        self.var_serv_tipo.set("")
        self.var_serv_hostname.set("")
        self.var_serv_ip_privado.set("")
        self.var_serv_ip_publico.set("")
        self.var_serv_user.set("")
        self.var_serv_pass.set("")

    def remover_servidor(self):
        selecionado = self.tabela_serv.selection()
        if selecionado:
            self.tabela_serv.delete(selecionado)
        else:
            messagebox.showwarning('Aviso','Selecione um servidor para remover', parent=self.janela)

    def salvar_cliente(self):
        # Validação
        nome = self.var_nome.get().strip()
        cnpj = self.var_cnpj_cpf.get().strip()
        ambiente = self.var_ambiente.get().strip()
        
        # Correção da conversão de string para boolean (assumindo 'Sim' = True)
        vpn = True if self.var_vpn.get() == "Sim" else False
        sgbd = self.var_sgbd.get() # Variável já corrigida para String
        ad = self.var_ad.get().strip()
        
        if not nome or not cnpj:
            messagebox.showwarning("Aviso", "O nome do cliente e CNPJ/CPF são obrigatórios.", parent=self.janela)
            self.notebook.select(self.aba_dados)
            return
            
        # 1. Preparar os dados do Cliente
        from models.cliente_dedicado import ClienteDedicado # Assumindo a classe do projeto original
        qnt_serv = len(self.tabela_serv.get_children())
        
        # O construtor do Cliente recebe id=0 para novos registos
        cliente = ClienteDedicado(id=0, nome=nome, cnpj=cnpj, qnt_server=qnt_serv, 
                          active_directory=ad, ambiente=ambiente, vpn=vpn, sgbd=sgbd)
                          
        # 2. Preparar a lista de Servidores Dedicados
        from models.servidor_dedicado import ServidorDedicado
        lista_servidores = []
        for linha in self.tabela_serv.get_children():
            valores = self.tabela_serv.item(linha)['values']
            servidor = ServidorDedicado(
                tipo=valores[0], 
                ip=valores[2], # IP Privado (como exemplo, dependendo do que o DAO original espera)
                usuario=valores[4], 
                senha=valores[5]
            )
            lista_servidores.append(servidor)
            
        # 3. Guardar no Banco via DAO
        from dao.cliente_dedicado_dao import ClienteDedicadoDAO
        try:
            dao = ClienteDedicadoDAO()
            dao.salvar_com_servidores(cliente, lista_servidores)
            
            messagebox.showinfo("Sucesso", f"Cliente {nome} guardado com sucesso!", parent=self.janela)
            
            # Atualiza a tabela do MainView, se a referência foi passada
            if self.tabela_atualizacao:
                self.tabela_atualizacao()
                
            self.janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao guardar: {str(e)}", parent=self.janela)
