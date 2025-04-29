import json
import os
import MetaTrader5 as mt5
from datetime import datetime
import threading
import time

CAMINHO_LOGIN_SALVO = "login_salvo.json"

class AssetManager:
    def __init__(self):
        self._assets_status = {}
        self._lock = threading.Lock()
        self._monitoring = False
        self._monitor_thread = None

    def start_monitoring(self):
        """Start monitoring asset status"""
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_assets, daemon=True)
        self._monitor_thread.start()

    def stop_monitoring(self):
        """Stop monitoring asset status"""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join()

    def _monitor_assets(self):
        """Monitor assets status in background"""
        while self._monitoring:
            for asset in list(self._assets_status.keys()):
                self.update_asset_status(asset)
            time.sleep(1)  # Update every second

    def update_asset_status(self, asset):
        """Update status for a specific asset"""
        with self._lock:
            try:
                tick = mt5.symbol_info_tick(asset)
                info = mt5.symbol_info(asset)
                
                if tick is None or info is None:
                    self._assets_status[asset] = {
                        'status': 'error',
                        'message': 'Unable to get market data',
                        'last_update': datetime.now(),
                        'spread': None,
                        'bid': None,
                        'ask': None,
                        'trading_allowed': False
                    }
                    return

                spread = (tick.ask - tick.bid) / info.point
                self._assets_status[asset] = {
                    'status': 'active' if info.trade_mode == mt5.SYMBOL_TRADE_MODE_FULL else 'restricted',
                    'message': 'Trading available' if info.trade_mode == mt5.SYMBOL_TRADE_MODE_FULL else 'Trading restricted',
                    'last_update': datetime.now(),
                    'spread': spread,
                    'bid': tick.bid,
                    'ask': tick.ask,
                    'trading_allowed': info.trade_mode == mt5.SYMBOL_TRADE_MODE_FULL
                }
            except Exception as e:
                self._assets_status[asset] = {
                    'status': 'error',
                    'message': str(e),
                    'last_update': datetime.now(),
                    'spread': None,
                    'bid': None,
                    'ask': None,
                    'trading_allowed': False
                }

    def get_asset_status(self, asset):
        """Get current status for an asset"""
        with self._lock:
            return self._assets_status.get(asset, {
                'status': 'unknown',
                'message': 'Asset not monitored',
                'last_update': None,
                'spread': None,
                'bid': None,
                'ask': None,
                'trading_allowed': False
            })

    def add_asset(self, asset):
        """Add asset to monitoring"""
        with self._lock:
            if asset not in self._assets_status:
                self._assets_status[asset] = {
                    'status': 'initializing',
                    'message': 'Initializing monitoring',
                    'last_update': datetime.now(),
                    'spread': None,
                    'bid': None,
                    'ask': None,
                    'trading_allowed': False
                }
                self.update_asset_status(asset)

    def remove_asset(self, asset):
        """Remove asset from monitoring"""
        with self._lock:
            if asset in self._assets_status:
                del self._assets_status[asset]

# Utility functions
def salvar_login(server, login, password):
    dados = {
        "server": server,
        "login": login,
        "password": password
    }
    with open(CAMINHO_LOGIN_SALVO, "w") as f:
        json.dump(dados, f)

def carregar_login():
    if os.path.exists(CAMINHO_LOGIN_SALVO):
        with open(CAMINHO_LOGIN_SALVO, "r") as f:
            return json.load(f)
    return None

def conectar_mt5(server, login, password):
    if not mt5.initialize(server=server, login=int(login), password=password):
        return False
    return True

def verificar_conta_real():
    info = mt5.account_info()
    if info is None:
        return False
    return info.trade_mode == 0  # 0 = Conta Real

def obter_saldo():
    conta = mt5.account_info()
    if conta:
        return conta.balance
    return 0.0

# Create global asset manager instance
asset_manager = AssetManager()
