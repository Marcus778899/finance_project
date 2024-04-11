import requests as req
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent


class BasicInformation:
    def __init__(self, types: str, stock_id: str):
        self.types = types
        self.stock_id = stock_id.split('.')[0]
        self.url = f'https://goodinfo.tw/tw/{types}.asp?STOCK_ID={self.stock_id}'

    def get_data(self):
        user_agent = UserAgent().random
        headers = {'User-Agent': user_agent}
        res = req.get(self.url,headers=headers)
        print(f'visit: {self.url} ,status: {res.status_code}')
        res.encoding = 'utf-8'
        soup = bs(res.text, 'lxml')
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
    
if __name__ == '__main__':
    action = BasicInformation('BasicInfo', '2443')
    print(action.get_data())
        
        