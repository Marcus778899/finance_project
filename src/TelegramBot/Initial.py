from telebot import TeleBot

from ..setting import send_info, TELEGRAM_INFO

TOKEN = TELEGRAM_INFO['TOKEN']
bot = TeleBot(TOKEN, parse_mode=None)

from .response_image import *

def start_polling():
    send_info("Starting Telegram bot polling...")
    
    @bot.message_handler(commands=['start'])
    def command_start(message):
        bot.send_message(
            message.chat.id, 
            "Hello! I'm a bot\nType '/help' to get the user manual."
            )
        send_info("Received '/start' command")

    @bot.message_handler(commands=['help'])
    def command_help(message):
        bot.send_message(
            message.chat.id, 
            "This is the help message.\nAvailable commands:\n/start - Start the bot\n/help - Show this help message."
            )
        send_info("Received '/help' command")

    @bot.message_handler(commands=['stock'])
    def start_message(message):
        send_info('stock command')
        bot.send_message(message.chat.id, 'Please Enter stock code')
        bot.register_next_step_handler(message, request_stock)

    bot.polling(none_stop=True)
