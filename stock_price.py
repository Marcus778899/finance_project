from scraping_package import get_stock_list,scraping_stock_price
from database_package import mysql_action
from tqdm import tqdm

sql = mysql_action
def main():
    stock_list = get_stock_list()
    def stock_price(stock_id: str):
        table_name = 'stock_price'
        result = scraping_stock_price(stock_id)
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
    # drop_query = sql.drop_table(table_name)
    # create_query = sql.create_table(table_name)
    # sql.execute_query(drop_query)
    # sql.execute_query(create_query)

    main()

    sql.close_driver()