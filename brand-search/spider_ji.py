# -*- coding: utf-8 -*-
## 纪凤伟版本

import requests
from pymongo import MongoClient
import math
import time
import logging

logger = logging.getLogger('sbgg_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

session.get('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearch.html?annNum=1625', headers=headers)

client = MongoClient('mongodb://localhost:27017/')
db = client.publish1
C = db.publish1


def dopost(page,annNum):
    try:
        response = session.post('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearchDG.html', data={
            'page': page,
            'rows': 200,
            'annNum': annNum,
            'annType': None,
            'tmType': None,
            'recUserName': None,
            'allowUserName': None,
            'byAllowUserName': None,
            'appId': None,
            'coowner': None,
            'appIdZhiquan': None,
            'bfchangedAgengedName': None,
            'changeLastName': None,
            'transferUserName': None,
            'acceptUserName': None,
            'regName': None,
            'tmName': None,
            'intCls': None,
            'fileType': None,
            'totalYOrN': False,
            'appDateBegin': None,
            'appDateEnd': None,
        }, headers=headers)

        if response.status_code ==200:
            return response.json()
        else:
            return None
    except Exception as e:
        logger.error(e)
        print(e)

if __name__ == '__main__':
    for i in range(1,1626):
        print(i)
        data = dopost(1,i)
        if data is not None:
            for row in data.get('rows'):
                row.update({'_id': row.get('id')})
                C.insert_one(row)
            totalPage = math.ceil(data.get('total') / 200) + 1
            for p in range(2,totalPage):
                print(i,p)
                data = dopost(p,i)
                if data is not None:
                    for row in data.get('rows'):
                        row.update({'_id': row.get('id')})
                        C.insert_one(row)
                time.sleep(0.5)
