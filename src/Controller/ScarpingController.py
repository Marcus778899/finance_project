from time import sleep
from datetime import datetime

from fastapi import APIRouter, HTTPException,status, Response
from ..setting import send_warn
from ..Database import sql_client
from ..Scraping import daily_scraping, setting_stock_list

scraping_router = APIRouter(prefix="/scraping",tags=['scraping'])

@scraping_router.get("/daily")
async def daily_work(date: str=datetime.now().strftime("%Y-%m-%d")):
    """
    ## Hint:
    date format need to be "%Y-%m-%d" beginning
    """
    stock_list = setting_stock_list()
    try:
        for stock in stock_list:
            df = daily_scraping(stock, date)
            if df is None:
                continue
            sql_client.insert_data("stock_price", df)
            sleep(1)
        
        return Response(
            status_code=status.HTTP_200_OK,
            content="Scrap Successfully"
        )
    
    except Exception as e:
        send_warn(f"Unexception {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexception Error occured"
        )