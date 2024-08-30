from io import BytesIO
from . import logger
from .bot_init import bot
import requests

request_body = {}

@bot.message_handler(commands=['stock'])
def start_message(message):
    logger.info('stock command')
    bot.send_message(message.chat.id, 'Please Enter stock code')
    bot.register_next_step_handler(message, request_stock)

def request_stock(message):
    chat_id = message.chat.id
    request_body['stock_id'] = message.text
    bot.send_message(chat_id, 'Please Enter data length (<=500)')
    bot.register_next_step_handler(message, request_length)

def request_length(message):
    chat_id = message.chat.id
    request_body['limit'] = message.text
    bot.send_message(chat_id, 'Please Enter Condition (or enter N)')
    bot.register_next_step_handler(message, generate_image)

def generate_image(message):
    
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Please wait...')

    condition = message.text.upper()

    if condition == 'N':
        pass
    else:
        request_body['condition'] = condition

    logger.info(f"parameter: {request_body}")
    bot.send_message(chat_id, 'Please wait...')
    try:
        url = "http://localhost:5001/image"
        response = requests.post(url, params=request_body)
        if response.status_code == 200:
            image = BytesIO(response.content)
            bot.send_photo(chat_id, image)
            logger.info(f"{request_body['stock_id']} image sent!!")
            image.close()
        else:
            logger.error(f"Error: {response.status_code}")
            bot.send_message(chat_id, 'Error: ' + str(response.status_code))
    except Exception as e:
        logger.exception(e)
        bot.send_message(chat_id, 'Error: ' + str(e))