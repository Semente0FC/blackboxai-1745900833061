import tkinter as tk
from tkinter import ttk, messagebox
import MetaTrader5 as mt5
from utils import obter_saldo
from estrategia import EstrategiaTrading
from log_system import LogSystem
import threading
import time
from datetime import datetime


class PainelApp:  # Changed from EnhancedPainelApp to PainelApp to match imports
    def __init__(self, root):
        self.root = root
        self.root.title("Future MT5 Pro Trading")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Theme colors
        self.dark_theme = {
            'bg_dark': '#0A0A0A',  # Darker background
            'bg_medium': '#1E1E1E',  # Medium background
            'bg_light': '#2D2D2D',  # Light background
            'accent': '#00C853',  # Vibrant green
            'accent_hover': '#00E676',  # Lighter green
            'warning': '#FFB300',  # Warning color
            'danger': '#FF3D00',  # Danger color
            'text': '#FFFFFF',  # White text
            'text_secondary': '#B3B3B3'  # Gray text
        }

        self.light_theme = {
            'bg_dark': '#F5F5F5',  # Light gray background
            'bg_medium': '#FFFFFF',  # White background
            'bg_light': '#FAFAFA',  # Very light gray
            'accent': '#00C853',  # Keep green
            'accent_hover': '#00E676',  # Keep hover
            'warning': '#FFB300',  # Keep warning
            'danger': '#FF3D00',  # Keep danger
            'text': '#212121',  # Dark text
            'text_secondary': '#757575'  # Gray text
        }

        self.is_dark_mode = True
        self.colors = self.dark_theme

        self.root.configure(bg=self.colors['bg_dark'])
        self.root.resizable(False, False)
        self.centralizar_janela(1000, 700)

        # Multi-asset trading variables
        self.ativos = []  # List to store active assets
        self.estrategias = {}  # Dictionary to store strategy instances
        self.asset_frames = {}  # Dictionary to store asset UI frames
        self.status_labels = {}  # Dictionary to store status labels
        self.max_assets = 4  # Maximum number of assets to trade

        # Trading variables for each asset
        self.ativo_selecionado = {}
        self.timeframe_selecionado = {}
        self.lote_selecionado = {}
        self.operando = {}

        for i in range(self.max_assets):
            self.ativo_selecionado[i] = tk.StringVar()
            self.timeframe_selecionado[i] = tk.StringVar()
            self.lote_selecionado[i] = tk.StringVar(value="0.10")
            self.operando[i] = False

        self.log_system = LogSystem()

        self.setup_styles()
        self.setup_ui()

    def centralizar_janela(self, largura, altura):
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Combobox style
        style.configure("Custom.TCombobox",
                        fieldbackground=self.colors['bg_light'],
                        background=self.colors['bg_light'],
                        foreground=self.colors['text'],
                        arrowcolor=self.colors['accent'],
                        selectbackground=self.colors['accent'],
                        selectforeground=self.colors['text'])

        # Update style on theme change
        self.root.bind('<<ThemeChanged>>', lambda e: self.update_styles())

    def update_styles(self):
        style = ttk.Style()
        style.configure("Custom.TCombobox",
                        fieldbackground=self.colors['bg_light'],
                        background=self.colors['bg_light'],
                        foreground=self.colors['text'],
                        arrowcolor=self.colors['accent'],
                        selectbackground=self.colors['accent'],
                        selectforeground=self.colors['text'])

    def setup_ui(self):
        # Theme switcher at the very top
        self.setup_theme_switcher(self.root)

        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'], padx=20, pady=20)
        main_container.pack(fill="both", expand=True)

        # Header
        self.setup_header(main_container)

        # Trading dashboard
        self.setup_dashboard(main_container)

        # Control panel
        self.setup_control_panel(main_container)

        # Time display
        time_frame = tk.Frame(main_container, bg=self.colors['bg_medium'], padx=20, pady=10)
        time_frame.pack(fill="x")

        self.time_label = tk.Label(
            time_frame,
            text="",
            font=("Helvetica", 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_medium']
        )
        self.time_label.pack(side="right")

        # Start data update threads
        self.start_update_threads()

    def setup_theme_switcher(self, parent):
        # Create a frame at the top of the window
        switcher_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        switcher_frame.pack(fill="x")

        # Add padding frame to position the button
        padding_frame = tk.Frame(switcher_frame, bg=self.colors['bg_dark'], height=10)
        padding_frame.pack(fill="x")

        # Create the theme toggle button with a more visible style
        self.theme_button = tk.Button(
            switcher_frame,
            text="☀️ Modo Claro" if self.is_dark_mode else "🌙 Modo Escuro",
            command=self.toggle_theme,
            font=("Helvetica", 10, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg_light'],
            activebackground=self.colors['accent_hover'],
            activeforeground=self.colors['text'],
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.theme_button.pack(side="right", padx=20, pady=5)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.colors = self.dark_theme if self.is_dark_mode else self.light_theme

        # Update theme button with animation effect
        self.theme_button.config(
            text="☀️ Modo Claro" if self.is_dark_mode else "🌙 Modo Escuro",
            fg=self.colors['text'],
            bg=self.colors['bg_light']
        )

        # Create animation effect
        self.theme_button.config(relief="sunken")
        self.root.after(100, lambda: self.theme_button.config(relief="flat"))

        # Update all widgets
        self.update_theme()

        # Generate theme changed event
        self.root.event_generate('<<ThemeChanged>>')

    def update_theme(self):
        # Update root
        self.root.configure(bg=self.colors['bg_dark'])

        # Update all frames and widgets
        for widget in self.root.winfo_children():
            self.update_widget_colors(widget)

    def update_widget_colors(self, widget):
        widget_type = widget.winfo_class()

        if widget_type in ['Frame', 'Labelframe']:
            if widget.cget('bg') in [self.dark_theme['bg_dark'], self.light_theme['bg_dark']]:
                widget.configure(bg=self.colors['bg_dark'])
            elif widget.cget('bg') in [self.dark_theme['bg_medium'], self.light_theme['bg_medium']]:
                widget.configure(bg=self.colors['bg_medium'])
            elif widget.cget('bg') in [self.dark_theme['bg_light'], self.light_theme['bg_light']]:
                widget.configure(bg=self.colors['bg_light'])

        elif widget_type == 'Label':
            widget.configure(
                bg=widget.master.cget('bg'),
                fg=self.colors['text'] if widget.cget('fg') == self.dark_theme['text'] else self.colors[
                    'text_secondary']
            )

        elif widget_type == 'Button':
            if widget.cget('bg') == self.colors['accent']:
                # Don't change accent buttons
                pass
            else:
                widget.configure(
                    bg=self.colors['bg_light'],
                    fg=self.colors['text'],
                    activebackground=self.colors['accent_hover'],
                    activeforeground=self.colors['text']
                )

        elif widget_type == 'Text':
            widget.configure(
                bg=self.colors['bg_light'],
                fg=self.colors['text'],
                insertbackground=self.colors['text']
            )

        # Update children widgets
        for child in widget.winfo_children():
            self.update_widget_colors(child)

    def setup_header(self, parent):
        header = tk.Frame(parent, bg=self.colors['bg_dark'])
        header.pack(fill="x", pady=(0, 20))

        # Logo and title container
        title_container = tk.Frame(header, bg=self.colors['bg_dark'])
        title_container.pack(side="left")

        logo_label = tk.Label(
            title_container,
            text="📈",
            font=("Helvetica", 32),
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        )
        logo_label.pack(side="left", padx=(0, 10))

        title_label = tk.Label(
            title_container,
            text="FUTURE MT5 PRO",
            font=("Helvetica", 24, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg_dark']
        )
        title_label.pack(side="left")

        # Balance display
        self.saldo_frame = tk.Frame(header, bg=self.colors['bg_light'], padx=15, pady=10)
        self.saldo_frame.pack(side="right")

        tk.Label(
            self.saldo_frame,
            text="SALDO",
            font=("Helvetica", 10, "bold"),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_light']
        ).pack()

        self.saldo_label = tk.Label(
            self.saldo_frame,
            text="R$ 0.00",
            font=("Helvetica", 18, "bold"),
            fg=self.colors['accent'],
            bg=self.colors['bg_light']
        )
        self.saldo_label.pack()

    def setup_dashboard(self, parent):
        dashboard = tk.Frame(parent, bg=self.colors['bg_medium'], padx=20, pady=20)
        dashboard.pack(fill="both", expand=True)

        # Create 2x2 grid for assets
        for i in range(2):
            dashboard.grid_rowconfigure(i, weight=1)
            dashboard.grid_columnconfigure(i, weight=1)

        # Create asset cards
        for i in range(self.max_assets):
            row = i // 2
            col = i % 2
            self.create_asset_card(dashboard, i, row, col)

    def create_input_group(self, parent, label):
        frame = tk.Frame(parent, bg=self.colors['bg_medium'])

        tk.Label(
            frame,
            text=label,
            font=("Helvetica", 10, "bold"),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_medium']
        ).pack(anchor="w", pady=(0, 5))

        return frame

    def setup_control_panel(self, parent):
        control_panel = tk.Frame(parent, bg=self.colors['bg_medium'], padx=20, pady=20)
        control_panel.pack(fill="x", pady=(0, 20))

        # Global refresh button
        self.btn_atualizar = self.create_button(
            control_panel,
            "🔄 Atualizar Ativos",
            self.carregar_ativos,
            self.colors['bg_light']
        )
        self.btn_atualizar.pack(side="right")

    def create_button(self, parent, text, command, color):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Helvetica", 11, "bold"),
            fg=self.colors['text'],
            bg=color,
            activebackground=self.colors['accent_hover'],
            activeforeground=self.colors['text'],
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )

    def create_asset_card(self, parent, index, row, col):
        # Create card with 3D effect
        card = tk.Frame(
            parent,
            bg=self.colors['bg_light'],
            relief="raised",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=self.colors['accent']
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Add inner shadow effect
        inner_frame = tk.Frame(
            card,
            bg=self.colors['bg_light'],
            padx=15,
            pady=15
        )
        inner_frame.pack(fill="both", expand=True)

        # Asset header
        header = tk.Frame(inner_frame, bg=self.colors['bg_light'])
        header.pack(fill="x", pady=(0, 10))

        title = tk.Label(
            header,
            text=f"ATIVO {index + 1}",
            font=("Helvetica", 12, "bold"),
            fg=self.colors['accent'],
            bg=self.colors['bg_light']
        )
        title.pack(side="left")

        # Trading controls
        controls = tk.Frame(inner_frame, bg=self.colors['bg_light'])
        controls.pack(fill="x", pady=(0, 10))

        # Asset selection
        asset_frame = self.create_input_group(controls, "Ativo")
        combo_ativo = ttk.Combobox(
            asset_frame,
            textvariable=self.ativo_selecionado[index],
            style="Custom.TCombobox",
            width=20
        )
        combo_ativo.pack(fill="x")

        # Timeframe selection
        timeframe_frame = self.create_input_group(controls, "Timeframe")
        combo_timeframe = ttk.Combobox(
            timeframe_frame,
            textvariable=self.timeframe_selecionado[index],
            values=["M1", "M5", "M15", "M30", "H1", "H4", "D1"],
            style="Custom.TCombobox",
            width=20
        )
        combo_timeframe.pack(fill="x")
        combo_timeframe.current(1)

        # Lot size
        lot_frame = self.create_input_group(controls, "Lote")
        entry_lote = tk.Entry(
            lot_frame,
            textvariable=self.lote_selecionado[index],
            font=("Helvetica", 11),
            bg=self.colors['bg_medium'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief="flat",
            width=20
        )
        entry_lote.pack(fill="x")

        # Organize frames horizontally
        asset_frame.pack(side="left", padx=(0, 5))
        timeframe_frame.pack(side="left", padx=5)
        lot_frame.pack(side="left", padx=(5, 0))

        # Status and buttons
        status_frame = tk.Frame(inner_frame, bg=self.colors['bg_light'])
        status_frame.pack(fill="x", pady=10)

        self.status_labels[index] = tk.Label(
            status_frame,
            text="⭘ AGUARDANDO",
            font=("Helvetica", 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_light']
        )
        self.status_labels[index].pack(side="left")

        # Control buttons with modern styling
        btn_frame = tk.Frame(status_frame, bg=self.colors['bg_light'])
        btn_frame.pack(side="right")

        start_btn = tk.Button(
            btn_frame,
            text="▶",
            command=lambda: self.iniciar_robo(index),
            font=("Helvetica", 11),
            fg=self.colors['text'],
            bg=self.colors['accent'],
            activebackground=self.colors['accent_hover'],
            relief="flat",
            width=3,
            cursor="hand2"
        )
        start_btn.pack(side="left", padx=2)

        stop_btn = tk.Button(
            btn_frame,
            text="⏹",
            command=lambda: self.parar_robo(index),
            font=("Helvetica", 11),
            fg=self.colors['text'],
            bg=self.colors['danger'],
            activebackground=self.colors['danger'],
            relief="flat",
            width=3,
            cursor="hand2"
        )
        stop_btn.pack(side="left", padx=2)

        # Log area with modern styling
        log_frame = tk.Frame(inner_frame, bg=self.colors['bg_medium'])
        log_frame.pack(fill="both", expand=True)

        text_log = tk.Text(
            log_frame,
            height=8,
            bg=self.colors['bg_medium'],
            fg=self.colors['text'],
            font=("Consolas", 9),
            relief="flat",
            padx=10,
            pady=10
        )
        text_log.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_frame, command=text_log.yview)
        scrollbar.pack(side="right", fill="y")
        text_log.config(yscrollcommand=scrollbar.set)

        # Store references
        self.asset_frames[index] = {
            'card': card,
            'combo_ativo': combo_ativo,
            'combo_timeframe': combo_timeframe,
            'entry_lote': entry_lote,
            'text_log': text_log
        }

        # Add log widget to log system
        self.log_system.add_log_widget(f"asset_{index}", text_log)

    def start_update_threads(self):
        # Update balance
        threading.Thread(target=self.atualizar_saldo_loop, daemon=True).start()
        # Update time
        threading.Thread(target=self.atualizar_hora_loop, daemon=True).start()
        # Load initial assets
        self.carregar_ativos()

    def atualizar_hora_loop(self):
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            self.time_label.config(text=current_time)
            time.sleep(1)

    def atualizar_saldo_loop(self):
        while True:
            saldo = obter_saldo()
            self.saldo_label.config(text=f"R$ {saldo:.2f}")
            time.sleep(5)

    def tem_ativos_operando(self):
        """Check if any assets are currently running"""
        return any(self.operando.values())

    def carregar_ativos(self):
        try:
            symbols = mt5.symbols_get()
            lista_ativos = [symbol.name for symbol in symbols if symbol.visible]
            
            # Update all asset comboboxes
            for i in range(self.max_assets):
                if i in self.asset_frames:
                    self.asset_frames[i]['combo_ativo']['values'] = lista_ativos
                    if lista_ativos:
                        self.asset_frames[i]['combo_ativo'].current(0)
            
            ativos_ativos = sum(1 for i in range(self.max_assets) if i in self.asset_frames)
            self.log_system.logar(f"✅ {len(lista_ativos)} ativos disponíveis carregados em {ativos_ativos} cards")
        except Exception as e:
            self.log_system.logar(f"❌ Erro ao carregar ativos: {e}")

    def verificar_campos(self, index):
        """Verify fields for a specific asset"""
        ativo = self.ativo_selecionado[index].get().strip()
        timeframe = self.timeframe_selecionado[index].get().strip()
        lote = self.lote_selecionado[index].get().strip()
        
        # Fields are verified individually per asset now, no need to enable/disable buttons
        if not all([ativo, timeframe, lote]):
            self.log_system.logar(f"⚠️ Preencha todos os campos para o Ativo {index + 1}", f"asset_{index}")
            return False
        return True

    def iniciar_robo(self, index):
        ativo = self.ativo_selecionado[index].get().strip()
        timeframe = self.timeframe_selecionado[index].get().strip()
        lote = self.lote_selecionado[index].get().strip()

        if not ativo:
            self.log_system.logar(f"⚠️ Selecione um ativo para operar! (Ativo {index + 1})", f"asset_{index}")
            return
        if not timeframe:
            self.log_system.logar(f"⚠️ Selecione um timeframe para operar! (Ativo {index + 1})", f"asset_{index}")
            return
        if not lote:
            self.lote_selecionado[index].set("0.10")
            lote = "0.10"
            self.log_system.logar(f"⚠️ Lote vazio. Valor padrão 0.10 atribuído (Ativo {index + 1})", f"asset_{index}")

        try:
            lote_float = round(float(lote), 2)
            if lote_float <= 0:
                self.log_system.logar("⚠️ O lote deve ser maior que zero.")
                return
        except ValueError:
            messagebox.showerror("Erro de Lote", "Valor de lote inválido! Informe um número válido como 0.10")
            self.log_system.logar("❌ Erro: Lote inválido informado.")
            return

        info = mt5.symbol_info(ativo)
        if info is None:
            self.log_system.logar(f"❌ Ativo {ativo} não encontrado no MetaTrader 5.")
            return
        if not info.visible:
            self.log_system.logar(f"⚠️ Ativo {ativo} não está visível no MT5. Abra o ativo no terminal!")
            return
        if info.trade_mode != mt5.SYMBOL_TRADE_MODE_FULL:
            self.log_system.logar(f"❌ Ativo {ativo} não está liberado para operar (modo inválido)!")
            return

        tick = mt5.symbol_info_tick(ativo)
        if tick is None:
            self.log_system.logar(f"❌ Não foi possível obter preços do ativo {ativo}.")
            return

        spread = (tick.ask - tick.bid) / info.point
        spread_maximo_aceito = 50

        if spread > spread_maximo_aceito:
            self.log_system.logar(
                f"⚠️ Spread do ativo {ativo} está muito alto ({spread:.1f} pontos). Análise bloqueada.")
            return

        if tick.bid == 0 or tick.ask == 0:
            self.log_system.logar(f"⚠️ Mercado para o ativo {ativo} está FECHADO. Análise bloqueada.")
            return
        else:
            self.log_system.logar(f"✅ Mercado para o ativo {ativo} está ABERTO.")

        self.operando[index] = True
        self.status_labels[index].config(text="● OPERANDO", fg=self.colors['accent'])
        self.log_system.logar(
            f"✅ Ambiente OK. Iniciando análise no ativo {ativo}, timeframe {timeframe}, lote {lote_float}. Spread atual: {spread:.1f} pontos.",
            f"asset_{index}")
        
        # Create and store strategy instance
        self.estrategias[index] = EstrategiaTrading(ativo, timeframe, lote_float, self.log_system)
        threading.Thread(target=self.estrategias[index].executar, daemon=True).start()

    def parar_robo(self, index):
        self.operando[index] = False
        self.status_labels[index].config(text="⭘ AGUARDANDO", fg=self.colors['text_secondary'])
        if index in self.estrategias:
            self.estrategias[index].parar()
            del self.estrategias[index]
        self.log_system.logar(f"🛑 Análise parada para Ativo {index + 1}", f"asset_{index}")


    def on_closing(self):
        """Handle window closing"""
        if self.tem_ativos_operando():
            if messagebox.askokcancel("Sair", "Existem robôs em execução. Deseja realmente sair?"):
                # Stop all running strategies
                for index in range(self.max_assets):
                    if self.operando[index]:
                        self.parar_robo(index)
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PainelApp(root)
    root.mainloop()
