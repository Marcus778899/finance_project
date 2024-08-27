"""
上市 https://isin.twse.com.tw/isin/C_public.jsp?strMode=2
上櫃 https://isin.twse.com.tw/isin/C_public.jsp?strMode=4
"""
from . import logger
from io import StringIO
import requests as req
import pandas as pd


def scraping_stock_list(url):

    logger.debug(f"scraping {url}")
    response = req.get(url)
    logger.debug(f"status_code: {response.status_code}, Now processing data...")

    html_data = StringIO(response.text)
    df = pd.read_html(html_data)[0]

    exclude_title = [
        "臺灣存託憑證(TDR)",
        "特別股",
        "受益證券-資產基礎證券",
        "受益證券-不動產投資信託",
        "創新板",
        "上市認購(售)權證",
        "ETN",
        "ETF",
        "股票"
    ]
    def is_possible_title(text):
        return any(title in text for title in exclude_title)
    df = df[~df.iloc[:,0].apply(lambda x: is_possible_title(str(x)))]
    logger.debug(f"status_code: {response.status_code}, Data processing complete")

    df.columns = df.iloc[0]
    df = df.iloc[2:]
    df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
    column_translate = {
        '有價證券代號及名稱':'stock',
        '國際證券辨識號碼(ISIN Code)':'ISIN_Code',
        '上市日':'date_market',
        '市場別':'category_market',
        '產業別':'category_industry',
    }

    df.columns = [column_translate.get(x, x) for x in df.columns]

    df['stock'] = df['stock'].str.replace('　', '')
    df['date_market'] = pd.to_datetime(
        df['date_market'].str.replace('/', '-'),
        format='%Y-%m-%d'
        )
    
    return df

def main():
    url_list = [
        "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2", 
        "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4"  
    ]
    df = pd.DataFrame()
    for url in url_list:
        df_tmp = scraping_stock_list(url)
        df = pd.concat([df, df_tmp], ignore_index=True)
    return df
    