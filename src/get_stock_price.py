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
    
if __name__ == "__main__":
    stock_id = "036893.TW"
    start_date = datetime(2023, 1, 1)
    df = scraping_stock_price(stock_id, start_date)
    print(df.head()) 