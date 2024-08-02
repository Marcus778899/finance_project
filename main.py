from datetime import datetime, timedelta
import time
from database_init import db
from src import get_stock_list, scraping_stock_a_day


def calculate_date():
    start = datetime(2020,1,1)
    end = datetime.now() - timedelta(days=1)
    time_list = []
    while start <= end:
        time_list.append(start)
        start += timedelta(days=1)
    return time_list

def scarping_stock_list():
    db.create_table("stock_list")
    stock_list = get_stock_list.main()
    db.insert_data("stock_list", stock_list)

def scraping_stock_price():
    db.create_table("stock_price")
    time_list = calculate_date()
    for times in time_list:
        df = scraping_stock_a_day(times)
        db.insert_data("stock_price", df)
        print("NOW sleep for ten seconds...")
        time.sleep(10)

if __name__ == "__main__":
    scraping_stock_price()
    db.close_driver()