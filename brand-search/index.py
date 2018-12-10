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

from http import cookiejar

ssl._create_default_https_context = ssl._create_unverified_context

########################################################################################################################  start

## 采集字段举例：
# "page_no":1,
# "tm_name":"图形",
# "ann_type_code":"TMZCSQ",
# "tmname":"图形",
# "reg_name":"东莞市附城上丰粘胶加工厂",
# "ann_type":"商标初步审定公告",
# "ann_num":"703",
# "reg_num":"1342551",
# "id":"ED8A238833C44C3BA67A430CAF3A90AB",
# "rn":51,
# "ann_date":"1999-09-14",
# "regname":"东莞市附城上丰粘胶加工厂"

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



## 抓取商标列表
##      公告期数，没有显示条数，页码
def get_annSearchDG(annNum,rows=0,page=0):
    url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearchDG.html';    ## 采集地址

    conn = pymongo.MongoClient('mongodb://10.10.107.103:27017')
    db = conn.BrandGazette  # 连接数据库名

    # 获取需要的 cookie
    cookie = load_cookie()

    # body 参数
    dic = {'annNum': annNum, 'rows':rows, 'page': page}     # dic = {'annNum': '1624','rows':'5','page':'1'}
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

        db.gazetteInfo.insert_many(rows)
        count = len(rows)   ##  处理的条数

    return total,count      ## 返回总条数和处理成功的条数



##  设置采集
def spideGazette(endNum):

    pageShow = 1500     ## 每页显示条数
    pageNum = 1         ## 采集页数

    conn = pymongo.MongoClient('mongodb://10.10.107.103:27017')
    db = conn.BrandGazette  # 连接数据库名

    ## 读取中段的操作，继续采集
    lastNum = db.spiderLog.find().sort([("add_time",-1)]).limit(1)  ##  最后采集的数据

    page_num =  lastNum[0]['page_num']   ## 最后页码
    page_show = lastNum[0]['page_show'] ## 每页显示数
    start_num = lastNum[0]['ann_num']   ## 最后采集的期数
    start_num = 1625

    ## 判断最后采集的期数的最大页码
    ck_last = get_annSearchDG(start_num)
    ck_totalNum = ck_last[0]  ##  单期商标返回的总数
    ck_maxPage = math.ceil(ck_totalNum / page_show)


    for i in list(range(start_num,endNum)):

        if i > start_num:

            print('start:')
            print(i)

            re = get_annSearchDG(i)
            totalNum = re[0]  ##  单期商标返回的总数
            maxPage = math.ceil(totalNum / pageShow)
            maxPage = maxPage + 1
            for j in list(range(1, maxPage)):
                re = get_annSearchDG(i, pageShow, j)  ##  采集返回

                thisTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                db.spiderLog.insert_one({"ann_num": i, "page_show": pageShow, "page_num": j, "content_num": re[1], "add_time": thisTime})

        else:
            print('re start:')
            print(i)

            if ck_maxPage>page_num:  ## 中断后开始

                for j in list(range(page_num+1, ck_maxPage+1)):

                    re = get_annSearchDG(start_num, pageShow, j)    ##  采集返回

                    thisTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    db.spiderLog.insert_one({"ann_num":start_num,"page_show":pageShow,"page_num":j,"content_num":re[1],"add_time":thisTime})




spideGazette(1626)




######################################################################################################################## end




######################################################################################################################## Test start

# conn = pymongo.MongoClient('mongodb://10.10.107.103:27017')
# db = conn.BrandGazette # 连接数据库名


# for item in db.gazetteInfo.find():
#     print(item)

# db.gazetteInfo.insert_one({
# 		"page_no": 1,
# 		"tm_name": "银康",
# 		"ann_type_code": "TMZCSQ",
# 		"tmname": "银康",
# 		"reg_name": "上海银康投资管理有限公司",
# 		"ann_type": "商标初步审定公告",
# 		"ann_num": "1624",
# 		"reg_num": "10836225",
# 		"id": "e48b920e6711d40c016715b1bd105c64",
# 		"rn": 1,
# 		"ann_date": "2018-11-20",
# 		"regname": "上海银康投资管理有限公司"
# 	})






