from time import sleep
import requests as req
from requests import Response
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import numpy as np


class BasicInformation:
    
    def __init__(self, types: str, stock_id: str):
        self.types = types
        self.stock_id = stock_id.split('.')[0]
        self.url = f'https://goodinfo.tw/tw/{types}.asp?STOCK_ID={self.stock_id}'

    def get_data(self) -> Response:
        user_agent = UserAgent().random
        headers = {'User-Agent': user_agent}
        print(f'visit: {self.url}')
        print(f'headers: {headers}')
        res = req.get(self.url,headers=headers)
        res.encoding = 'utf-8'
        if '若您是使用程式大量下載本網站資料' not in res.text :
            print(res.text)
            return res
        else:
            print(f"Scraping Failed")
        sleep(np.random.uniform(3, 5))

    def parse_data(self):
        response = self.get_data()
        soup = bs(response.text, 'lxml')
        parse_data = soup.select('table.b1.p4_6.r10.box_shadow tr td')
        if parse_data == []:
            return None
        else:
            parse_data = parse_data[1:] # delete title
            basic_dict = {}
            for index, value in enumerate(parse_data):
                if index % 2 == 1:
                    value = value.text.replace('\xa0','')
                    basic_dict[f'{parse_data[index - 1].text}'] = value
            return basic_dict
        
    def another_way(self):
        url = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"

        payload = {}
        headers = {}

        response = req.request("GET", url, headers=headers, data=payload)

        print(response.text)