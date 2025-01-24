import requests
from io import BytesIO

from .Initial import bot
from ..setting import send_info, error_handle, send_warn, SERVER_INFO

request_body = {}

@error_handle
def request_stock(message):
    chat_id = message.chat.id
    request_body['stock_id'] = message.text
    bot.send_message(chat_id, 'Please Enter data length (<=500)')
    bot.register_next_step_handler(message, request_length)

@error_handle
def request_length(message):
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