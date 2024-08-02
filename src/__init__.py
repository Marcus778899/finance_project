import logging
from database_init import stock_list
from . import get_stock_list
from .get_stock_price import scraping as scraping_stock_a_day

logging.basicConfig(level=logging.INFO)