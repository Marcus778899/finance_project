import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from typing import Iterator

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
        df = stock.history(start=date - timedelta(days=1), end=date + timedelta(days=1), interval='1d')
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'].dt.strftime('%Y-%m-%d'))
        df['stock_id'] = stock_id.split('.')[0]

        return df
    
    except Exception as e:
        print(e)
        print(f'Error scraping {stock_id}')
        return None
    
def main() -> Iterator[pd.DataFrame]:
    stock_list = get_stock_list() 

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(scraping_stock_price, stock_list)

    return results

def test():
    scraping_stock_price('2330.TW')
    print('TSMC scraping Done')