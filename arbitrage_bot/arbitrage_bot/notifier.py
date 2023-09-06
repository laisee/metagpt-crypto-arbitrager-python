## notifier.py
import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

class Notifier:
    def __init__(self):
        self.webhook_url = os.getenv('WEBHOOK_URL')

    def send_notification(self, message: str) -> None:
        data = {
            'text': message,
        }

        try:
            response = requests.post(self.webhook_url, json=data)
            response.raise_for_status()
            logging.info(f'Notification sent: {message}')
        except requests.exceptions.RequestException as e:
            logging.error(f'Error sending notification: {e}')
