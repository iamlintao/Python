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
import requests

from http import cookiejar
from urllib import request

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



## 抓取商标图片
##      公告期号对应的code，图片页码
def get_annSearchDG(id,pageNum):
    url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/imageView.html'    ## 采集地址

    # 获取需要的 cookie
    cookie = load_cookie()

    # body 参数
    dic = {'id': id, 'pageNum':pageNum, 'flag': 1}
    data = bytes(urllib.parse.urlencode(dic), encoding='utf-8')

    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'
    }

    req = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
    jsonContent = urllib.request.urlopen(req).read().decode('utf-8')  ## 返回 值
    jsonData = json.loads(jsonContent)

    pageSize = jsonData['pageSize']
    totalPage = jsonData['totalPage']
    total = jsonData['total']
    imaglist = jsonData['imaglist']

    print(totalPage)
    print(imaglist)



get_annSearchDG('B9DE4C1827094514ACA7F262180531E9',1)


##  设置采集
def spideGazette(endNum):

    pageShow = 1500     ## 每页显示条数
    pageNum = 1         ## 采集页数

    conn = pymongo.MongoClient('mongodb://10.10.107.103:27017')
    db = conn.BrandGazette  # 连接数据库名

    ## 读取中段的操作，继续采集
    lastNum = db.spiderLog.find().sort([("add_time",-1)]).limit(1)  ##  最后采集的数据

    page_num = lastNum[0]['page_num']   ## 最后页码
    page_show = lastNum[0]['page_show'] ## 每页显示数
    start_num = lastNum[0]['ann_num']   ## 最后采集的期数

    ## 判断最后采集的期数的最大页码
    ck_last = get_annSearchDG(start_num)
    ck_totalNum = ck_last[0]  ##  单期商标返回的总数
    ck_maxPage = math.ceil(ck_totalNum / page_show)


    # for i in list(range(start_num,endNum)):
    #
    #     if i > start_num:
    #
    #         print('start:')
    #         print(i)
    #
    #         re = get_annSearchDG(i)
    #         totalNum = re[0]  ##  单期商标返回的总数
    #         maxPage = math.ceil(totalNum / pageShow)
    #         maxPage = maxPage + 1
    #         for j in list(range(1, maxPage)):
    #             re = get_annSearchDG(i, pageShow, j)  ##  采集返回
    #
    #             thisTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #             db.spiderLog.insert_one({"ann_num": i, "page_show": pageShow, "page_num": j, "content_num": re[1], "add_time": thisTime})
    #
    #     else:
    #         print('re start:')
    #         print(i)
    #
    #         if ck_maxPage>page_num:  ## 中断后开始
    #
    #             for j in list(range(page_num+1, ck_maxPage+1)):
    #
    #                 re = get_annSearchDG(start_num, pageShow, j)    ##  采集返回
    #
    #                 thisTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #                 db.spiderLog.insert_one({"ann_num":start_num,"page_show":pageShow,"page_num":j,"content_num":re[1],"add_time":thisTime})




######################################################################################################################## end




######################################################################################################################## Test start
