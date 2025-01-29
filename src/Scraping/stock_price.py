from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from ..setting import send_info, error_handle,send_warn

@error_handle
def scraping_stock_price(stock_id: str, start_date: datetime) -> pd.DataFrame:
    send_info(f"Scraping stock price for {stock_id}")
    stock = yf.Ticker(stock_id)
    df = stock.history(start=start_date, end=datetime.today(), interval='1d')
    if df is not None and len(df) > 0:
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'].dt.strftime('%Y-%m-%d'))
        df['stock_id'] = stock_id.split('.')[0]
        return df
    else:
        return None
    
@error_handle
def daily_scraping(stock_id:str, date:str) -> pd.DataFrame|None:
    date_only = date.split('T')[0]
    start_date = datetime.strptime(date_only, '%Y-%m-%d')
    send_info(f"Scraping stock price for {stock_id} on {start_date}")
    stock = yf.Ticker(stock_id)
    df = stock.history(start=start_date, end=start_date + timedelta(days=1), interval='1d')
    if df is not None and len(df) > 0:
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'].dt.strftime('%Y-%m-%d'))
        df['stock_id'] = stock_id.split('.')[0]
        return df
    else:
        send_warn(f"No data found for {stock_id} on {start_date}")
        return None