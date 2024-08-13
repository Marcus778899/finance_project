# https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={上市或上櫃)_{股票代號}.tw_{日期}"
import json
import time
import logging
from datetime import datetime
from tqdm import tqdm
import requests
import pandas as pd
from fake_useragent import UserAgent
from . import stock_list
# import random
# from .free_proxy import proxies

class ScrapingStockPrice:
    def __init__(self):
        self.stock_list = stock_list

    def request_url(self, url, headers):
        """
        Send a GET request to the specified URL with a random proxy from the proxy list.
        If the request fails, try a different proxy until a successful response is received.
        """
        while True:
            try:
                # ip = random.choice(self.prxoy_list)
                # proxy = {'http': ip, 'https': ip}
                # logging.info(f"proxy => {ip}")
                response = requests.request(
                    "GET",
                    url,
                    headers=headers,
                    # proxies=proxy,
                    timeout=5
                )
                content = json.loads(response.text)['msgArray'][0]
                return content
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
                time.sleep(150)
                continue

    def main(self,date: datetime) -> pd.DataFrame:
        if date.weekday() == 5 or date.weekday() == 6:
            logging.error("Saturday or Sunday is not a working day")
            return None
    
        year = date.year
        month = date.month
        day = date.day
        suffix = f"{year}{month:02d}{day:02d}"
        ua = UserAgent()

        df = []

        pbar = tqdm(self.stock_list, unit="stock")
        for prefix in pbar:
            pbar.set_description(f"Processing {prefix}")
            url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={prefix}_{suffix}"

            headers = {
                'content-type':'application/json',
                'user-agent':ua.random
            }
            logging.info(f"Now request: {prefix} on {suffix}")

            content = self.request_url(url, headers)

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
            time.sleep(1)

        df = pd.DataFrame(df)

        return df
