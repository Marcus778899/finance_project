import pandas as pd
from typing import Set

def read_stock_info() -> pd.DataFrame:
    '''
    read stock_list.csv
    '''
    df = pd.read_csv('./stock_info.csv')
    df = df[0:3171]

    df.set_index('stock_id', inplace=True)

    return df

def stock_list_with_suffix() -> Set:
    '''
    clean repeat stock_id
    '''
    stock_list = read_stock_info()
    
    pattern = {
        'twse': 'TW',
        'tpex': 'TWO'
    }

    for key, value in pattern.items():
        stock_list['type'] = stock_list['type'].str.replace(key, value)

    dict_stock_list = {stock for stock in stock_list.index + '.' + stock_list['type']}

    return dict_stock_list

def stock_list_without_suffix() -> dict:
    '''
    clean repeat stock_id
    '''
    stock_list = read_stock_info()

    output_dict = {}
    for index, row in stock_list.iterrows():
        output_dict[index] = row['industry_category']

    exclude_type = ['ETF','上櫃指數股票型基金(ETF)','指數投資證券(ETN)','受益證券','ETN']
    key_to_remove = []
    for key, value in output_dict.items():
        if value in exclude_type:
            key_to_remove.append(key)

    for key in key_to_remove:
        output_dict.pop(key)

    return output_dict