#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import ssl
import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import os
import pymongo
import json
import math
import time

from urllib import request
from http import cookiejar

ssl._create_default_https_context = ssl._create_unverified_context

########################################################################################################################  start


## 保存cookie
def make_cookie_file(cookie_filename):

    url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearch.html'
    # cookie_filename = 'annSearchCookie.txt'

    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'
    }
    dic = {'annNum': '1624'}
    data = bytes(urllib.parse.urlencode(dic), encoding='utf-8')

    ## 创建记录cookie方法
    # cpploe = http.cookiejar.CookieJar()   # 创建实例
    cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)

    ## 创建请求url
    request = urllib.request.Request(url,data=data,headers=header)

    ## 创建实际请求
    response = opener.open(request)

    cookieStr = ''
    for item in cookie:
        cookieStr = cookieStr + item.name + '=' + item.value + ';'

    # print(cookieStr)
    # cookie.save()

    f = open(cookie_filename,'a')
    f.write(cookieStr)
    f.closed

## 读取 cookie
def load_cookie():
    cookie_filename = 'annSearchCookie.txt'

    if(os.path.exists(cookie_filename)):
        with open(cookie_filename, mode='r', encoding='utf-8') as f:
            ftext = f.read()

            if (ftext == ''):
                res = make_cookie_file(cookie_filename)
                load_cookie()

            else:
                return ftext
    else:
        make_cookie_file(cookie_filename)
        load_cookie()

## 换取code
##  根据公告期号和公告类型换取对应的code
def get_code(annNum,annTypecode):
    url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/selectInfoidBycode.html'   ## 请求地址

    # 获取需要的 cookie
    cookie = load_cookie()

    # body 参数
    dic = {'annNum': annNum, 'annTypecode': annTypecode}
    data = bytes(urllib.parse.urlencode(dic), encoding='utf-8')

    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0',
    }

    req = urllib.request.Request(url=url, data=data, headers=headers, method='POST')

    try:
        code =  urllib.request.urlopen(req).read().decode('utf-8')  ## 返回 code 值

    except urllib.error.URLError as e:
        code = ''

    return code


## 记录商标期号、类型 对应的code
##
def annnum_code_log(endNum):
    conn = pymongo.MongoClient('mongodb://10.10.107.103:27017')
    db = conn.BrandGazette  # 连接数据库名
    start_num = 1
    # type_code = ['TMZCSQ','TMZCZC','TMZRSQ','TMBMSQ','TMXZSQ']      ## 初审公告、注册公告、转让/转义公告、注册人/申请人变更及地址变更、续展公告

    for i in list(range(start_num, endNum)):

        type_code = get_annType(i)
        for j in type_code:

            code = get_code(i,j)
            if len(code):

                thisTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                db.annNumPicCode.insert_one({"ann_num": i, "ann_type": j, "code": code,"add_time": thisTime})

        print('add annNum:')
        print(i)


## 获取每期下有的商标公告分类
## get 方法   ，参数为公告期数
##
def get_annType(annNum):
    url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/getAnnType.html'       ## 请求地址

    # 获取需要的 cookie
    cookie = load_cookie()

    # body 参数
    dic = {'annNum': annNum}
    data = bytes(urllib.parse.urlencode(dic), encoding='utf-8')

    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0',
    }

    req = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
    jsonContent = urllib.request.urlopen(req).read().decode('utf-8')  ## 返回 type的值
    jsonData = json.loads(jsonContent)

    typeCode = []
    for item in jsonData:
        typeCode.append(item['ann_type_code'])

    return typeCode



## 执行

annnum_code_log(1625)




######################################################################################################################## end




######################################################################################################################## Test start
