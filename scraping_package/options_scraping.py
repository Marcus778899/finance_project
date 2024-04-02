import requests as req
import pandas as pd
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta

def debug(func):
    def wrapper(*args, **kwargs):
        print(f'Now processing {func.__name__}')
        result = func(*args, **kwargs)
        print(result)
        print(type(result))
        return result
    return wrapper

def get_response(url: str) -> bs:

    time_now = datetime.now()
    response = req.get(url)
    soup = bs(response.text, 'lxml')
    return soup, time_now

def parse_html(soup: bs, time_now: datetime) -> dict[str, list[dict]]:

    # 主欄位
    first_columns = soup.select_one('table.TableV1 tr.C.TableV2Field')
    columns = first_columns.get_text()
    columns = [desc.replace('\u3000','') for desc in columns.split('\n') if desc]

    # 即時價格波動
    table = soup.select('tr.R')
    data = []
    for tag in table:
        data.append([td.get_text() for td in tag if td != '\n' and td != ' '])

    df = pd.DataFrame(data[1:], columns= data[0])
    df['履約價'] = df['履約價'].astype(int)
    df.replace('--', pd.NA, inplace=True)

# region Dataframe tramsform to json

    # combine with json
    call_df = df[df.columns[:6]].to_dict(orient='records')
    put_df = df[df.columns[5:]].to_dict(orient='records')

    merge_json = {
        '時間': time_now,
        '買權': call_df,
        '賣權': put_df
        }
    
# endregion
    return merge_json
    
@debug
def main():
    url = 'https://ww2.money-link.com.tw/FutOpt/TWChoose.aspx'
    soup, time_now = get_response(url)
    test = parse_html(soup, time_now)

    return test
