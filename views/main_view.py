import tkinter as tk
from tkinter import messagebox


class MainView:
    def __init__(self, root: tk.Tk, usuario):
        self.root = root
        self.usuario = usuario

        # Configuração da Janela principal
        self.root.title('Proton - Gestão de Infraestrutura')
        self.root.geometry('1200x700')
        self.root.configure(bg='#f8f9fa')

        try:
            self.root.state('zoomed')
        except:
            pass

        self.construir_interface()

    def construir_interface(self):
        # =================================================================
        # GRID DA JANELA PRINCIPAL
        # =================================================================
        # A janela terá 2 linhas:
        # Linha 0 -> Cabeçalho Superior (Header)
        # Linha 1 -> Corpo (Menu Lateral + Área Central)
        self.root.rowconfigure(0, weight=0) # Cabeçalho não vai esticar na vertical
        self.root.rowconfigure(1, weight=2)
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
        lbl_logo_menu = tk.Label(frame_menu, text='')