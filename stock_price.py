'''
scraping program
'''
import sys
from datetime import datetime
from tqdm import tqdm
from scraping_package import stock_list_with_suffix,scraping_stock_price
from database_package import mysql_action

sql = mysql_action
def main(date: datetime):
    stock_list = stock_list_with_suffix()
    def stock_price(stock_id: str):
        table_name = 'stock_price'
        result = scraping_stock_price(stock_id,date)
        if result is not None:
            try:
                query = sql.insert_data(table_name, result)
                sql.execute_query(query)
                print(f'{stock_id} is Done')
            except Exception as e:
                print(e)
                print(stock_id)
        print('=' * 50)

    progress = tqdm(total= len(stock_list), desc= 'Progress')
    for stock_id in stock_list:
        stock_price(stock_id)
        progress.update(1)

if __name__ == '__main__':
    today = sys.argv[1]
    today = datetime.strptime(today, "%a %b %d %H:%M:%S %Z %Y").date()
    main(today)

    sql.close_driver()