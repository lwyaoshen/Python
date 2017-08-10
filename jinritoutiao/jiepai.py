import json
import os
import re
import urllib
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from requests import RequestException


def get_page_index(offset,keyword):
    data={
        'offset': offset,
        'format':'json',
        'keyword':keyword,
        'autoload':'true',
        'count':'20',
        'cur_tab':3
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code ==200:
            return response.text
        return None
    except RequestException as e:
        print('请求出错')
        return None
def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException as e:
        return None
def parse_page_detail(html):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    print(title)

    os.mkdir("D://jinritoutiao//" + title)
    pattern = re.compile('gallery: (.*?)]},',re.S)
    result = re.search(pattern,html)
    if result:
        #print(result.group(1))
        data = json.loads(result.group(1) + ']}')
        print(data)

        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            print(sub_images)
            images = [item.get('url') for item in sub_images]
            for image in images:
                print('开始下载图片' + image)
                urllib.request.urlretrieve(image, 'D:\\jinritoutiao\\' + title + "\\" + os.path.split(image)[-1] + '.jpg');
                print(image + '下载完毕')
            '''
            return {
                'title':title,
                'images':images,
            }
            '''

def main():
    html = get_page_index(0,'街拍')
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            parse_page_detail(html)
        #print(url)
    #print(html)

if __name__ =='__main__':
    os.mkdir("D://jinritoutiao//")
    main()