from io import BytesIO

from telebot import TeleBot
import requests

from .. import error_handle, send_info, SERVER_INFO, send_warn

request_body = {}

def register_stock_handler(bot: TeleBot):
    @bot.message_handler(commands=['stock'])
    def start_message(message):
        send_info('Received /stock command')
        bot.send_message(message.chat.id, 'Please Enter stock code')
        bot.register_next_step_handler(message, request_stock)


    @error_handle
    def request_stock(message):
        send_info("Reveive stock code")
        chat_id = message.chat.id
        request_body['stock_id'] = message.text
        bot.send_message(chat_id, 'Please Enter data length (<=500)')
        bot.register_next_step_handler(message, request_length)

    @error_handle
    def request_length(message):
        send_info("Reveive data length")
        chat_id = message.chat.id
        request_body['limit'] = message.text
        bot.send_message(chat_id, 'Please Enter Condition (or enter N)')
        bot.register_next_step_handler(message, generate_image)

    @error_handle
    def generate_image(message):
        
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Please wait...')

        condition = message.text.upper()

        if condition == 'N':
            pass
        else:
            request_body['condition'] = condition

        send_info(f"parameter: {request_body}")
        bot.send_message(chat_id, 'Please wait...')

        url = f"http://{SERVER_INFO['url']}:{SERVER_INFO['port']}/image"
        response = requests.post(url, params=request_body)
        if response.status_code == 200:
            image = BytesIO(response.content)
            bot.send_photo(chat_id, image)
            send_info(f"{request_body['stock_id']} image sent!!")
            image.close()
        else:
            send_warn(f"Error: {response.status_code}")
            bot.send_message(chat_id, 'Error: ' + str(response.status_code))
