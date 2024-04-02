import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import json

def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        print(f"args: {args} ,kwargs: {kwargs}")
        print(f"Returning \n{func(*args, **kwargs)}")
        print('=' * 50)
        return func(*args, **kwargs)
    return wrapper

def get_stock_list():
    stock_list = pd.read_csv('./stock_info.csv')
    stock_list = stock_list[0:3171]

    stock_list.set_index('stock_id', inplace=True)
    
    pattern = {
        'twse': 'TW',
        'tpex': 'TWO'
    }

    for key, value in pattern.items():
        stock_list['type'] = stock_list['type'].str.replace(key, value)

    dict_stock_list = [stock for stock in stock_list.index + '.' + stock_list['type']]

    return dict_stock_list

@debug
def scraping_stock_price(stock_id: str) -> pd.DataFrame:
    try:
        date = datetime.now().date()
        stock = yf.Ticker(stock_id)
        df = stock.history(start=datetime.now().date(), end=date + timedelta(days=1), interval='1d')
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'].dt.strftime('%Y-%m-%d'))
        df['stock_id'] = stock_id.split('.')[0]

        return df
    
    except Exception as e:
        print(e)
        print(f'Error scraping {stock_id}')
        return None

def company_finance_statement(stock_id: str) -> pd.DataFrame:
    stock = yf.Ticker(stock_id)
    df = stock.financials
    df = df.T
    df['Year'] = df.index.strftime('%Y')
    df['stock_id'] = stock_id.split('.')[0]
    df.reset_index(inplace=True)
    df.drop('index',axis=1, inplace=True)
    columns_to_convert = [col for col in df.columns if col not in ['Year', 'stock_id']]
    df[columns_to_convert] = df[columns_to_convert].astype('float16')

    def schema_write():
        config_path = Path('scraping_package/config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        schema_path = Path(config['schema_file_path'])

        type_of_data = df.dtypes
        schema = {}
        for index,types in type_of_data.items():
            schema[index] = types.name
        schema_df = pd.DataFrame(schema.items(), columns = ['column', 'data_type'])

        with pd.ExcelWriter(schema_path, engine='openpyxl', mode='a') as writer:
            schema_df.to_excel(writer, sheet_name='finance_statement', index=False)

        print(f'Finance statement schema write to {schema_path}')

    return df

@debug
def test():
    df = company_finance_statement('2330.TW')
    return df

if __name__ == '__main__':
    test()