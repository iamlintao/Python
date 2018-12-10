#! /usr/bin/env python3
# -*- coding:utf-8 -*-
## 采集每一期公告的统计信息

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

from http import cookiejar

ssl._create_default_https_context = ssl._create_unverified_context

########################################################################################################################  start

# ann_type_code	商标初步审定公告    ## 公告类型
# page_num	187     ## 公告页数
# case_num	1       ## 公告件数
# ann_num	125     ## 公告期号
# id	5ADB5C4E318049F9B4A3C4C4E37D38B1    ## 公告id
# rn	2
# ann_date	1985-09-15      ## 公告日期

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



## 抓取公告概述统计
def get_CatalogueInfo(annNum):
    url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/getCatalogueInfo.html';    ## 采集地址

    conn = pymongo.MongoClient('mongodb://10.10.107.103:27017')
    db = conn.BrandGazette  # 连接数据库名

    # 获取需要的 cookie
    cookie = load_cookie()

    # body 参数
    rows = 1500
    page = 1
    dic = {'annNum': annNum, 'rows':rows, 'page': page}
    data = bytes(urllib.parse.urlencode(dic), encoding='utf-8')

    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'
    }

    req = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
    response = urllib.request.urlopen(req)

    jsonContent = response.read().decode('utf-8')
    jsonData = json.loads(jsonContent)
    total = jsonData['total']   ## 总条数
    rows = jsonData['rows']      ## 当前页的商标列表

    count = 0       ## 计数器
    if  len(jsonData['rows']):

        db.catalogueInfo.insert_many(rows)
        count = len(rows)   ##  处理的条数

    return total,count      ## 返回总条数和处理成功的条数



## 设置采集
## 结束期号
def spideCatalogue(endNum):

    pageShow = 1500     ## 每页显示条数
    pageNum = 1625         ## 采集页数

    for i in list(range(pageNum,endNum)):

        re = get_CatalogueInfo(i)  ##  采集返回

        print('start:')
        print(i)
        print(re)


spideCatalogue(1626)




######################################################################################################################## end




######################################################################################################################## Test start






