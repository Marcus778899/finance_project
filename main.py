import time
from datetime import datetime, timedelta
from database_init import db
from src import get_stock_list, ScrapingStockPrice


def calculate_date():
    start = datetime(2021,4,7)
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
    action = ScrapingStockPrice()
    db.create_table("stock_price")
    time_list = calculate_date()
    for times in time_list:
        print(f"Now start scraping {times}")
        df = action.main(times)
        if df is None:
            continue
        else:
            db.insert_data("stock_price", df)
            print("NOW sleep for three minutes...")
            time.sleep(180)
        print("=" * 100)

if __name__ == "__main__":
    try:
        scraping_stock_price()
    finally:
        db.close_driver()