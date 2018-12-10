#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import urllib.request
import ssl
from bs4 import BeautifulSoup
import re


def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    html = html.decode('gbk')
    return html


##########################################################################################  内容


ssl._create_default_https_context = ssl._create_unverified_context
url = "https://www.dytt8.net/html/gndy/dyzz/20181107/57755.html"
html = getHtml(url)
soup = BeautifulSoup(html,"html.parser")
content = soup.select('#Zoom')


strinfo = re.compile('\<strong>*</strong>')
b = strinfo.sub('-',content)


print(b)

##########################################################################################  列表

# ssl._create_default_https_context = ssl._create_unverified_context
# url = "https://www.dytt8.net/html/gndy/dyzz/index.html"
# html = getHtml(url)
#
# soup = BeautifulSoup(html,"html.parser")
# # list = soup.find_all('.co_content8 a')
# list = soup.select('a[class="ulink"]')
#
# for link in list:
#     print(link.name, link['href'], link.get_text())



## https://www.dytt8.net/html/gndy/dyzz/index.html


##########################################################################################

# html_doc = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>
# <p class="story">...</p>
# """
#
# soup = BeautifulSoup(html_doc,"html.parser")
# links = soup.find_all('a')
#
# for link in links:
#     print(link.name,link['href'],link.get_text())



#######################################################################

# import re
#
# print(re.findall("\bblow",'Jason blow cat'))
# print(re.findall("\\bblow",'Tom blow cat'))
# print(re.findall(r"\bblow",'Jar blow cat'))

# import urllib.request
# response = urllib.request.urlopen('http://www.iamlintao.com')
#
# # print("查看 response 的返回类型：",type(response))
# # print("查看反应地址信息: ",response)
# # print("查看头部信息1(http header)：\n",response.info())
# # print("查看头部信息2(http header)：\n",response.getheaders())
# # print("输出头部属性信息：",response.getheader("Server"))
# # print("查看响应状态信息1(http status)：\n",response.status)
# # print("查看响应状态信息2(http status)：\n",response.getcode())
# # print("查看响应 url 地址：\n",response.geturl())
#
# page = response.read()
# print("输出网页源码:",page.decode('utf-8'))



# import mysql.connector
# conn = mysql.connector.connect(user='root',password='',database='zuiw')
# db = conn.cursor()
#
# list = db.execute('select * from partner_recommend limit 10 ')
# value = db.fetchall()
# for con in value:
#     print(con)


# f = open('hetong.txt','r')
#
# print(f.read())
#
# f.close()


# class Student(object):
#     pass
#
#
# s = Student()
# s.name = 'tom'
#
# print(s.name)


# class Student(object):
#
#     def __init__(self,name,score):
#         self.name = name
#         self.score = score
#
#     def get_grade(self):
#         if self.score >= 90:
#             return 'A'
#         elif self.score >=60:
#             return 'B'
#         else:
#             return 'C'
#
#
#
# bart = Student('tom',101)
# print(bart.name,bart.get_grade())

# import sys
#
# def test():
#     args = sys.argv
#     if len(args) == 1:
#         print('hello,world!')
#     elif len(args) == 2:
#         print('Hello, %s!' % args[1])
#     else:
#         print(' Too many arguments!')
#
# if __name__ == '__main__':
#     test()


# def lazy_sum(*args):
#     def sum():
#         ax = 0
#         for n in args:
#             ax = ax + n
#         return ax
#     return sum
#
#
# f = lazy_sum(1,2,3,4,5,6)
# print(f())


# def getSum(x):
#     num = 0
#     j = x+1
#     for i in list(range(j)):
#         num = num + i
#     return num


# a = getSum(100)
# print(a)

# arr = list(range(1,101,2))
# print(arr[-30:-5:4])


# bb = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# print(bb[4:20:3])

# print([x+y for x in range(1,101,2) for y in range(2,101,2)])

# g = (x+y for x in range(1,101,2) for y in range(2,101,2))
#
# for i in g:
#     print(next(g))