import sys
from log import logger
from database_init import MariaDB, yfinance_stock_list
from src import daily_scraping

excution_date = sys.argv[1]

db = MariaDB()
stock_list = yfinance_stock_list()

for stock in stock_list:
    df = daily_scraping(stock, excution_date)
    if df is None:
        continue
    db.insert_data("stock_price", df)

logger.info(f"Daily Scraping Complete : {excution_date}")