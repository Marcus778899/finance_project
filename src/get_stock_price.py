from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from . import logger

def scraping_stock_price(stock_id: str, start_date: datetime) -> pd.DataFrame:
    try:
        logger.debug(f"Scraping stock price for {stock_id}")
        stock = yf.Ticker(stock_id)
        df = stock.history(start=start_date, end=datetime.today() + timedelta(days=1), interval='1d')
        if df is not None and len(df) > 0:
            df.reset_index(inplace=True)
            df['Date'] = pd.to_datetime(df['Date'].dt.strftime('%Y-%m-%d'))
            df['stock_id'] = stock_id.split('.')[0]
            return df
        else:
            logger.warning(f"No data found for {stock_id}")
            return None
    
    except Exception as e:
        logger.exception(e)
        return None
    
if __name__ == "__main__":
    stock_id = "0050.TW"
    start_date = datetime(2023, 1, 1)
    df = scraping_stock_price(stock_id, start_date)
    print(df)