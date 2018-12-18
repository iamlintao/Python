# -*- coding: utf-8 -*-
# author:zxy
#Date:2018-9-19

import requests
import pymysql
import re
import time
import html
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
    response = requests.get(url, headers=HEADERS,timeout=120) #print(response.content.decode('gbk'))
    # text = response.text.encode("utf-8")  #拿到数据，，再解码
    text = response.content.decode('gbk',"ignore")      ##  ignore  解决编码问题
    html = etree.HTML(text)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    detail_urls=map(lambda url:BASE_DOMAIN+url,detail_urls)
    return detail_urls

def parse_detail_page(url):
    movie={}
    response=requests.get(url,headers=HEADERS)
    text=response.content.decode('gbk',"ignore")  #text = response.text.encode("utf-8")
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

            if info.startswith("◎国　　家"):
                info=parse_info(info,"◎国　　家")
                movie['country']=info

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
        movie['download_url']=download_url
        return movie

## 定义数组
# movies=[]
#
# def spider():
#     base_url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
#     for x in range(100,1,-1):  #how much page depend on you
#         # print("==="*30)
#         # print(x)
#         url=base_url.format(x)
#         detail_urls=get_detail_url(url)
#         for detail_url in detail_urls:
#             # print(detail_url)
#             movie=parse_detail_page(detail_url)
#             movies.append(movie)

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
                item = pymysql.escape_string(item)
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
                item = pymysql.escape_string(item)
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
                item = pymysql.escape_string(item)
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
                item = pymysql.escape_string(item)
                insert_sql = " insert into subtitle (subtitle_name) VALUE ('" + item + "') "
                cursor.execute(insert_sql)
                lastID = db.insert_id()
                db.commit()
                ids.append(lastID)

    return ",".join(str(i) for i in ids)


## 发布时间处理
def add_release(releaseTime):
    ids = [];

    ## 特出情况处理
    if releaseTime == '2014-06-06(美国/中国)':
        releaseTime = '2014-06-06(美国)/2014-06-06(中国)'

    if releaseTime == '2014-06-27(美国/中国大陆)':
            releaseTime = '2014-06-27(美国)/2014-06-27(中国)'


    release = releaseTime.split("/")
    for item in release:

        item = item.strip()

        ## 上映时间
        # _date =  re.search(r"(\d{4}-\d{1,2}-\d{1,2})",item)
        _date = re.search(r"(\d{4}(-\d{1,2})*)", item)

        releaseDate = _date.group(0)

        ## 上映地区
        # rep = re.compile(r'[(](.*?)[)]',re.S)
        # releaseArea = re.findall(rep, item)
        # releaseArea = releaseArea[0]

        ## 提取中文
        rep = re.compile("[\u4e00-\u9fa5]+")
        releaseArea = re.findall(rep, item)
        if releaseArea:
            releaseArea = releaseArea[0]
        else:
            releaseArea = ''

        if item:
            sql = " select id from released where release_time='" + releaseDate + "'  and release_area='" + releaseArea + "' "
            cursor.execute(sql)
            list = cursor.fetchone()

            if list:  ## 不为空
                ids.append(list[0])
            else:
                releaseDate = pymysql.escape_string(releaseDate)
                releaseArea = pymysql.escape_string(releaseArea)

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
        _score = pymysql.escape_string(_score)

        insert_sql = " insert into score (movie_id,score_type,score,from_user) values ('%s','%s','%s','%s' ) " % (movieID,typeID,_score,_users)
        cursor.execute(insert_sql)
        lastID = db.insert_id()
        db.commit()
        id = lastID

    return id


## 导演、演员处理
def add_worker(type,content):
    ids = []

    ## 导演的数据需要转换一下
    if type == 1:
        content = {content}

    for i in content:

        _name = i.split(' ',1)
        _name_cn = _name[0].replace("'", "_")  ## 中文名

        if len(_name) > 1:
            _name_en = _name[1].replace("'","_")     ## 英文名
        else:
            _name_en = ''

        sql = " select id from worker where worker_type=%s and worker_name_cn='%s' and worker_name_en='%s' " %(type,_name_cn,_name_en)
        cursor.execute(sql)
        rs = cursor.fetchone()

        if rs:  ## 不为空
            ids.append(rs[0])

        else:
            _name_cn = pymysql.escape_string(_name_cn)
            _name_en = pymysql.escape_string(_name_en)

            insert_sql = " insert into worker (worker_type,worker_name_cn,worker_name_en) VALUES (%s,'%s','%s')" %(type,_name_cn,_name_en)
            cursor.execute(insert_sql)
            lastID = db.insert_id()
            db.commit()
            ids.append(lastID)


    _ids = [str(j) for j in ids]
    _ids = ','.join(_ids)

    return _ids

## 下载地址处理
## 1 迅雷 2 电驴 3 百度网盘 4 ftp 5 magnet( 磁力链)
def add_download(movieID,downloadURL):
    id = ''

    ## 判断类型
    typeCode = downloadURL.split(":")[0]
    type = ''
    if typeCode == 'ftp':
        type = 4
    if typeCode == 'magnet':
        type = 5

    if typeCode == 'http':
        return ''

    else:
        # sql = " select id from download where movie_id=%s and download_type =%s and download_url='%s' " % (movieID,type,downloadURL)
        sql = " select id from download where download_url='%s' " % (downloadURL)
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


#########


if __name__ == '__main__':

    # ## 国家id
    # countryID = add_country('英国/')
    #
    # ## 分类id
    # categoryID = add_category('科幻/悬疑/惊悚')
    #
    # ## 语言id
    # languageID = add_language('英语/西班牙语')
    #
    # ## 字幕
    # subtitleID = add_subtitle('中英双字幕')
    #
    # ## 上映时间
    # release = add_release('2018-08-31(威尼斯电影节) / 2018-10-05(美国)')
    #
    # ## 评分,需要电影表主键和平台id：1 豆瓣 2 imdb
    # score = add_score(1,1,'5.3/10 from 19921 users')
    #
    # ## 导演和演员
    # act = add_worker(2,['查宁·塔图姆 Channing Tatum', '詹姆斯·柯登 James Corden', '赞达亚 Zendaya', '勒布朗·詹姆斯 LeBron James', '科曼 Common', '吉娜·罗德里格兹 Gina Rodriguez', '丹尼·德维托 Danny DeVito', '吉米·塔特罗 Jimmy Tatro', '雅拉·沙希迪 Yara Shahidi', '伊利·亨利 Ely Henry'])
    #
    # ## 下载地址
    # down = add_download(1,'magnet:?xt=urn:btih:3dcecfe415c6244a059ba4dfca0bdc5d3ef38759&amp;dn=%e9%98%b3%e5%85%89%e7%94%b5%e5%bd%b1www.ygdy8.com.%e5%bd%b1.HD.1080p.%e5%9b%bd%e8%af%ad%e4%b8%ad%e8%8b%b1%e5%8f%8c%e5%ad%97.mp4&amp;tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce&amp;tr=udp%3a%2f%2fthetracker.org%3a80%2fannounce&amp;tr=http%3a%2f%2fretracker.telecom.by%2fannounce')


    # spider()

    base_url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
    for x in range(61,0,-1):  # how much page depend on you
        url = base_url.format(x)

        print(url)

        detail_urls = get_detail_url(url)
        for detail_url in detail_urls:
            movies=[]

            movie = parse_detail_page(detail_url)

            if movie:
                movies.append(movie)

            for _movie in movies:
                info = {}   ## 定义字典

                info['_title'] = ''
                info['_short_title'] = ''
                info['_name_cn'] = ''
                info['_name_en'] = ''
                info['_cover'] = ''
                info['_year'] = ''
                info['_country'] = ''
                info['_category'] = ''
                info['_language'] = ''
                info['_sub_title'] = ''
                info['_release_time'] = ''
                info['_file_format'] = ''
                info['_ratio'] = ''
                info['_length'] = ''
                info['_director'] = ''
                info['_writers'] = ''
                info['_actors'] = ''
                info['_profiles'] = ''
                info['_imdb_score'] = ''
                info['_douban_score'] = ''

                for (key,value) in _movie.items():

                    ##   '_writers': '',
                    if key == 'writers':
                        info['_writers'] = add_worker(3,value)

                    ##   'title': '2018年悬疑《一个小忙/失踪网红》BD中英双字幕',
                    if key == 'title':
                        # info['_title'] = value
                        info['_title'] = value
                        info['_short_title'] = re.findall(r'[《](.*?)[》]', value)[0]

                    ##   'cover': 'https://extraimage.net/images/2018/12/12/78a6236c00693a056d28d726a12ae835.jpg',
                    if key == 'cover':
                        info['_cover'] = value

                    ##   'name_cn': '一个小忙/举手之劳/失踪网红(台)/小心帮忙(港)/简单帮个忙',
                    if key == 'name_cn':
                        info['_name_cn'] = value

                    ##   'name_en': 'A Simple Favor',
                    if key == 'name_en':
                        info['_name_en'] = value

                    ##   'year': '2018',
                    if key == 'year':
                        info['_year'] = value

                    ##   'country': '美国/加拿大',
                    if key == 'country':
                        info['_country'] = add_country(value)

                    ##   'category': '剧情/悬疑/犯罪',
                    if key == 'category':
                        info['_category'] = add_category(value)

                    ##   'language': '英语',
                    if key == 'language':
                        info['_language'] = add_language(value)

                    ##   'sub_title': '中英双字幕',
                    if key == 'sub_title':
                        info['_sub_title'] = add_subtitle(value)

                    ##   'release_time': '2018-09-14(美国)',
                    if key == 'release_time':
                        info['_release_time'] = add_release(value)

                    ## 'imdb_score': '7.1/10 from 28895 users',
                    if key == 'imdb_score':
                        info['_imdb_score'] = value

                    ## 'douban_score': '7.1/10 from 4109 users',
                    if key == 'douban_score':
                        info['_douban_score'] = value


                    ##   'file_format': 'x264 + aac',
                    if key == 'file_format':
                        info['_file_format'] = value

                    ##   'ratio': '1280 x 688',
                    if key == 'ratio':
                        info['_ratio'] = value

                    ##   'length': '117分钟',
                    if key == 'length':
                        info['_length'] = value

                    ##   'director': '保罗·费格 Paul Feig',
                    if key == 'director':
                        info['_director'] = add_worker(1,value)

                    ##   'actors': ['布蕾克·莱弗利 Blake Lively', ],
                    if key == 'actors':
                        info['_actors'] = add_worker(2,value)


                    ##   'profiles': ['', '故事讲述一博主史蒂芬娜（', ''],
                    if key == 'profiles':
                        _value = [str(i) for i in value]
                        info['_profiles'] = '<p/>'.join(_value)
                        info['_profiles'] = html.escape(info['_profiles'])


                    ##   'download_url': 'ftp://ygdy8:ygdy8@yg45.dydytt.net:8369/阳光电影www.ygdy8.com.一个小忙.BD.720p.中英双字幕.mkv'
                    if key == 'download_url':
                        info['_download_url'] = value

                # ## 主表操作
                ck_sql = " select id from movies where short_title='" + info['_short_title'] + "' "
                cursor.execute(ck_sql)
                ck = cursor.fetchone()

                if ck:  ## not empty
                    lastID = ck[0]
                else:
                    _thisTime = int(time.time())
                    in_sql = " insert into movies (title,short_title,name_cn,name_en,cover,publish_year,country,category,languages,sub_title,release_time,file_format,ratio,time_length,director,writers,actors,profiles,create_time) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(pymysql.escape_string(info['_title']), pymysql.escape_string(info['_short_title']), pymysql.escape_string(info['_name_cn']), pymysql.escape_string(info['_name_en']), info['_cover'], info['_year'],info['_country'], info['_category'], info['_language'], info['_sub_title'], info['_release_time'],info['_file_format'], info['_ratio'], info['_length'], info['_director'], info['_writers'], info['_actors'], pymysql.escape_string(info['_profiles']), _thisTime)
                    try:
                        cursor.execute(in_sql)
                        lastID = db.insert_id()
                        db.commit()
                    except:

                        ## 写入错入日志
                        f = open('error_sql.txt', 'a')
                        f.write(in_sql)
                        f.closed

                        print(in_sql)

                ## imdb评分
                if info['_imdb_score']:
                    add_score(lastID,2, info['_imdb_score'])

                ## 豆瓣评分
                if info['_douban_score']:
                    add_score(lastID,1,info['_douban_score'])


                if info['_download_url']:
                   add_download(lastID,info['_download_url'])



                print(info['_title'])
