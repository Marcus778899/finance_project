from fastapi import FastAPI
import requests as req
from api.response_model import StrikePriceRequest
from scraping_package import options_scraping



app = FastAPI(
    title="Options Data",
)

merge_df = options_scraping.main()

@app.get('/data')
async def get_data():
    return merge_df

@app.post('/data/strike')
async def get_strike(request_body: StrikePriceRequest):
    strike_price = request_body.strike_price
    traget_df = []
    for index , price_table in merge_df.items():
        if index == '時間':
            continue
        for price in price_table:
            if price['履約價'] == strike_price:
                price['category'] = index
                traget_df.append(price)
    return traget_df