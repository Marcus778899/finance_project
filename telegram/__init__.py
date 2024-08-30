from log import logger
from .bot_init import bot
from .telegram_stock import *

@bot.message_handler(commands=['start'])
def command_hello(message):
    logger.info("receive hello command")
    msg = "Hello! I'm a bot\nPlease Submit '/help' to get user manual"
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['help'])
def command_help(message):
    logger.info("receive help command")
    msg = (
        "This is a help message\n\n"
        "/start : will send you Welcome message\n"
        "/help : will send you this message\n"
        "/stock : generate stock image"
    )
    bot.send_message(message.chat.id, msg)