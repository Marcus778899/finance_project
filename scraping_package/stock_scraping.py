import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        print(f"args: {args} ,kwargs: {kwargs}")
        print(f"Returning \n{func(*args, **kwargs)}")
        print('=' * 50)
        return func(*args, **kwargs)
    return wrapper
        
@debug
def scraping_stock_price(stock_id: str, date: str) -> pd.DataFrame:
    try:
        today = datetime.strptime(date, "%a %b %d %H:%M:%S %Z %Y").date()
        stock = yf.Ticker(stock_id)
        df = stock.history(start=today, end=today + timedelta(days=1), interval='1d')
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'].dt.strftime('%Y-%m-%d'))
        df['stock_id'] = stock_id.split('.')[0]

        return df
    
    except Exception as e:
        print(e)
        print(f'Error scraping {stock_id}')
        return None


