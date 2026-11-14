import tkinter as tk
from tkinter import ttk, messagebox
import re

class FormClienteView:
         
    def __init__(self, root, tabela_atualizacao=None, cliente_id=None):
        self.root = root
        self.tabela_atualizacao = tabela_atualizacao
        self.cliente_id = cliente_id

        self.janela = tk.Toplevel(self.root)
        self.janela.title('Cadastro Novo Cliente Dedicado')
        self.janela.geometry('950x700')
        self.janela.configure(bg='#e9ecef')

        self.janela.grab_set()
        self.janela.focus_force()

        # Posicionamento da tela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (950 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (700 // 2)
        self.janela.geometry(f'+{x}+{y}')

        # Definir Fontes Globais
        self.fonte_normal = ("Segoe UI", 11)
        self.fonte_negrito = ("Segoe UI", 10, "bold")
        self.fonte_titulo = ("Segoe UI", 18, "bold")

        # Variáveis Aba 1
        self.var_nome = tk.StringVar()
        self.var_cnpj_cpf = tk.StringVar()
        self.var_ambiente = tk.StringVar()
        self.var_vpn = tk.StringVar() 
        self.var_sgbd = tk.StringVar() 
        self.var_ad = tk.StringVar()

        # Variáveis Aba 2
        self.var_serv_tipo = tk.StringVar()
        self.var_serv_hostname = tk.StringVar()
        self.var_serv_ip_privado = tk.StringVar()
        self.var_serv_ip_publico = tk.StringVar()
        self.var_serv_porta = tk.StringVar()
        self.var_serv_user = tk.StringVar()
        self.var_serv_pass = tk.StringVar()

        self.construir_interface()

    def construir_interface(self):
        self.janela.rowconfigure(0, weight=1)
        self.janela.columnconfigure(0, weight=1)

        frame_bg = tk.Frame(self.janela, bg="#ffffff", bd=1, relief="solid")
        frame_bg.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        frame_bg.columnconfigure(0, weight=1)
        frame_bg.rowconfigure(2, weight=1)

        tk.Label(frame_bg, text="Triagem e Cadastro de Clientes - Nuvem Dedicada", font=self.fonte_titulo, bg="#ffffff", fg="#212529").grid(row=0, column=0, sticky="w", padx=20, pady=(15, 0))
        tk.Label(frame_bg, text="Preencha as informações do novo cliente ou edite um registro existente.", font=("Segoe UI", 12), bg="#ffffff", fg="#6c757d").grid(row=1, column=0, sticky="w", padx=20, pady=(0, 15))

        self.notebook = ttk.Notebook(frame_bg)
        self.notebook.grid(row=2, column=0, sticky='nsew', padx=20)

        self.aba_dados = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.aba_dados, text='Dados Principais do Cliente')

        self.aba_serv = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.aba_serv, text="Gestão de Servidores / Infra")

        self.construir_aba_dados()
        self.construir_aba_servidores()

        frame_botoes = tk.Frame(frame_bg, bg="#ffffff")
        frame_botoes.grid(row=3, column=0, sticky='e', padx=20, pady=15)

        btn_cancelar = tk.Button(frame_botoes, text='Cancelar', font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#dc3545", bd=1, relief="solid", cursor="hand2", command=self.janela.destroy)
        btn_cancelar.grid(row=0, column=0, padx=10, ipadx=15, ipady=5)

        btn_salvar = tk.Button(frame_botoes, text='Salvar Cadastro ✔', font=("Segoe UI", 11, "bold"), bg="#198754", fg="white", bd=0, cursor="hand2", command=self.salvar_cliente)
        btn_salvar.grid(row=0, column=1, ipadx=15, ipady=5)

    def construir_aba_dados(self):
        self.aba_dados.columnconfigure(0, weight=1)
        self.aba_dados.columnconfigure(1, weight=1)

        # Campos mais largos
        tk.Label(self.aba_dados, text='Nome / Cliente: ', font=self.fonte_negrito, bg="#ffffff", fg="#495057").grid(row=0, column=0, sticky='w', padx=20, pady=(20,2))
        ttk.Entry(self.aba_dados, textvariable=self.var_nome, font=self.fonte_normal).grid(row=1, column=0, sticky='ew', padx=20, ipadx=4, ipady=4)

        tk.Label(self.aba_dados, text='CNPJ / CPF: ', font=self.fonte_negrito, bg="#ffffff", fg="#495057").grid(row=0, column=1, sticky='w', padx=20, pady=(20,2))
        ttk.Entry(self.aba_dados, textvariable=self.var_cnpj_cpf, font=self.fonte_normal).grid(row=1, column=1, sticky='ew', padx=20, ipadx=4, ipady=4)

        tk.Label(self.aba_dados, text="Ambiente:", font=self.fonte_negrito, bg="#ffffff", fg="#495057").grid(row=2, column=0, sticky="w", padx=20, pady=(15, 2))
        cb_amb = ttk.Combobox(self.aba_dados, textvariable=self.var_ambiente, values=['Micro', 'Scaling'], font=self.fonte_normal, state='readonly')
        cb_amb.grid(row=3, column=0, sticky='w', padx=20, ipady=4)

        tk.Label(self.aba_dados, text="Possui VPN:", font=self.fonte_negrito, bg="#ffffff", fg="#495057").grid(row=2, column=1, sticky="w", padx=20, pady=(15, 2))
        cb_vpn = ttk.Combobox(self.aba_dados, textvariable=self.var_vpn, values=['Sim', 'Não'], font=self.fonte_normal, state='readonly')
        cb_vpn.grid(row=3, column=1, sticky='w', padx=20, ipady=4)

        tk.Label(self.aba_dados, text='Active Diretory (AD):', font=self.fonte_negrito, bg="#ffffff", fg="#495057").grid(row=4, column=0, sticky='w', padx=20, pady=(15,2))
        cb_AD = ttk.Combobox(self.aba_dados, textvariable=self.var_ad, values=['Fortes Tecnologia', 'Autos.Sky'], font=self.fonte_normal, state='readonly')
        cb_AD.grid(row=5, column=0, sticky='w', padx=20, ipady=4)

        tk.Label(self.aba_dados, text='SGBD:', font=self.fonte_negrito, bg="#ffffff", fg="#495057").grid(row=4, column=1, sticky='w', padx=20, pady=(15,2))
        cb_sgbd = ttk.Combobox(self.aba_dados, textvariable=self.var_sgbd, values=['Firebird', 'MSSQL'], font=self.fonte_normal, state='readonly')
        cb_sgbd.grid(row=5, column=1, sticky='w', padx=20, ipady=4)

    def construir_aba_servidores(self):
        self.aba_serv.columnconfigure(0, weight=1)
        self.aba_serv.rowconfigure(2, weight=1)

        tk.Label(self.aba_serv, text="Adicione Máquinas vinculadas a este cliente:", font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#212529").grid(row=0, column=0, sticky='w', padx=20, pady=(15,10))

        frame_inputs = tk.Frame(self.aba_serv, bg='#ffffff')
        frame_inputs.grid(row=1, column=0, sticky='ew', padx=20)

        # Linha 1
        tk.Label(frame_inputs, text='Tipo:', font=self.fonte_negrito, bg="#ffffff", fg="#495057").grid(row=0, column=0, sticky='w', pady=(0,2))
        cb_tipo = ttk.Combobox(frame_inputs, textvariable=self.var_serv_tipo, values=['APP', 'BD', 'Repositorio', 'APP e BD', 'APP Fortes RH', 'BD Fortes RH', 'RH'], font=self.fonte_normal, width=15)
        cb_tipo.grid(row=0, column=1, padx=(0,10), ipady=3)

        tk.Label(frame_inputs, text='Hostname:', font=self.fonte_negrito, bg="#ffffff", fg="#495057").grid(row=0, column=2, sticky='w', pady=(0,2))
        tk.Entry(frame_inputs, textvariable=self.var_serv_hostname, font=self.fonte_normal, width=20).grid(row=0, column=3, padx=(0,10), ipady=3)
        
        btn_add = tk.Button(frame_inputs, text='+ Adicionar', font=("Segoe UI", 14, "bold"), bg="#0d6efd", fg="white", bd=0, cursor="hand2", command=self.adicionar_servidor)
        btn_add.grid(row=0, column=4, rowspan=3, sticky='ns', ipadx=15, pady=(10,0)) 

        # Linha 2
        tk.Label(frame_inputs, text='IP Privado:', font=self.fonte_negrito, bg="#ffffff", fg="#495057").grid(row=1, column=0, sticky='w', pady=(5,2))
        tk.Entry(frame_inputs, textvariable=self.var_serv_ip_privado, font=self.fonte_normal, width=20).grid(row=1, column=1, padx=(0,10), ipady=3, pady=(5,0))

        tk.Label(frame_inputs, text='IP Publico:', font=self.fonte_negrito, bg="#ffffff", fg="#495057").grid(row=1, column=2, sticky='w', pady=(5,2))
        tk.Entry(frame_inputs, textvariable=self.var_serv_ip_publico, font=self.fonte_normal, width=20).grid(row=1, column=3, padx=(0,10), ipady=3, pady=(5,0))

        # Linha 3
        tk.Label(frame_inputs, text='Porta/RDP:', font=self.fonte_negrito, bg="#ffffff", fg="#495057").grid(row=2, column=0, sticky='w', pady=(5,2))
        tk.Entry(frame_inputs, textvariable=self.var_serv_porta, font=self.fonte_normal, width=20).grid(row=2, column=1, padx=(0,10), ipady=3, pady=(5,0))

        tk.Label(frame_inputs, text='Usuário:', font=self.fonte_negrito, bg="#ffffff", fg="#495057").grid(row=2, column=2, sticky='w', pady=(5,2))
        tk.Entry(frame_inputs, textvariable=self.var_serv_user, font=self.fonte_normal, width=20).grid(row=2, column=3, padx=(0,10), ipady=3, pady=(5,0))

        tk.Label(frame_inputs, text='Senha:', font=self.fonte_negrito, bg="#ffffff", fg="#495057").grid(row=3, column=0, sticky='w', pady=(5,2))
        tk.Entry(frame_inputs, textvariable=self.var_serv_pass, font=self.fonte_normal, width=20).grid(row=3, column=1, padx=(0,10), ipady=3, pady=(5,10))

        # Tabela (Treeview)
        colunas = ('Tipo', 'Hostname', 'IP Privado', 'IP Publico', 'Porta', 'Usuário de Rede', 'Senha de Acesso')
        self.tabela_serv = ttk.Treeview(self.aba_serv, columns=colunas, show='headings', selectmode='browse')
        self.tabela_serv.grid(row=2, column=0, sticky='nsew', padx=20, pady=15)

        larguras = [100, 120, 100, 100, 60, 100, 100]
        for i, col in enumerate(colunas):
            self.tabela_serv.heading(col, text=col)
            self.tabela_serv.column(col, width=larguras[i], anchor='center')

        scroll = ttk.Scrollbar(self.aba_serv, orient='vertical', command=self.tabela_serv.yview)
        self.tabela_serv.configure(yscrollcommand=scroll.set)
        scroll.grid(row=2, column=1, sticky='ns', pady=15)

        btn_del = tk.Button(self.aba_serv, text='Remover Servidor Selecionado', font=("Segoe UI", 10, "bold"), bg="#dc3545", fg="white", bd=0, cursor="hand2", command=self.remover_servidor)
        btn_del.grid(row=3, column=0, sticky='w', padx=20, pady=(0,15), ipadx=10, ipady=3)

    def is_valid_ip(self, ip_str):
        if not ip_str: 
            return True 
        pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        return re.match(pattern, ip_str) is not None

    def adicionar_servidor(self):
        tipo = self.var_serv_tipo.get().strip()
        hostname = self.var_serv_hostname.get().strip()
        ip_privado = self.var_serv_ip_privado.get().strip()
        ip_publico = self.var_serv_ip_publico.get().strip()
        porta = self.var_serv_porta.get().strip()
        user = self.var_serv_user.get().strip()
        senha = self.var_serv_pass.get().strip()

        if not tipo or not hostname:
            messagebox.showwarning('Aviso!', 'Preencha o Tipo e o Hostname.', parent=self.janela)
            return

        if not ip_privado and not ip_publico:
            messagebox.showwarning('Aviso!', 'Preencha pelo menos um IP (Privado ou Público).', parent=self.janela)
            return

        if not self.is_valid_ip(ip_privado) or not self.is_valid_ip(ip_publico):
            messagebox.showwarning('Aviso!', 'Formato de IP inválido. Exemplo: 192.168.0.1', parent=self.janela)
            return

        if not user or not senha:
            messagebox.showwarning('Aviso!', 'Os campos Usuário e Senha são obrigatórios!', parent=self.janela)
            return

        self.tabela_serv.insert('', 'end', values=(tipo, hostname, ip_privado, ip_publico, porta, user, senha))

        self.var_serv_tipo.set("")
        self.var_serv_hostname.set("")
        self.var_serv_ip_privado.set("")
        self.var_serv_ip_publico.set("")
        self.var_serv_porta.set("")
        self.var_serv_user.set("")
        self.var_serv_pass.set("")

    def remover_servidor(self):
        selecionado = self.tabela_serv.selection()
        if selecionado:
            self.tabela_serv.delete(selecionado)
        else:
            messagebox.showwarning('Aviso','Selecione um servidor para remover.', parent=self.janela)

    def salvar_cliente(self):
        nome = self.var_nome.get().strip()
        cnpj = self.var_cnpj_cpf.get().strip()
        ambiente = self.var_ambiente.get().strip()
        vpn_str = self.var_vpn.get().strip()
        sgbd = self.var_sgbd.get().strip()
        ad = self.var_ad.get().strip()
                 
        if not nome or not cnpj:
            messagebox.showwarning("Aviso", "O nome do cliente e CNPJ/CPF são obrigatórios.", parent=self.janela)
            self.notebook.select(self.aba_dados)
            return
            
        if not ambiente or not vpn_str:
            messagebox.showwarning("Aviso", "O campo de Ambiente e VPN são obrigatórios.", parent=self.janela)
            self.notebook.select(self.aba_dados)
            return
            
        if not sgbd or not ad:
            messagebox.showwarning("Aviso", "O campo de SGBD e AD (Active Directory) são obrigatórios.", parent=self.janela)
            self.notebook.select(self.aba_dados)
            return

        # VERIFICAÇÃO DE DADOS NA ABA 2 (Obrigatório ter pelo menos 1 servidor)
        qnt_serv = len(self.tabela_serv.get_children())
        if qnt_serv == 0:
            messagebox.showwarning("Aviso", "Não é possível salvar um cliente sem infraestrutura. Adicione pelo menos um servidor na aba 2.", parent=self.janela)
            self.notebook.select(self.aba_serv)
            return
            
        vpn = True if vpn_str == "Sim" else False

        from models.cliente_dedicado import ClienteDedicado 
                 
        # Os nomes dos argumentos foram ajustados para coincidir exatamente com os parâmetros da classe ClienteDedicado
        cliente = ClienteDedicado(
            id_cliente=0, 
            cliente=nome, 
            cnpj_cpf=cnpj, 
            qnt_de_servs=qnt_serv,
            ad=ad, 
            ambiente=ambiente, 
            vpn=vpn
        )
        cliente.sgbd = sgbd

        from models.servidor_dedicado import ServidorDedicado
        lista_servidores = []
        for linha in self.tabela_serv.get_children():
            valores = self.tabela_serv.item(linha)['values']
            servidor = ServidorDedicado(
                tipo=str(valores[0]), 
                hostname=str(valores[1]),
                ip_privado=str(valores[2]),
                ip_publico=str(valores[3]),
                usuario=str(valores[5]),
                senha=str(valores[6])
            )
            servidor.porta = str(valores[4])
            lista_servidores.append(servidor)
                     
        from dao.cliente_dedicado_dao import ClienteDedicadoDAO
        try:
            dao = ClienteDedicadoDAO()
            dao.salvar_com_servidores(cliente, lista_servidores)
                         
            messagebox.showinfo("Sucesso", f"Cliente {nome} guardado com sucesso!", parent=self.janela)
                         
            self.var_nome.set("")
            self.var_cnpj_cpf.set("")
            self.var_ambiente.set("")
            self.var_vpn.set("")
            self.var_sgbd.set("")
            self.var_ad.set("")
            
            for item in self.tabela_serv.get_children():
                self.tabela_serv.delete(item)
            
            if self.tabela_atualizacao:
                self.tabela_atualizacao()
                             
            self.janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao guardar:\n{str(e)}", parent=self.janela)