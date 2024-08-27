import os
from datetime import datetime
import logging

save_file = os.path.join(
    os.path.dirname(__file__),
    'logs', 
    f'{datetime.now().strftime("%Y%m%d")}.log'
)
logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
                    filename=save_file,
                    encoding='utf-8',
                    mode='a'
                )
file_handler.setLevel(logging.WARN)
file_handler.setFormatter(logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s'))

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s'))

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
