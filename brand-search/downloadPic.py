#! /usr/bin/env python3
# -*- coding:utf-8 -*-
## 下载图片

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


## 递归创建目录
def mkdir_path(savePath):
    if savePath[0] == '/':
        path = savePath[1:len(savePath)]
    else:
        path = savePath

    if os.path.isdir(path):
        return True
    else:
        os.makedirs(path,0o777)
        return True


## 下载图片
##
def download_image():

    ## 数据库配置
    conn = pymongo.MongoClient('mongodb://10.10.107.103:27017')
    db = conn.BrandGazette  # 连接数据库名

    _id = ''
    lastImg = db.downloadPicLog.find().sort([("_id", -1)]).limit(1)  ##  最后采集的数据
    for i in lastImg:
        if i['p_id']:
            _id = i['p_id']   ## 最后插入的图片_id

    if _id:    ## 中断后下载
        list = db.gazettePic.find({"_id":{"$gt":_id}}) ##  最后采集的数据
    else:
        list = db.gazettePic.find()  ##  最后采集的数据

    for item in list:

        path = item['picPath']

        ## 图片保存路径
        if path[0] == '/':
            savePath = path[1:len(path)]
        else:
            savePath = path

        if mkdir_path(os.path.dirname(path)):

            ## 保存图片
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(item['picUrl'], savePath)

            ## 记录log
            thisTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            db.downloadPicLog.insert_one({"p_id": item['_id'], "ann_num": item['ann_num'], "ann_type": item['ann_type'], "picPath": savePath, "add_time": thisTime})

            print(item['_id'])



#########


download_image()













######################################################################################################################## end




######################################################################################################################## Test start
