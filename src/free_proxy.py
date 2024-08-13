'''
free proxy isn't steadable
'''
import re
import requests

def proxies():
    response = requests.get('https://free-proxy-list.net/')

    proxy_list = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', response.text)

    vaild_ip = []

    for ip in proxy_list:
        try:
            res = requests.get(
                'https://api.ipify.org?format=json', # check proxy vaild or not
                proxies={'http': ip, 'https': ip}, 
                timeout=5
            )
            if res.status_code == 200:
                vaild_ip.append(ip)
        except requests.exceptions.RequestException:
            pass
        
    return vaild_ip