#coding=utf-8
import urllib.request
import re

# data=urllib.request.urlopen("http://www.shuju.net/data-info.html").read().decode("utf-8")
# pat='<div class="title">(.*?)</div>'
# res=re.compile(pat).findall(data)
#
# fh=open("log.txt","w")
#
# for i in range(0,len(res)):
#     print(res[i])
#     fh.write(res[i]+"\n")
# fh.close()

file = urllib.request.urlopen("http://iamlintao.com")

print(file.info())

print(file.getcode())

print(file.geturl())