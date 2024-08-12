# https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={上市或上櫃)_{股票代號}.tw_{日期}"
import json
import logging
from datetime import datetime
from tqdm import tqdm
import requests
from . import stock_list
import pandas as pd
import time
import time
    
def scraping(date: datetime):

    if date.weekday() == 5 or date.weekday() == 6:
        logging.error("Saturday or Sunday is not a working day")
        return None
    
    year = date.year
    month = date.month
    day = date.day
    suffix = f"{year}{month:02d}{day:02d}"

    df = []

    pbar = tqdm(stock_list, unit="stock")
    for index, prefix in enumerate(pbar):
        if index % 10 == 0:
            time.sleep(5)
        pbar.set_description(f"Processing {prefix}")
        url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={prefix}_{suffix}"

        payload = {}
        headers = {
            'content-type':'application/json',
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
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

