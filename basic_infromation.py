'''
main for basic information
'''
from time import sleep
from tqdm import tqdm
import pandas as pd
from scraping_package import BasicInformation
from scraping_package.stock_scraping import stock_list_for_basic_information
from database_package import mysql_action

def column_select(df: pd.DataFrame) -> pd.DataFrame:
    '''
    All the data type is object
    '''
    column_list =[ 
        '股票代號',
        '股票名稱',
        '產業別',
        '上市/上櫃',
        '上市日期', 
        '上櫃日期', 
        '資本額', 
        '每股面值', 
        '目前市值',
        '公司債發行',
        '發行股數',
        '特別股',
        '盈餘分派頻率',
        '董事長'
        ]
    df = df[column_list].set_index('股票代號').reset_index()
    return df

if __name__ == '__main__':
    stock_list = stock_list_for_basic_information()
    progress_bar = tqdm(total=len(stock_list.items()), desc='progess')
    seen_value = set()
    sql_action = mysql_action
    sql_action.execute_query(sql_action.create_table('basic_information'))
    for index, value in stock_list.items():

        progress_bar.update(1)
        if index in seen_value:
            continue

        action = BasicInformation('BasicInfo', index)
        basic_information = action.get_data()

        if basic_information is None:
            print(f'{value} {index} is not exist')
            print('=' * 100)
            continue

        seen_value.add(index)
        df = pd.DataFrame(basic_information, index=[index])
        df = column_select(df)
        query = sql_action.insert_data('basic_information', df)
        print(query)
        sql_action.execute_query(query)
        sql_action.conn.commit()
        print('=' * 100)
        sleep(5)
    sql_action.close_driver()