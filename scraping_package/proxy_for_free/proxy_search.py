'''
Free proxy can use
Unfortunately no proxy is available
'''
import re
from datetime import datetime
import requests as req

def get_proxy():
    response = req.get('https://free-proxy-list.net/')
    matches = re.findall('\d+\.\d+\.\d+\.\d+:\d+', response.text)

    valid_ips = []
    for ip in matches:
        try:
            res = req.get('https://api.ipify.org?format=json',proxies = {'http':ip, 'https':ip}, timeout = 2)
            valid_ips.append(ip)
            print(f'valid ip: {res.json()}')
        except:
            print(f'invalid ip: {ip}')
    
    return valid_ips

if __name__ == '__main__':
    start = datetime.now()
    proxy_ips = get_proxy()
    end = datetime.now()
    print(f'total spend {(end - start).seconds} seconds')
    with open('./free_proxy.txt','w') as file:
        for ip in proxy_ips:
            file.write(ip + '\n')
