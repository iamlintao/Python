#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import ssl
import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import os
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

    print(jsonData)






get_annSearchDG(5)




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






