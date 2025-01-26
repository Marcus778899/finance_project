from telebot import TeleBot
from .. import send_info

def register_start_handler(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def command_start(message):
        bot.send_message(
            message.chat.id, 
            "Hello! I'm a bot\nType '/help' to get the user manual."
        )
        send_info("Received '/start' command")