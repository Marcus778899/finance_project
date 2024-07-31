import json
import os
import requests
from bs4 import BeautifulSoup as bs

url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_2330.tw_20210504"

payload = {}
headers = {
  'Cookie': 'JSESSIONID=BBA418118B0189B06265CBFC534BB4C8'
}

response = requests.request("GET", url, headers=headers, data=payload)

data = json.loads(response.text)
print(data['msgArray'])
