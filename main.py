from scraping_package import stock_scraping
from database_package import mysql_action
from concurrent.futures import ThreadPoolExecutor

sql = mysql_action
scarping = stock_scraping
def main():
    stock_list = stock_scraping.get_stock_list()
    def action(stock_id: str):
        result = scarping.scraping_stock_price(stock_id)
        if result is not None:
            try:
                query = sql.insert_data(table_name, result)
                sql.execute_query(query)
                print(f'{stock_id} is Done')
            except Exception as e:
                print(e)
                print(stock_id)
        print('=' * 50)

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(action, stock_list)
        executor.shutdown(wait=True)

if __name__ == '__main__':
    table_name = 'stock_price'
    drop_query = sql.drop_table(table_name)
    create_query = sql.create_table(table_name)
    sql.execute_query(drop_query)
    sql.execute_query(create_query)

    main()

    sql.close_driver()