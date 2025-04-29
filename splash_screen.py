import tkinter as tk
import threading
import time
import random


class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Future MT5 - Loading")

        # Modern color scheme
        self.colors = {
            'bg_dark': '#1a1a1a',
            'bg_medium': '#2d2d2d',
            'bg_light': '#363636',
            'accent': '#3498db',
            'accent_hover': '#2980b9',
            'success': '#2ecc71',
            'success_dark': '#27ae60',
            'text': '#ffffff',
            'text_secondary': '#b3b3b3'
        }

        # Configure main window
        self.root.configure(
            bg=self.colors['bg_dark'],
            highlightbackground=self.colors['success'],
            highlightcolor=self.colors['success'],
            highlightthickness=2
        )
        self.root.overrideredirect(True)
        self.centralizar_janela(450, 350)

        self.setup_ui()
        threading.Thread(target=self.simular_carregamento, daemon=True).start()

    def centralizar_janela(self, largura, altura):
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

    def create_gradient_frame(self, parent, color1, color2):
        frame = tk.Frame(parent, bg=color1, height=2)
        return frame

    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(expand=True, fill="both", padx=25, pady=25)

        # Top gradient
        gradient_top = self.create_gradient_frame(main_container, self.colors['success'], self.colors['bg_dark'])
        gradient_top.pack(fill="x", pady=(0, 20))

        # Logo and title section
        logo_label = tk.Label(
            main_container,
            text="🚀",
            font=("Helvetica", 48),
            bg=self.colors['bg_dark'],
            fg=self.colors['success']
        )
        logo_label.pack(pady=(0, 10))

        title_label = tk.Label(
            main_container,
            text="Future MT5",
            font=("Helvetica", 28, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['text']
        )
        title_label.pack()

        subtitle_label = tk.Label(
            main_container,
            text="Trading Platform",
            font=("Helvetica", 12),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack()

        # Message label with modern styling
        self.label_mensagem = tk.Label(
            main_container,
            text="Initializing...",
            font=("Helvetica", 11),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_secondary']
        )
        self.label_mensagem.pack(pady=(30, 15))

        # Modern progress bar container
        self.progress_container = tk.Frame(
            main_container,
            bg=self.colors['bg_medium'],
            height=6
        )
        self.progress_container.pack(fill="x", padx=30)

        # Progress bar with rounded corners effect
        self.progress_bar = tk.Frame(
            self.progress_container,
            bg=self.colors['success'],
            width=0,
            height=6
        )
        self.progress_bar.pack(side="left")

        # Bottom gradient
        gradient_bottom = self.create_gradient_frame(main_container, self.colors['bg_dark'], self.colors['success'])
        gradient_bottom.pack(fill="x", pady=(20, 0))

    def simular_carregamento(self):
        progresso = 0
        mensagens = [
            "Initializing modules...",
            "Connecting to MetaTrader 5...",
            "Loading Future MT5 robot...",
            "Preparing market analysis...",
            "Warming up trading engines...",
            "Finalizing startup...",
            "Almost there..."
        ]

        # Smooth progress animation
        while progresso <= 100:
            if not self.root.winfo_exists():
                return

            # Smooth progress bar animation
            self.progress_bar.config(width=int((self.root.winfo_width() - 60) * (progresso / 100)))

            # Update message periodically
            if progresso % 15 == 0:
                new_message = random.choice(mensagens)
                self.label_mensagem.config(text=new_message)

            # Slower at start and end for better effect
            if progresso < 20:
                delay = 0.1
            elif progresso > 80:
                delay = 0.08
            else:
                delay = 0.05

            progresso += 1
            time.sleep(delay)

        # Ensure we show 100% before transitioning
        self.progress_bar.config(width=self.root.winfo_width() - 60)
        time.sleep(0.5)

        if self.root.winfo_exists():
            self.root.after(100, self.abrir_login)

    def abrir_login(self):
        from login import LoginApp
        # Smooth fade out effect
        for alpha in range(100, -1, -5):
            if self.root.winfo_exists():
                self.root.attributes('-alpha', alpha / 100)
                self.root.update()
                time.sleep(0.01)

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.overrideredirect(False)
        self.root.title("Future MT5 - Login")
        self.root.geometry("400x600")
        self.root.configure(bg=self.colors['bg_dark'])
        self.root.attributes('-alpha', 1.0)  # Reset transparency
        LoginApp(self.root)


def exibir_splash():
    root = tk.Tk()
    app = SplashScreen(root)
    root.mainloop()


if __name__ == "__main__":
    exibir_splash()