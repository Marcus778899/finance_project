import pandas as pd
from .mariadb_config import MariaDB
from .query_generate import create_table_query

def setting_stock_list():
    db = MariaDB()
    all_item = MariaDB().parse_basic_info()

    query = f"SELECT DISTINCT stock_id from stock_price;"
    result = set(db.export_data(query)['stock_id'])

    table_name = "stock_list"
    create_query = create_table_query(table_name)
    db.execute_query(create_query)

    yfinance_list = [item for item in all_item if item.split('.')[0] in result]
    yfinance_df = pd.DataFrame(yfinance_list, columns=['stock_id'])
    db.insert_data(table_name, yfinance_df)

def yfinance_stock_list():
    db = MariaDB()
    query = f"SELECT stock_id from stock_list;"
    result = db.export_data(query)['stock_id'].tolist()
    return result    

if __name__ == "__main__":
    setting_stock_list()
