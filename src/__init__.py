import logging
from database_init import stock_list
from . import get_stock_list
from .get_stock_price import ScrapingStockPrice

logging.basicConfig(level=logging.INFO)