#coding: utf-8

import requests
import traceback

base_url=''

def get_session( pool_connections, pool_maxsize, max_retries):
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize, max_retries=max_retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get_html(url,session):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
        r=session.get(url,timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    except:
        print('获取数据失败，未连接上网络')
        print(str(traceback.format_exc()))
        return "ERROR"

def main():
    session = get_session(50, 50, 3)
    url = 'https://xxxxxx.com/login.do'
    d = {
         'username': 'value',
         'password': '123456',
         'verifyCode':'2345'
    }
    # 需要登录
    session.post(url, data=d)
    # print(r)
    getIncident_url='http://xxxxxx.com/'
    SrAcceptInfo=get_html(getIncident_url,session)
    print(SrAcceptInfo)



if __name__ == '__main__':
    main()
