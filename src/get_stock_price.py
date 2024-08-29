from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from . import logger

def scraping_stock_price(stock_id: str, start_date: datetime) -> pd.DataFrame:
    logger.debug(f"Scraping stock price for {stock_id}")
    try:
        stock = yf.Ticker(stock_id)
        df = stock.history(start=start_date, end=datetime.today(), interval='1d')
        if df is not None and len(df) > 0:
            df.reset_index(inplace=True)
            df['Date'] = pd.to_datetime(df['Date'].dt.strftime('%Y-%m-%d'))
            df['stock_id'] = stock_id.split('.')[0]
            return df
        else:
            return None
    
    except Exception as e:
        logger.exception(e)
        return None
    
def daily_scraping(stock_id:str, date:str) -> pd.DataFrame|None:
    start_date = datetime.strptime(date, '%Y-%m-%d')
    today = datetime.today()
    logger.info(f"Scraping stock price for {stock_id} on {today}")
    try:
        stock = yf.Ticker(stock_id)
        df = stock.history(start=start_date, end=start_date + timedelta(days=1), interval='1d')
        if df is not None and len(df) > 0:
            df.reset_index(inplace=True)
            df['Date'] = pd.to_datetime(df['Date'].dt.strftime('%Y-%m-%d'))
            df['stock_id'] = stock_id.split('.')[0]
            logger.info(f"Scraping stock price for {stock_id} on {today} success")
            return df
        else:
            logger.warning(f"No data found for {stock_id} on {today}")
            return None
    except Exception as e:
        logger.exception(e)
        return None
    
if __name__ == "__main__":
    stock_id = "036893.TW"
    df = daily_scraping(stock_id, '2023-05-01')
    print(df.head()) 