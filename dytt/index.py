# -*- coding: utf-8 -*-
# author:zxy
#Date:2018-9-19

import requests
import pymysql
import re
import json
from lxml import etree

##  链接数据库配置
db = pymysql.connect("localhost","root","","p7dy")
cursor = db.cursor()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/67.0.3396.99 Safari/537.36'
}
BASE_DOMAIN="http://www.dytt8.net"


def get_detail_url(url):
    response = requests.get(url, headers=HEADERS) #print(response.content.decode('gbk'))
    text = response.text.encode("utf-8")  #拿到数据，，再解码
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    detail_urls=map(lambda url:BASE_DOMAIN+url,detail_urls)
    return detail_urls

def parse_detail_page(url):
    movie={}
    response=requests.get(url,headers=HEADERS)
    text=response.content.decode('gbk')  #text = response.text.encode("utf-8")
    html=etree.HTML(text)
    title=html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
    # for x in title:
    #     print(etree.tostring(x,encoding="utf-8").decode("utf-8"))
    #print(title)
    movie['title']=title
    Zoome=html.xpath("//div[@id='Zoom']")[0] #return list
    imgs=Zoome.xpath(".//img/@src")
    #print(cover)
    if imgs:        ## 如果存在图片则继续执行
        cover=imgs[0]
        # screenshot=imgs[1]
        movie['cover']=cover
        # movie['screenshot']=screenshot  not all movie has screenshot ,so discard for this moment

        def parse_info(info,rule):
            return info.replace(rule,"").strip()

        infos=Zoome.xpath(".//text()")

        for index,info in enumerate(infos):
            if info.startswith("◎年　　代"):
                info=parse_info(info,"◎年　　代")
                movie['year']=info
            elif info.startswith("◎译　　名"):
                info=parse_info(info,"◎译　　名")
                movie['name_cn']=info
            elif info.startswith("◎片　　名"):
                info=parse_info(info,"◎片　　名")
                movie['name_en']=info
            elif info.startswith("◎产　　地"):
                info=parse_info(info,"◎产　　地")
                movie['country']=info
            elif info.startswith("◎类　　别"):
                info=parse_info(info,"◎类　　别")
                movie['category']=info
            elif info.startswith("◎语　　言"):
                info=parse_info(info,"◎语　　言")
                movie['language']=info
            elif info.startswith("◎字　　幕"):
                info=parse_info(info,"◎字　　幕")
                movie['sub_title']=info
            elif info.startswith("◎上映日期"):
                info=parse_info(info,"◎上映日期")
                movie['release_time']=info
            elif info.startswith("◎IMDb评分"):
                info=parse_info(info,"◎IMDb评分")
                movie['imdb_score']=info
            elif info.startswith("◎豆瓣评分"):
                info=parse_info(info,"◎豆瓣评分")
                movie['douban_score']=info
            elif info.startswith("◎文件格式"):
                info=parse_info(info,"◎文件格式")
                movie['file_format']=info
            elif info.startswith("◎视频尺寸"):
                info=parse_info(info,"◎视频尺寸")
                movie['ratio']=info
            elif info.startswith("◎片　　长"):
                info=parse_info(info,"◎片　　长")
                movie['length']=info
            elif info.startswith("◎导　　演"):
                info=parse_info(info,"◎导　　演")
                movie['director']=info
            elif info.startswith("◎主　　演"):
                info=parse_info(info,"◎主　　演")
                actors=[info]
                for x in range(index+1,len(infos)):
                    actor=infos[x].strip()
                    if actor.startswith("◎"):
                        break
                    actors.append(actor)
                movie['actors']=actors
            elif info.startswith("◎简　　介"):
                info=parse_info(info,"◎简　　介")
                profiles=[info]
                for x in range(index+1,len(infos)):
                    profile=infos[x].strip()
                    if profile.startswith("【下载地址】"):
                        break
                    profiles.append(profile)
                    movie['profiles']=profiles
        download_url=html.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
        #print(download_url)
        movie['download_url']=download_url
        return movie

## 定义数组
movies=[]

def spider():
    base_url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
    for x in range(1,2):  #how much page depend on you
        # print("==="*30)
        # print(x)
        url=base_url.format(x)
        detail_urls=get_detail_url(url)
        for detail_url in detail_urls:
            # print(detail_url)
            movie=parse_detail_page(detail_url)
            movies.append(movie)

## 国家字段处理，返回逗号分隔的id
def add_country(countryName):

    ids = [];
    country = countryName.split("/")
    for item in country:

        if item:
            sql = "select id from country where country_name='"+item+"' "
            cursor.execute(sql)
            list = cursor.fetchone()

            if list:        ## 不为空
                ids.append(list[0])
            else:
                insert_sql= " insert into country (country_name) VALUE ('"+item+"') "
                cursor.execute(insert_sql)
                lastID = db.insert_id()
                db.commit()
                ids.append(lastID)

    return ",".join(str(i) for i in ids)

## 分类处理
def add_category(actegoryName):

    ids = [];
    actegory = actegoryName.split("/")
    for item in actegory:
        item = item.strip()
        if item:
            sql = "select id from category where category_name='" + item + "' "
            cursor.execute(sql)
            list = cursor.fetchone()

            if list:  ## 不为空
                ids.append(list[0])
            else:
                insert_sql = " insert into category (category_name) VALUE ('" + item + "') "
                cursor.execute(insert_sql)
                lastID = db.insert_id()
                db.commit()
                ids.append(lastID)

    return ",".join(str(i) for i in ids)

## 语言处理
def add_language(languageName):
    ids = [];
    language = languageName.split("/")
    for item in language:

        if item:
            sql = "select id from language where language_name='" + item + "' "
            cursor.execute(sql)
            list = cursor.fetchone()

            if list:  ## 不为空
                ids.append(list[0])
            else:
                insert_sql = " insert into language (language_name) VALUE ('" + item + "') "
                cursor.execute(insert_sql)
                lastID = db.insert_id()
                db.commit()
                ids.append(lastID)

    return ",".join(str(i) for i in ids)

## 字幕处理
def add_subtitle(subtitleName):

    ids = [];
    subtitle = subtitleName.split("/")
    for item in subtitle:

        if item:
            sql = "select id from subtitle where subtitle_name='" + item + "' "
            cursor.execute(sql)
            list = cursor.fetchone()

            if list:  ## 不为空
                ids.append(list[0])
            else:
                insert_sql = " insert into subtitle (subtitle_name) VALUE ('" + item + "') "
                cursor.execute(insert_sql)
                lastID = db.insert_id()
                db.commit()
                ids.append(lastID)

    return ",".join(str(i) for i in ids)


## 发布时间处理
def add_release(releaseTime):
    ids = [];
    release = releaseTime.split("/")
    for item in release:

        item = item.strip()

        ## 上映时间
        _date =  re.search(r"(\d{4}-\d{1,2}-\d{1,2})",item)
        releaseDate = _date.group(0)

        ## 上映地区
        rep = re.compile(r'[(](.*?)[)]',re.S)
        releaseArea = re.findall(rep, item)
        releaseArea = releaseArea[0]

        if item:
            sql = " select id from released where release_time='" + releaseDate + "'  and release_area='" + releaseArea + "' "
            cursor.execute(sql)
            list = cursor.fetchone()

            if list:  ## 不为空
                ids.append(list[0])
            else:
                insert_sql = " insert into released (release_time,release_area) VALUE ('" +releaseDate+ "','"+releaseArea+"') "
                cursor.execute(insert_sql)
                lastID = db.insert_id()
                db.commit()
                ids.append(lastID)

    return ",".join(str(i) for i in ids)

## 评分处理
def add_score(movieID,typeID,scoreContent):
    ids = ''

    ## 提取评分和人数
    _split = scoreContent.split(" ")
    _score = _split[0].split('/')[0]
    _users = _split[2]

    sql = " select id from score where movie_id=%d and score_type=%d " %(movieID,typeID)
    cursor.execute(sql)
    rs = cursor.fetchone()

    if rs: ## 不为空
        update_sql = " update score set score='%s',from_user='%s' where id='%s' " %(_score,_users,rs[0])
        cursor.execute(update_sql)
        db.commit()
        id = rs[0]

    else:
        insert_sql = " insert into score (movie_id,score_type,score,from_user) values ('%s','%s','%s','%s' ) " % (movieID,typeID,_score,_users)
        cursor.execute(insert_sql)
        lastID = db.insert_id()
        db.commit()
        id = lastID

    return id


## 导演、演员处理
def add_worker(type,content):
    ids = []

    for i in content:

        _name = i.split(' ',1)
        _name_cn = _name[0]     ## 中文名
        _name_en = _name[1]     ## 英文名

        sql = " select id from worker where worker_type=%s and worker_name_cn='%s' and worker_name_en='%s' " %(type,_name_cn,_name_en)
        cursor.execute(sql)
        rs = cursor.fetchone()

        if rs:  ## 不为空
            ids.append(rs[0])

        else:
            insert_sql = " insert into worker (worker_type,worker_name_cn,worker_name_en) VALUES (%s,'%s','%s')" %(type,_name_cn,_name_en)
            cursor.execute(insert_sql)
            lastID = db.insert_id()
            db.commit()
            ids.append(lastID)

    return ids


def add_download(movieID,type,downloadURL):
    id = ''

    sql = " select id from download where movie_id=%s and download_type =%s and download_url='%s' " % (movieID,type,downloadURL)
    cursor.execute(sql)
    rs = cursor.fetchone()

    if rs:  ## 不为空
        id = rs[0]
    else:
        insert_sql = " insert into download (movie_id,download_type,download_url) VALUES (%s,'%s','%s')" % (movieID,type,downloadURL)
        cursor.execute(insert_sql)
        lastID = db.insert_id()
        db.commit()
        id = lastID

    return id


if __name__ == '__main__':

    ## 国家id
    countryID = add_country('英国/')

    ## 分类id
    categoryID = add_category('科幻/悬疑/惊悚')

    ## 语言id
    languageID = add_language('英语/西班牙语')

    ## 字幕
    subtitleID = add_subtitle('中英双字幕')

    ## 上映时间
    release = add_release('2018-08-31(威尼斯电影节) / 2018-10-05(美国)')

    ## 评分,需要电影表主键和平台id：1 豆瓣 2 imdb
    score = add_score(1,1,'5.3/10 from 19921 users')

    ## 导演和演员
    act = add_worker(2,['查宁·塔图姆 Channing Tatum', '詹姆斯·柯登 James Corden', '赞达亚 Zendaya', '勒布朗·詹姆斯 LeBron James', '科曼 Common', '吉娜·罗德里格兹 Gina Rodriguez', '丹尼·德维托 Danny DeVito', '吉米·塔特罗 Jimmy Tatro', '雅拉·沙希迪 Yara Shahidi', '伊利·亨利 Ely Henry'])

    ## 下载地址
    down = add_download(1,1,'ftp://ygdy8:ygdy8@yg45.dydytt.net:3155/阳光电影www.ygdy8.com.网络谜踪.BD.720p.中英双字幕.mkv')
    print(down)




    # spider()
    # for movie in movies:
    #     for (key,value) in movie.items():
    #
    #         print(key)
    #         print(value)
    #
    #     exit()