from datetime import datetime
from tqdm import tqdm
from time import sleep
from src import get_stock_list, scraping_stock_price, daily_scraping
from database_init import MariaDB, yfinance_stock_list
from database_init.query_generate import *
from log import logger

def set_stock_list():
    '''
    scraping stock_list from twse website
    '''
    table_name = "basic_info"
    df = get_stock_list.main()
    create_query = create_table_query(table_name)
    db = MariaDB()
    try:
        db.execute_query(create_query)
        db.insert_data(table_name, df)
    except Exception as e:
        logger.exception(e)
        raise e
    
def scraping_stock():
    '''
    scraping stock price from yfinance
    '''
    table_name = "stock_price"
    create_query = create_table_query(table_name)
    db = MariaDB()
    start_date = datetime(2017,1,1)
    try:
        stock_list = db.parse_basic_info()
        db.execute_query(create_query)
        for stock in tqdm(stock_list):
            logger.info(f"Scraping {stock}")
            df = scraping_stock_price(stock, start_date)
            if df is not None:
                db.insert_data(table_name, df)
            else:
                logger.warning(f"{stock} has no data")
                pass

    except Exception as e:
        logger.exception(e)

def missing_fill(time: str):
    logger.info(f"filling missing data at {time}")
    table_name = "stock_price"
    db = MariaDB()
    try:
        stock_list = yfinance_stock_list()
        for stock in tqdm(stock_list):
            logger.info(f"Scraping {stock}")
            df = daily_scraping(stock, time)
            if df is not None:
                db.insert_data(table_name, df)
            else:
                logger.warning(f"{stock} has no data")
                pass

    except Exception as e:
        logger.exception(e)

if __name__ == "__main__":
    missing_fill("2024-08-28")