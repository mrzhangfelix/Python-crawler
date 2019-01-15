#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import traceback
import requests
import time

base_url = 'https://www.baidu.com/'

def get_html(url):
    try:
        proxy = { "https": "http://username:password@xxxxxx.com:8080" }
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0'}
        r=requests.get(url,timeout=30, headers = headers, proxies = proxy)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    except:
        print('获取数据失败，请检查你的网络连接')
        print(str(traceback.format_exc()))
        return "ERROR"

def main(base_url):
    html=get_html(base_url)
    print(html)

if __name__ == '__main__':
    main(base_url)
