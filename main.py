from datetime import datetime
from tqdm import tqdm
from time import sleep
from src import get_stock_list, scraping_stock_price
from database_init import MariaDB
from database_init.query_generate import *
from log import logger

def set_stock_list():
    '''
    scraping stock_list from twse website
    '''
    table_name = "stock_list"
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
        stock_list = db.parse_stock_list()
        db.execute_query(create_query)
        for stock in tqdm(stock_list):
            logger.info(f"Scraping {stock}")
            df = scraping_stock_price(stock, start_date)
            if df is not None:
                db.insert_data(table_name, df)
            else:
                logger.warning(f"{stock} has no data")
                pass
            sleep(2)

    except Exception as e:
        logger.exception(e)

if __name__ == "__main__":
    scraping_stock()