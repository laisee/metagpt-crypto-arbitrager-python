## trader.py
import os
import logging
from dotenv import load_dotenv
from binance_api import BinanceAPI
from bitfinex_api import BitfinexAPI
from notifier import Notifier

load_dotenv()

class Trader:
    def __init__(self):
        self.binance = BinanceAPI()
        self.bitfinex = BitfinexAPI()
        self.notifier = Notifier()
        self.threshold = float(os.getenv('PRICE_DIFF_THRESHOLD', 0.01))

    def monitor_prices(self) -> None:
        binance_price = self.binance.get_price()
        bitfinex_price = self.bitfinex.get_price()

        if binance_price is None or bitfinex_price is None:
            logging.error('Error fetching prices.')
            return

        price_difference = abs(binance_price - bitfinex_price)

        if price_difference > self.threshold:
            logging.info(f'Price difference detected: {price_difference}')
            self.execute_arbitrage_trade(binance_price, bitfinex_price)

    def execute_arbitrage_trade(self, binance_price: float, bitfinex_price: float) -> None:
        trade_amount = float(os.getenv('TRADE_AMOUNT', 1.0))

        if binance_price > bitfinex_price:
            self.binance.execute_trade(trade_amount)
            self.bitfinex.execute_trade(trade_amount)
        else:
            self.bitfinex.execute_trade(trade_amount)
            self.binance.execute_trade(trade_amount)

        self.notifier.send_notification('Trade executed')
