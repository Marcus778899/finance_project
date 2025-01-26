import time

from urllib3.exceptions import ProtocolError
from requests.exceptions import ConnectionError, ReadTimeout
from telebot import TeleBot

from . import send_info, TELEGRAM_INFO, send_warn, error_handle
from .command_handler import register_all_handlers

TOKEN = TELEGRAM_INFO['TOKEN']
bot = TeleBot(TOKEN, parse_mode=None)

@error_handle
def start_polling():
    send_info("Starting Telegram bot polling...")

    retires_count = 0
    max_retires = 5

    while True:
        try:
            send_info("Bot is running")
            register_all_handlers(bot)
            bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    
        except (ConnectionError, ReadTimeout, ProtocolError) as e:
            send_warn(f"Connect Error: {e}")
            retires_count += 1
            if retires_count > max_retires:
                send_warn("Max retries reached. Exiting polling...")
                break
            sleep_time = min(2 ** retires_count, 60)
            send_info(f"Retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)
        
        except Exception as e:
            send_info(f"Unexpected Error: {e}")
            time.sleep(5)
        
        else:
            retires_count = 0