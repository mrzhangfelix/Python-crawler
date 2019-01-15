#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import traceback
import requests
from bs4 import BeautifulSoup

import time

current_milli_time = lambda: int(round(time.time() * 1000))

base_url = 'http://xxxxx.com/'

def get_html(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0'}
        r=requests.get(url,timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    except:
        print('获取数据失败，请检查你的网络连接')
        print(str(traceback.format_exc()))
        return "ERROR"

def main(base_url):
    user_list=[]
    with open('config.json', 'r') as f:
        configFile=f.read()
        configJson=json.loads(configFile)
        user_list=configJson['people']
    for user in user_list:
        print('name::'+user['name']+'gender:'+user['gender']+'age:'+str(user['age']))
    html=get_html(base_url)
    print(html)
    print('succes!')

if __name__ == '__main__':
    main(base_url)
