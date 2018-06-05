#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import traceback

import requests
from bs4 import BeautifulSoup

sum = 0
base_url = 'http://fund.eastmoney.com/'

def get_html(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0'}
        r=requests.get(url,timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    except:
        return "ERROR"


def get_concent(url,amount):
    html=get_html(url)
    soup=BeautifulSoup(html,'lxml')
    titlediv=soup.find('div',attrs={'class':'fundDetail-tit'})
    # time=soup.find('span',attrs={'id':'gz_gztime'})
    # print(time.text)
    curFundInfo=soup.find('dd',attrs={'class':'dataNums'})
    comment={}
    try:
        comment['基金名']=titlediv.text.strip().replace(u'\xa0', u' ')
        comment['净值']=curFundInfo.find('span',attrs={'id':'gz_gsz'}).text.strip()
        text2=curFundInfo.find('span',attrs={'id':'gz_gszzl'}).text.strip()
        comment['涨幅率']=text2
        comment['盈利']=float(text2[1:-1])*amount/100
        if text2[0:1]=='-':
            comment['盈利']=comment['盈利']*-1
        global sum
        sum+=comment['盈利']
    except BaseException as e:
        print(str(traceback.format_exc()))
    return comment


def show(list):
    for l in list:
        print(l+' : '+str(list[l]))
    print('\n')



def main(base_url):
    codelist=[]
    amountlist=[]
    url_list=[]
    with open('fund.json', 'r') as f:
        fundlistJson=f.read()
        fundlist=json.loads(fundlistJson)
        for fund in fundlist['fundlist']:
            codelist.append(fund['fundcode'])
            amountlist.append(float(fund['fundamount']))
    for i in codelist:
        url_list.append(base_url+i+'.html')
    print('url生成完成')

    for url,amount in zip(url_list,amountlist):
        content=get_concent(url,amount)
        show(content)
    print('当前基金总盈利:'+str(sum))

if __name__ == '__main__':
    main(base_url)