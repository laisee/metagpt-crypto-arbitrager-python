import os
import ccxt
import logging
from dotenv import load_dotenv

load_dotenv()

class BinanceAPI:
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        self.exchange = ccxt.binance({
            'apiKey': self.api_key,
            'secret': self.api_secret,
        })

    def get_price(self) -> float:
        try:
            data = self.exchange.fetch_ticker('SOL/USDT')
            return float(data['last'])
        except ccxt.BaseError as e:
            logging.error(f'Error fetching price from Binance: {e}')
            return None

    def execute_trade(self, amount: float) -> None:
        try:
            order = self.exchange.create_market_buy_order('SOL/USDT', amount)
            logging.info(f'Trade executed on Binance: {order}')
        except ccxt.BaseError as e:
            logging.error(f'Error executing trade on Binance: {e}')
