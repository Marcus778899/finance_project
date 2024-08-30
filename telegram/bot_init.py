from configparser import ConfigParser
import os
from telebot import TeleBot
from . import logger

config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'TelegramInfo.cfg'))
if config:
    TOKEN = config.get('Telegram', 'TOKEN')

bot = TeleBot(TOKEN, parse_mode=None)

logger.info("Telegram bot initialized")