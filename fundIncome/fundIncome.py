#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import traceback

import requests
from bs4 import BeautifulSoup

import time

current_milli_time = lambda: int(round(time.time() * 1000))

sum = 0
base_url = 'http://fundgz.1234567.com.cn/js/{}.js?rt={}'

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


def get_concent(url,amount):
    res=get_html(url)
    res=res[8:-2]
    fundinfo=json.loads(res)
    # print('当前时间：'+fundinfo['gztime'])
    comment={}
    try:
        comment['基金名']=fundinfo['name']#.ljust(14)
        for i in range(len(comment['基金名']),14):
            comment['基金名']=comment['基金名']+'  '
    # comment['净值']=fundinfo['gsz']
        comment['涨幅率']=fundinfo['gszzl']+'%'
        for i in range(len(comment['涨幅率']),7):
            comment['涨幅率']=comment['涨幅率']+' '
        comment['盈利']=float(fundinfo['gszzl'])*amount/100
        global sum
        sum+=comment['盈利']
    except BaseException as e:
        print('获取基金信息失败')
        print(str(traceback.format_exc()))
    return comment

def get_concentByShare(url,share):
    res=get_html(url)
    res=res[8:-2]
    fundinfo=json.loads(res)
    # print('当前时间：'+fundinfo['gztime'])
    comment={}
    try:
        comment['基金名']=fundinfo['name']#.ljust(14)
        for i in range(len(comment['基金名']),14):
            comment['基金名']=comment['基金名']+'  '
            # comment['净值']=fundinfo['gsz']
        comment['涨幅率']=fundinfo['gszzl']+'%'
        for i in range(len(comment['涨幅率']),7):
            comment['涨幅率']=comment['涨幅率']+' '
        comment['盈利']=(float(fundinfo['gsz'])-float(fundinfo['dwjz']))*share
        global sum
        sum+=comment['盈利']
    except BaseException as e:
        print('获取基金信息失败')
        print(str(traceback.format_exc()))
    return comment


def show(list):
    for l in list:
        print('%s : %s  '%(l,str(list[l])), end='\t')
    print('')



def main(base_url):
    codelist=[]
    amountlist=[]
    sharelist=[]
    url_list=[]
    mode=0
    with open('fund.json', 'r') as f:
        fundJson=f.read()
        fundconf=json.loads(fundJson)
        mode=fundconf['mode']
        if mode==1:
            print('使用金额计算收益')
        elif mode==2:
            print('使用份额计算收益')
        else:
            print('mode未配置或配置出错')
            return
        for fund in fundconf['fundlist']:
            codelist.append(fund['fundcode'])
            amountlist.append(float(fund['fundamount']))
            sharelist.append(float(fund['Holdingshare']))
    for i in codelist:
        url_list.append(base_url.format(i,current_milli_time()))
    if mode==1:
        for url,amount in zip(url_list,amountlist):
            content=get_concent(url,amount)
            show(content)
    else:
        for url,share in zip(url_list,sharelist):
            content=get_concentByShare(url,share)
            show(content)
    print('当前基金总盈利:'+str(sum))

if __name__ == '__main__':
    main(base_url)