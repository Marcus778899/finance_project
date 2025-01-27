from telebot import TeleBot
from .. import send_info

def register_help_handler(bot: TeleBot):
    @bot.message_handler(commands=['help'])
    def command_help(message):
        help_content=f"""
This is the help message.
Available commands:\n
/start - Start the bot
/help - Show this help message.
/stock - For display stock price image 
/bullshit - healthy for your soul      
"""
        bot.send_message(
            message.chat.id, 
            help_content
        )
        send_info("Received '/help' command")
