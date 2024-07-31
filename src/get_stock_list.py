# 上市 https://isin.twse.com.tw/isin/C_public.jsp?strMode=2
# 上櫃 https://isin.twse.com.tw/isin/C_public.jsp?strMode=4
import logging
import requests as req
import pandas as pd
from io import StringIO


def scraping_stock_list(url):

    logging.info(f"scraping {url}")
    response = req.get(url)
    logging.info(f"status_code: {response.status_code}, Now processing data...")

    html_data = StringIO(response.text)
    df = pd.read_html(html_data)[0]

    df.columns = df.iloc[0]
    df = df.iloc[2:]
    df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1).drop(columns=['備註'], axis=0)
    column_translate = {
        '有價證券代號及名稱':'stock',
        '國際證券辨識號碼(ISIN Code)':'ISIN_Code',
        '上市日':'date_market',
        '市場別':'category_market',
        '產業別':'category_industry',
    }

    df.columns = [column_translate.get(x, x) for x in df.columns]

    df = df[df["CFICode"] == "ESVUFR"]

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
    print(df.head(3))
    print(df.dtypes)
    return df
    