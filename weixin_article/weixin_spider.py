from urllib.parse import urlencode

import requests
import pyquery as pq
import pymongo
from lxml.etree import XMLSyntaxError

from requests.exceptions import  ConnectionError
proxy = None
MAX_COUNT = 5
client = pymongo.MongoClient('localhost')
db = client['weixin']

base_url = 'http://weixin.sogou.com/weixin?'
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'SUV=005E5558B7E47373595119B547CE5454; CXID=D2BD1E488383C206A063F3CB7309433E; ad=IZllllllll2B0Dm0lllllVuP$BllllllHMSZvyllll9lllllpklll5@@@@@@@@@@; SUID=8E72E4B75E68860A59584F580003E89D; IPLOC=CN5000; pgv_pvi=7771967488; pgv_si=s1871873024; ABTEST=0|1504018496|v1; SNUID=4ACF5A09BFBAE85B278E9FBABFFC8E5E; weixinIndexVisited=1; sct=2; JSESSIONID=aaaQ_w4ZqyVT1gcsoQi4v; ppinf=5|1504018986|1505228586|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo3OlByaXZhdGV8Y3J0OjEwOjE1MDQwMTg5ODZ8cmVmbmljazo3OlByaXZhdGV8dXNlcmlkOjQ0Om85dDJsdVBVSC1XSG5FY1NsWlJ1bktGTFktVE1Ad2VpeGluLnNvaHUuY29tfA; pprdig=sGN54rMPxeYXZOAkv0mlIiim33jdZyZVHOfBD7TVWzAMpO3CUWRIon7N88g4O9fIBo1RxB-KWhkfYfzJzBQw7rJC3Ctfy-4K9avybUV6q5lG7ipSSW08aS0BQHn5drs9xK9M2uFtY5VxmJDmmxxwaVrUWaCYJ7MuYFwoW36aFP0; sgid=08-30641481-AVmlgiapibBicp88YV9W9L3WiaM; ppmdig=1504018986000000e3f857e43baff5770beae511c62e08f8',
    'Host':'weixin.sogou.com',
    'Referer':'http://weixin.sogou.com/weixin?query=%E9%A3%8E%E6%99%AF&type=2&page=72&ie=utf8',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'
}

def parse_index(html):
    doc = pq(html)
    detail_hrefs = doc('news-box .news-list li .txt-box h3 a').items()
    for detail_href in detail_hrefs:
        yield detail_href.attr['href']



def get_random_proxy():
    url = 'http://localhost:5000/get'
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.text
        else:
            return None
    except ConnectionError as e:
        return None
def get_html(url,count = 1):
    global proxy
    print('Crawling',url)
    print('count times',count)
    if(count>MAX_COUNT):
        print('too many times request')
        return None
    try:

        if proxy:
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }
            response = requests.get(url,allow_redirects=False,headers = headers,proxies = proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code==200:
            return response.text
        if response.status_code==302:
            proxy = get_random_proxy()
            count = count+1
            if proxy:
                print('Using proxy ' + proxy)
                return get_html(url,count)
            else:
                print('Get proxy failed')
                return None
    except ConnectionError as e:
        proxy = get_random_proxy()
        count = count+1
        return get_html(url,count)


def get_index(query,page):
    data = {'query': query,
            'type': '2',
            'page': page}
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html
def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.text
        else:
            return None
    except ConnectionError as e:
        return None
def parse_detail(html):
    try:
        doc = pq(html)
        title = doc('.rich_media_title').text()
        content = doc('.rich_media_content').text()
        date = doc('#post-date').text()
        nickname = doc('rich_media_meta_list rich_media_meta rich_media_meta_text rich_media_meta_nickname').text()
        return{
            'title':title,
            'content':content,
            'date':date,
            'nickname':nickname
        }
    except XMLSyntaxError as e:
        return None

def save_to_mongo(data):
    if db['articles'].update({'title':data['title']},{'$set':data},True):
        print('save success')
    else:
        print('save failed')


if __name__ =='__main__':
    for i in range(1,101):
        html = get_index('风景',i)
        if html:
            detail_hrefs = parse_index(html)
            for detail_href in detail_hrefs:
                html = get_detail(detail_href)
                if html:
                    data = parse_detail(html)
                    print('结果------------' + str(data))
                    if data:
                        save_to_mongo(data)
