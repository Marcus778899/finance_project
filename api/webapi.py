from fastapi import FastAPI
from api.response_model import StrikePriceRequest, OptionData
from scraping_package import options_scraping

app = FastAPI(
    title="Options Data",
)

merge_df = options_scraping.main()

@app.get('/')
async def root():
    root_dict = {
        "message": "Hello World",
        "url": ["/data"]
        }
    return root_dict

@app.get('/data')
async def get_data():
    return merge_df

@app.post('/data/strike_price')
async def get_strike(request_body: StrikePriceRequest):
    strike_price = request_body.strike_price
    option_data = []
    for index, row in merge_df:
        option_data.append(OptionData(option_type=index, data=[option for option in row if option['履約價'] == strike_price]))
    return option_data