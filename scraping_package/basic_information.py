import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd
from stock_scraping import stock_list_for_basic_information
from time import sleep


class BasicInformation:
    def __init__(self, types: str, stock_id: str):
        self.types = types
        self.stock_id = stock_id.split('.')[0]
        self.url = f'https://goodinfo.tw/tw/{types}.asp?STOCK_ID={self.stock_id}'

    def get_data(self):
        print(self.url)
        res = req.get(self.url)
        res.encoding = 'utf-8'
        print(res.text)
        soup = bs(res.text, 'lxml')
        parse_data = soup.select('table.b1.p4_6.r10.box_shadow tr td')
        if parse_data == []:
            return None
        else:
            parse_data = parse_data[1:-9] # delete title
            basic_dict = {}
            for index, value in enumerate(parse_data):
                if index % 2 == 1:
                    basic_dict[f'{parse_data[index - 1].text}'] = value.text
            return basic_dict

def main():
    stock_list = stock_list_for_basic_information()
    seen_value = set()
    for index, value in stock_list.items():
        if index in seen_value:
            continue
        print(f'now processing {value} {index}')
        action = BasicInformation('BasicInfo', index)
        basic_information = action.get_data()
        if basic_information is None:
            print(f'{value} {index} is not exist')
            pass
        seen_value.add(index)
        break
    print(basic_information)
    
if __name__ == '__main__':
    action = BasicInformation('BasicInfo', '2330')
    print(action.get_data())
        
        