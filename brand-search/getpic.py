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



## 抓取商标图片地址
##      公告期号、公告类型
def get_image(annNum):

    ## 数据库配置
    conn = pymongo.MongoClient('mongodb://10.10.107.103:27017')
    db = conn.BrandGazette  # 连接数据库名

    imgCode = db.annNumPicCode.find({'ann_num':annNum})  ##  获取期号下的图片code

    for i in list(imgCode):

        ann_num = i['ann_num']
        ann_type = i['ann_type']
        code = i['code']

        url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/imageView.html'    ## 采集地址

        # 获取需要的 cookie
        cookie = load_cookie()

        # body 参数
        _dic = {'id': code, 'pageNum':'9999999', 'flag': 1}
        _data = bytes(urllib.parse.urlencode(_dic), encoding='utf-8')

        headers = {
            'Cookie': cookie,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'
        }

        ## 获取总条数和总页数
        _req = urllib.request.Request(url=url, data=_data, headers=headers, method='POST')
        _jsonContent = urllib.request.urlopen(_req).read().decode('utf-8')  ## 返回 值
        _jsonData = json.loads(_jsonContent)
        totalNum = _jsonData['total']   ## 总条数
        totalPage = _jsonData['totalPage']  ## 总页数
        pageSize = _jsonData['pageSize']    ## 每页显示条数

        ## 判断是否有已经抓取的记录


        lastImg = db.gazettePic.find({'code':i['code']}).sort([("_id", -1)]).limit(1)  ##  最后采集的数据
        if lastImg.count() == 0:    ## 查询结果为零
            startNum = 0  ## 循环开始值,页码
        else:
            startNum = lastImg[0]['page']


        if totalPage > startNum:

            offset = 4  ## 偏移量
            for k in list(range(startNum,totalPage)):

                pageNum = ( k * pageSize ) + offset ## 页码

                dic = {'id': code, 'pageNum': pageNum, 'flag': 1}
                data = bytes(urllib.parse.urlencode(dic), encoding='utf-8')

                ## 获取 pageNum 页的图片列表
                req = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
                jsonContent = urllib.request.urlopen(req).read().decode('utf-8')  ## 返回 值
                jsonData = json.loads(jsonContent)

                imageList = []
                for j in list(jsonData['imaglist']):        ## 吧单页的图片放到json里面

                    picUrl = j      ## 图片地址
                    picPath = j.replace("http://sbggwj.saic.gov.cn:8000",'',1)  ## 去掉图片域名部分，需要作为图片本地的保存地址使用
                    thisTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                    imageList.append({"ann_num":ann_num,"ann_type":ann_type,"code":code,"page":k+1,"picUrl":j,"picPath":picPath,"add_time": thisTime})

                if len(imageList) > 0:

                    db.gazettePic.insert_many(imageList)        ## 记录图片地址

                    print('采集完成：',ann_num,ann_type,k+1)



##  设置采集
##  参数为 期数，倒序开始采集
def spideImg(startNum,endNum):


    ## 从最后抓取的期开始继续抓取
    conn = pymongo.MongoClient('mongodb://10.10.107.103:27017')
    db = conn.BrandGazette  # 连接数据库名
    last = db.gazettePic.find().sort([("_id", -1)]).limit(1)  ##  最后采集的数据
    if last[0]['ann_num']:
        startNum = last[0]['ann_num']

    if startNum > endNum:
        for i in range(startNum, endNum, -1):
            print(i)
            # get_image(i)
    else:
        print('起始值必须大于结束值')
        exit()



###################################################################

###################################################################


if __name__ == "__main__":
    ##  采集图片地址 start

    startNum= 1624 ## 1624      ## 起始期
    endNum = 0  ## 结束期
    spideImg(startNum,endNum)

######################################################################################################################## end




######################################################################################################################## Test start
