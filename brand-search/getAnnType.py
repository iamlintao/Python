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


## 记录商标期号、类型 对应的code
##
def insertAnnType(endNum):

    conn = pymongo.MongoClient('mongodb://10.10.107.103:27017')
    db = conn.BrandGazette  # 连接数据库名
    start_num = 1467

    for i in list(range(start_num, endNum)):

        type_code = get_annType(i)

        for j in list(type_code):

            ck = db.annType.find_one({'ann_type_code': j['ann_type_code']})
            if ck is  None:
                db.annType.insert_one(j)

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
        typeCode.append({'ann_type_code':item['ann_type_code'],'ann_type':item['ann_type']})

    return typeCode



## 执行

# insertAnnType(1626)


## 增加公告类型

def annnum_code_add():
    conn = pymongo.MongoClient('mongodb://10.10.107.103:27017')
    db = conn.BrandGazette  # 连接数据库名
    jsonContent = '[{"ann_type_code":"TMZCSQ","ann_type":"商标初步审定公告"},{"ann_type_code":"TMJTSQ","ann_type":"集体商标初步审定公告"},{"ann_type_code":"TMZMSQ","ann_type":"证明商标初步审定公告"},{"ann_type_code":"TMTCSQ","ann_type":"特殊标志登记公告"},{"ann_type_code":"TMZCZC","ann_type":"商标注册公告（一）"},{"ann_type_code":"TMQTZC","ann_type":"商标注册公告（二）"},{"ann_type_code":"TMJTZC","ann_type":"集体商标注册公告"},{"ann_type_code":"TMZMZC","ann_type":"证明商标注册公告"},{"ann_type_code":"TMZRSQ","ann_type":"商标转让/移转公告"},{"ann_type_code":"TMBMSQ","ann_type":"商标注册人/申请人名义及地址变更公告"},{"ann_type_code":"TMSJSQ","ann_type":"商品/服务项目删减公告"},{"ann_type_code":"TMBGSQ","ann_type":"变更商标代理机构公告"},{"ann_type_code":"TMGZSQ","ann_type":"商标更正公告"},{"ann_type_code":"TMXZSQ","ann_type":"注册商标续展公告"},{"ann_type_code":"TMXKSQ","ann_type":"商标使用许可备案公告"},{"ann_type_code":"TMXKBG","ann_type":"商标使用许可变更公告"},{"ann_type_code":"TMXKZZ","ann_type":"商标使用许可终止公告"},{"ann_type_code":"TMZYSQ","ann_type":"商标质权登记公告"},{"ann_type_code":"TMZCZX","ann_type":"注册商标注销公告"},{"ann_type_code":"TMXZZX","ann_type":"注册商标未续展注销公告"},{"ann_type_code":"TMCXSQ","ann_type":"注册商标撤销公告"},{"ann_type_code":"TMXGWX","ann_type":"注册商标宣告无效公告"},{"ann_type_code":"TMZCCH","ann_type":"商标注册申请撤回公告"},{"ann_type_code":"TMWXGG","ann_type":"无效公告"},{"ann_type_code":"TMZCYS","ann_type":"商标注册证遗失声明公告"},{"ann_type_code":"TMSDGG","ann_type":"送达公告"},{"ann_type_code":"TMYYSQ","ann_type":"商标异议公告"},{"ann_type_code":"TMYYCD","ann_type":"商标异议裁定公告"},{"ann_type_code":"TMYFCD","ann_type":"商标异议复审裁定公告"},{"ann_type_code":"TMZCGY","ann_type":"共有人注册商标"},{"ann_type_code":"TMZCCM","ann_type":"驰名商标公告"},{"ann_type_code":"TMZCWX","ann_type":"商标注册证无效公告"},{"ann_type_code":"TMBMZJ","ann_type":"变更集体/证明商标申请人名义地址/管理规则成员名单公告"},{"ann_type_code":"TMZRZJ","ann_type":"集体/证明商标申请人名义地址/成员名单管理规则转让/移转公告"},{"ann_type_code":"TMBQSQ","ann_type":"商标其他注册事项变更公告"},{"ann_type_code":"TMQTGG","ann_type":"商标其他事项公告"},{"ann_type_code":"TMXKCX","ann_type":"商标使用许可合同备案撤销公告"},{"ann_type_code":"TMQTCX","ann_type":"关于商标的处理决定撤销公告"},{"ann_type_code":"TMSBSD","ann_type":"商标申请补正通知书送达公告"},{"ann_type_code":"TMZCSD","ann_type":"准予撤回商标注册申请决定书送达公告"},{"ann_type_code":"TMSYSD","ann_type":"商标注册申请审查意见书送达公告"},{"ann_type_code":"TMBTSD","ann_type":"商标注册申请驳回通知书送达公告"},{"ann_type_code":"TMTSSD","ann_type":"提供注册商标使用证明通知书送达公告"},{"ann_type_code":"TMCJSD","ann_type":"撤销注册商标决定书送达公告"},{"ann_type_code":"TMYCSD","ann_type":"商标异议裁定书送达公告"},{"ann_type_code":"TMQTSD","ann_type":"其他商标书件送达公告"},{"ann_type_code":"TMBHZR","ann_type":"商标评审委员会驳回转让复审决定公告"},{"ann_type_code":"TMCXZY","ann_type":"商标评审委员会注册商标争议裁定公告"},{"ann_type_code":"TMCXBD","ann_type":"商标评审委员会撤销注册不当商标申请议裁定公告"},{"ann_type_code":"TMZFJD","ann_type":"商标评审委员会撤销注册商标复审决定公告"},{"ann_type_code":"TMDBSD","ann_type":"商标评审委员会答辩通知书送达公告"},{"ann_type_code":"TMCDSD","ann_type":"商标评审委员会裁(决)定通知书送达公告"},{"ann_type_code":"TMXWZX","ann_type":"注册人死亡/终止注销注册商标公告"},{"ann_type_code":"TMSBJG","ann_type":"商标局公告"},{"ann_type_code":"TMTYGG","ann_type":"通用公告"}]'
    jsonData = json.loads(jsonContent)

    for i in list(jsonData):
        db.annType.insert_one(i)

annnum_code_add()






######################################################################################################################## end




######################################################################################################################## Test start
