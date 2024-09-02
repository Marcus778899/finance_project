import os
import pandas as pd
module_path = os.path.join(
    os.path.dirname(__file__),
    '../..'
)
os.chdir(module_path)

from database_init import MariaDB
from database_init.query_generate import select_data_query

def ETF_0050():
    '''
    Only slice Close price
    '''
    query_0050 = select_data_query(
        "stock_price",
        "stock_id ='0050' ORDER BY Date DESC LIMIT 500"
        )
    df = MariaDB().export_data(query_0050)
    df.set_index(pd.DatetimeIndex(df['Date']), inplace=True)
    df.sort_index(inplace=True)
    df = pd.DataFrame(df['Close'], columns=['Close'])
    return df

def stock_2330():
    '''
    Only slice Close price
    '''
    query_0050 = select_data_query(
        "stock_price",
        "stock_id ='2330' ORDER BY Date DESC LIMIT 500"
        )
    df = MariaDB().export_data(query_0050)
    df.set_index(pd.DatetimeIndex(df['Date']), inplace=True)
    df.sort_index(inplace=True)
    df = pd.DataFrame(df['Close'], columns=['Close'])
    return df