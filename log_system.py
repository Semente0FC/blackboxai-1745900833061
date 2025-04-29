import time
from datetime import datetime
import tkinter as tk

class LogSystem:
    def __init__(self):
        self.log_widgets = {}  # Dictionary to store text widgets for each asset
        self.colors = {
            'success': '#2ecc71',
            'warning': '#f1c40f',
            'error': '#e74c3c',
            'info': '#3498db',
            'default': '#ecf0f1'
        }

    def add_log_widget(self, asset, text_widget):
        """Add a text widget for a specific asset"""
        self.log_widgets[asset] = text_widget
        self.log_widgets[asset].tag_configure('success', foreground=self.colors['success'])
        self.log_widgets[asset].tag_configure('warning', foreground=self.colors['warning'])
        self.log_widgets[asset].tag_configure('error', foreground=self.colors['error'])
        self.log_widgets[asset].tag_configure('info', foreground=self.colors['info'])
        self.log_widgets[asset].tag_configure('default', foreground=self.colors['default'])

    def remove_log_widget(self, asset):
        """Remove a text widget for a specific asset"""
        if asset in self.log_widgets:
            del self.log_widgets[asset]

    def clear_log_widgets(self):
        """Clear all log widgets"""
        self.log_widgets.clear()

    def get_message_type(self, mensagem):
        """Determine message type based on content"""
        if any(symbol in mensagem for symbol in ['✅', 'SUCESSO']):
            return 'success'
        elif any(symbol in mensagem for symbol in ['⚠️', 'AVISO']):
            return 'warning'
        elif any(symbol in mensagem for symbol in ['❌', 'ERRO']):
            return 'error'
        elif any(symbol in mensagem for symbol in ['ℹ️', 'INFO']):
            return 'info'
        return 'default'

    def logar(self, mensagem, asset=None):
        """Log a message to a specific asset's widget or all widgets if asset is None"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        msg_type = self.get_message_type(mensagem)
        texto_final = f"[{timestamp}] {mensagem}\n"

        if asset and asset in self.log_widgets:
            # Log to specific asset widget
            widget = self.log_widgets[asset]
            widget.insert('end', texto_final, msg_type)
            widget.see('end')
            
            # Limit log size to prevent memory issues
            if float(widget.index('end')) > 1000:  # Keep last 1000 lines
                widget.delete('1.0', '500.0')
        elif not asset:
            # Log to all widgets if no specific asset
            for widget in self.log_widgets.values():
                widget.insert('end', texto_final, msg_type)
                widget.see('end')
                
                # Limit log size
                if float(widget.index('end')) > 1000:
                    widget.delete('1.0', '500.0')

    def clear_logs(self, asset=None):
        """Clear logs for a specific asset or all assets"""
        if asset and asset in self.log_widgets:
            self.log_widgets[asset].delete('1.0', 'end')
        elif not asset:
            for widget in self.log_widgets.values():
                widget.delete('1.0', 'end')
