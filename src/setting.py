import os
import configparser
import logging
from datetime import datetime
from traceback import format_exc
import functools
import uuid
import json

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

WORKDIR = os.path.join(os.path.dirname(__file__), "..")

config_file = os.path.join(WORKDIR, "environment.cfg")
config = configparser.ConfigParser()
config.read(config_file)

DB_INFO = {
    "host": config.get('DB_Config', 'HOST'),
    "port": config.get('DB_Config', 'PORT'),
    "user": config.get('DB_Config', 'USERNAME'),
    "password": config.get('DB_Config', 'PASSWORD'),
    "database": config.get('DB_Config', 'DATABASE')
}

TELEGRAM_INFO = {
    "TOKEN": config.get("Telegram", "TOKEN")
}

SERVER_INFO = {
    "url": config.get("Server_URL", "URL"),
    'port': int(config.get("Server_URL","PORT"))
}

class LoggerHelper:
    def __init__(self):
        self.logger = logging.getLogger()

        logging.getLogger().addFilter(self.filter_process_guid) 
        logging.getLogger("uvicorn").addFilter(self.filter_process_guid)

        self.format = logging.Formatter(
            '(%(asctime)s)=> [%(process_guid)s][%(levelname)s] %(message)s',
            defaults={"process_guid": "N/A"} 
        )
        self.logger.setLevel(logging.INFO)
        self.process_guid = str(uuid.uuid4()).split('-')[0]
        self.save_path = f"{WORKDIR}/Logs"
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        self.save_daily = f"{self.save_path}/logs_{datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(self.save_daily):
            os.mkdir(self.save_daily)
        
        self.create_level_file_handlers()

        self.logger.addHandler(self.stream_handler())

    def create_level_file_handlers(self):
        levels = {
            logging.INFO: 'info',
            logging.WARNING: "warning",
            logging.ERROR: 'error',
            logging.CRITICAL: "critical"
        }
        for level, file_name in levels.items():
            self.file_handler(level, file_name)
        
    def file_handler(self, level, file_name):
        handler = logging.FileHandler(
            f"{self.save_daily}/{file_name}.log",
            encoding="utf-8",
            mode="a"
        )
        handler.setFormatter(self.format)
        handler.setLevel(level)
        
        handler.addFilter(lambda record: record.levelno == level)
        
        self.logger.addHandler(handler)

    def stream_handler(self):
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(self.format)
        return handler
    
    def filter_process_guid(self, record):
        if not hasattr(record, 'process_guid'):
            record.process_guid = self.process_guid
        return True


class LogMiddleware(BaseHTTPMiddleware):
    async def _aiter(self, body):
        for item in body:
            yield item

    async def dispatch(self, request: Request, call_next):
        domain = request.headers.get("host", "Unknown")
        url = str(request.url).split(domain)[-1]
        body = await request.body()
        try:
            body_text = body.decode('utf-8') 
            try:
                body_json = json.loads(body_text)  
                body_text = json.dumps(body_json)
            except json.JSONDecodeError:
                pass 
            send_info(f"{url}, Request=> {body_text}")
        except UnicodeDecodeError:  
            send_warn(f"{url}, Request body could not be decoded into UTF-8.")
            body_text = "[Non-text data, unable to decode]"

        response = await call_next(request)

        try:
            response_body = [section async for section in response.body_iterator]
            response.body_iterator = self._aiter(response_body)
            response_text = b"".join(response_body).decode()
            response_json = json.loads(response_text)
            status = response_json.get('status_code', None)
            return_content = json.dumps({"status": status})
        except (UnicodeDecodeError, json.JSONDecodeError):
            send_warn(f"{url}, Response body could not be decoded into UTF-8.")
            return_content = "{}"

        send_info(f"{url}, Response=> {return_content}")

        return response
    
logs = LoggerHelper()

def send_info(message: str):
    logs.logger.info(message)

def error_handle(func):
    @functools.wraps(func)
    def wrap(*args, **kwagrs):
        try:
            return func(*args, **kwagrs)
        except Exception as e:
            logs.logger.error(f"Error in func <{func.__name__}>\n{format_exc()}")
    return wrap

def send_warn(message: str):
    logs.logger.warning(message)