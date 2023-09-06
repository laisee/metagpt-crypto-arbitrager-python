import os
import ccxt
import logging
from dotenv import load_dotenv

load_dotenv()

class BitfinexAPI:
    def __init__(self):
        self.api_key = os.getenv('BITFINEX_API_KEY')
        self.api_secret = os.getenv('BITFINEX_API_SECRET')
        self.exchange = ccxt.bitfinex({
            'apiKey': self.api_key,
            'secret': self.api_secret,
        })

    def get_price(self) -> float:
        try:
            data = self.exchange.fetch_ticker('SOL/USD')
            return float(data['last'])
        except ccxt.BaseError as e:
            logging.error(f'Error fetching price from Bitfinex: {e}')
            return None

    def execute_trade(self, amount: float) -> dict:
        try:
            order = self.exchange.create_market_buy_order('SOL/USD', amount)
            logging.info(f'Trade executed on Bitfinex: {order}')
            return {'status': 'success', 'order': order}
        except ccxt.BaseError as e:
            logging.error(f'Error executing trade on Bitfinex: {e}')
            return {'status': 'error', 'message': str(e)}
