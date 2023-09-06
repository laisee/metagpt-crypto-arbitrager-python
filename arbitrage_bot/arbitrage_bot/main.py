## main.py
import os
import logging
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from trader import Trader

load_dotenv()

def start_bot():
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting bot...')
    
    trader = Trader()
    scheduler = BlockingScheduler()
    
    check_interval = int(os.getenv('CHECK_INTERVAL', 10))
    scheduler.add_job(trader.monitor_prices, 'interval', seconds=check_interval)
    
    logging.info(f'Scheduled bot to monitor prices every {check_interval} seconds.')
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info('Stopping bot...')

if __name__ == "__main__":
    start_bot()
