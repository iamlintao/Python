#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
# 仅仅爬取首页IP地址就足够一般使用
from bs4 import BeautifulSoup
import requests
import random

def get_ip_list(url, headers):
  web_data = requests.get(url, headers=headers)
  soup = BeautifulSoup(web_data.text, 'html.parser')
  ips = soup.find_all('tr')
  ip_list = []
  for i in range(1, len(ips)):
    ip_info = ips[i]
    tds = ip_info.find_all('td')
    ip_list.append(tds[1].text + ':' + tds[2].text)
  return ip_list

def get_random_ip(ip_list):
  proxy_list = []
  for ip in ip_list:
    proxy_list.append('http://' + ip)
  proxy_ip = random.choice(proxy_list)
  proxies = {'http': proxy_ip}
  return proxies

if __name__ == '__main__':
  url = 'http://www.xicidaili.com/nn/'
  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'
  }
  ip_list = get_ip_list(url, headers=headers)
  proxies = get_random_ip(ip_list)

  print(proxies)    ## 函数get_ip_list(url, headers)传入url和headers，最后返回一个IP列表，列表的元素类似42.84.226.65:8888格式，这个列表包括国内髙匿代理IP网站首页所有IP地址和端口。