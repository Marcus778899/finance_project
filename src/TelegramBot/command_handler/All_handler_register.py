from telebot import TeleBot
from .start_handler import register_start_handler
from .help_handler import register_help_handler
from .stock_handler import register_stock_handler

def register_all_handlers(bot: TeleBot):
    register_start_handler(bot)
    register_help_handler(bot)
    register_stock_handler(bot)