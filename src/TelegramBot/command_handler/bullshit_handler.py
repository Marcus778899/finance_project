from telebot import TeleBot
import requests

from .. import send_info, SERVER_INFO, send_warn

request_body = {}

def register_bullshit_handler(bot: TeleBot):
    @bot.message_handler(commands=['bullshit'])
    def start_message(message):
        send_info("Recieved bullshit command")
        bot.send_message(message.chat.id, "Please enter a topic")
        bot.register_next_step_handler(message, enter_length)

    def enter_length(message):
        chat_id = message.chat.id
        topic = message.text
        send_info(f"Customer enter {topic}")
        request_body['topic'] = topic
        bot.send_message(chat_id,"Please enter content length")
        bot.register_next_step_handler(message, generate_content)

    def generate_content(message):
        chat_id = message.chat.id

        request_body['content_length'] = int(message.text)
        send_info(f"Revecive content length {request_body['content_length']}")
        
        url = f"http://{SERVER_INFO['url']}:{SERVER_INFO['port']}/bullshit"
        try:
            response = requests.post(url, json=request_body).json()
            if response['status_code'] == 200:
                send_info("Status Code is normal")
                response_content = response["content"]
                bot.send_message(chat_id, response_content)
            else:
                send_warn("Status code Error")
                bot.send_message(chat_id, f"Error: {str(response['status_code'])}")
        
        except Exception as e:
            send_warn(f"Unexcept Error occured {str(e)}")    