# https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={上市或上櫃)_{股票代號}.tw_{日期}"
import json
import logging
from datetime import datetime
from tqdm import tqdm
import requests
from . import stock_list
import pandas as pd
    
def scraping(date: datetime):

    year = date.year
    month = date.month
    day = date.day
    suffix = f"{year}{month:02d}{day:02d}"

    df = []

    pbar = tqdm(stock_list)
    for prefix in pbar:
        pbar.set_description(f"Processing {prefix}")
        url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={prefix}_{suffix}"

        payload = {}
        headers = {
        'Cookie': 'JSESSIONID=BBA418118B0189B06265CBFC534BB4C8'
        }
        logging.info(f"Now request: {prefix} on {suffix}")
        response = requests.request("GET", url, headers=headers, data=payload)

        content = json.loads(response.text)['msgArray'][0]

        required_keys = ['c', 'n', 'y', 'o', 'h', 'l', 'u', 'w', 'v', 'd']
        if not all(key in content and content[key] != '-' for key in required_keys):
            logging.warning(f"Skipping invalid data for {prefix}")
            continue

        def safe_float_convert(value):
            try:
                return float(value)
            except ValueError:
                return float('nan')

        data = {
            'stock': content['c'],
            'stock_name': content['n'],
            'close_price': safe_float_convert(content['y']),
            'open_price': safe_float_convert(content['o']),
            'high_price': safe_float_convert(content['h']),
            'low_price': safe_float_convert(content['l']),
            'upper_limit': safe_float_convert(content['u']),
            'lower_limit': safe_float_convert(content['w']),
            'volume': safe_float_convert(content['v']),
            'date': datetime.strptime(suffix,'%Y%m%d').strftime('%Y-%m-%d')
        }
        df.append(data)

    df = pd.DataFrame(df)

    return df

