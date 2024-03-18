from fastapi import FastAPI
from typing import List
from scraping_package import options_scraping

app = FastAPI()


@app.get('/data')
async def get_data() -> List[dict]:
    df = options_scraping.main()
    data = df.to_dict(orient='records')
    return data