import logging
from .mariadb_config import MariaDB

logging.basicConfig(level=logging.INFO)

db = MariaDB()
stock_list = db.parse_stock_list()