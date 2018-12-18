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

## Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36


# userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'
# userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'

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

        ## 判断是否有已经抓取的记录
        lastImg = db.gazettePic.find({'code': code, 'ann_num': annNum}).sort([("page",-1)]).limit(1)  ##  最后采集的数据

        url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/imageView.html'    ## 采集地址

        ## 获取需要的 cookie
        cookie = load_cookie()

        # # body 参数
        # _dic = {'id': code, 'pageNum':'9999999', 'flag': 1}
        # _data = bytes(urllib.parse.urlencode(_dic), encoding='utf-8')
        #
        headers = {
            'Cookie': cookie,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'
        }
        #
        # ## 获取总条数和总页数
        # _req = urllib.request.Request(url=url, data=_data, headers=headers, method='POST')
        # _jsonContent = urllib.request.urlopen(_req).read().decode('utf-8')  ## 返回 值
        # _jsonData = json.loads(_jsonContent)
        #
        # totalNum = _jsonData['total']   ## 总条数
        # totalPage = _jsonData['totalPage']  ## 总页数
        # pageSize = _jsonData['pageSize']    ## 每页显示条数


        ##  从统计信息表内取出总条数，计算出总页数
        annTypeCodeName = db.annType.find({'ann_type_code':ann_type}).limit(1)

        ## 商标局的公告名称做过变更 -- by zuiw
        if annTypeCodeName[0]['ann_type'] == '商标使用许可备案公告':
            _typeName_new = '商标使用许可合同备案公告'

            _info = db.catalogueInfo.find({"$and":[{"$or":[{"ann_type_code":str(annTypeCodeName[0]['ann_type'])},{"ann_type_code":str(_typeName_new)}]},{"ann_num":str(annNum)}]}  ).limit(1)  ##  最后采集的数据

        else:

            _info = db.catalogueInfo.find({'ann_type_code':str(annTypeCodeName[0]['ann_type']),'ann_num': str(annNum)}).limit(1)  ##  最后采集的数据

        totalNum = _info[0]['page_num']   ## 总条数
        pageSize = 20    ## 每页显示条数
        totalPage = math.ceil(totalNum / pageSize)  ## 总页数

        ## 抓取
        if lastImg.count() == 0:    ## result is zero
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
                jsonContent = urllib.request.urlopen(req,timeout=300).read().decode('utf-8')  ## 返回值,超时时间设置为300秒
                jsonData = json.loads(jsonContent)

                imageList = []
                for j in list(jsonData['imaglist']):        ## 吧单页的图片放到json里面

                    picUrl = j      ## 图片地址
                    picPath = j.replace("http://sbggwj.saic.gov.cn:8000",'',1)  ## 去掉图片域名部分，需要作为图片本地的保存地址使用
                    thisTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                    imageList.append({"ann_num":ann_num,"ann_type":ann_type,"code":code,"page":k+1,"picUrl":j,"picPath":picPath,"add_time": thisTime})

                if len(imageList) > 0:

                    db.gazettePic.insert_many(imageList)        ## 记录图片地址

                    print('Finsh:', ann_num , ann_type , k+1)



##  设置采集
##  参数为 期数，倒序开始采集, startNum > endNum
## $gt 大于 $lt 小于
def spideImg(startNum,endNum):

    ## 从最后抓取的期开始继续抓取
    conn = pymongo.MongoClient('mongodb://10.10.107.103:27017')
    db = conn.BrandGazette  # 连接数据库名
    # last = db.gazettePic.find().sort([("_id", -1)]).limit(1)  ##  最后采集的数据
    last = db.gazettePic.find({"ann_num":{"$gt":endNum,"$lte":startNum}}).sort([("ann_num",1)]).limit(1) ##  最后采集的数据

    # if not last and last[0]['ann_num']:
    if last[0]['ann_num']:
        startNum = last[0]['ann_num']

    if startNum > endNum:
        for i in range(startNum, endNum, -1):
            get_image(i)
    else:
        print(startNum)
        print(endNum)
        print('起始值必须大于结束值')
        exit()



###################################################################

###################################################################


# if __name__ == "__main__":
#     ##  采集图片地址 start
#
#     startNum= 1624 ## 1624      ## 起始期
#     endNum = 0  ## 结束期
#     spideImg(startNum,endNum)

######################################################################################################################## end

## 参数说明：
##  1 ：1 -- 1500 期
##  2： 1501 - 1550
##  3： 1551 - 1600
##  4：  1601 - 1605
##  5： 1606 - 1610
##  6： 1611 - 1615
##  7： 1616 - 1620

import sys

startNum = ''
endNum = ''

if sys.argv[1] == '1':
    startNum = 1500
    endNum = 0

if sys.argv[1] == '2':
    startNum = 1550
    endNum = 1500

if sys.argv[1] == '3':
    startNum = 1600
    endNum = 1550

if sys.argv[1] == '4':
    startNum = 1605
    endNum = 1600

if sys.argv[1] == '5':
    startNum = 1610
    endNum = 1605

if sys.argv[1] == '6':
    startNum = 1615
    endNum = 1610

if sys.argv[1] == '7':
    startNum = 1620
    endNum = 1615

spideImg(startNum,endNum)

######################################################################################################################## Test start
