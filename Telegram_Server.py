import time
from urllib3.exceptions import ProtocolError
from requests.exceptions import ConnectionError, ReadTimeout
from telegram import logger, bot

def start_bot():
    retry_count = 0
    max_retires = 5

    while True:
        try:
            logger.info("Bot is running...")
            bot.enable_save_next_step_handlers(delay=2)
            bot.load_next_step_handlers()
            bot.infinity_polling(timeout=60,long_polling_timeout=60)
        except (ReadTimeout, ConnectionError, ProtocolError) as e:
            logger.error(f"Connect Error: {e}")
            retry_count += 1
            if retry_count > max_retires:
                logger.error("Max retries reached. Exiting...")
                break
            sleep_time = min(2 ** retry_count, 60)
            logger.info(f"Retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)
        except Exception as e:
            logger.error(f"Unexcepted Error: {e}")
            time.sleep(5)
        else:
            retry_count = 0

if __name__ == '__main__':
    start_bot()