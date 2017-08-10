import os
import re
import urllib
from urllib.error import ContentTooShortError

import requests
from bs4 import BeautifulSoup
from requests import RequestException



def get_html(url):
    try:
        response = requests.get(url);
        if(response.status_code==200):
            return response.text;
    except RequestException as e:
        print("错误");
        return None;

def main(url):
    return get_html(url);
def get_pic_url(html):
    if html:
        soup = BeautifulSoup(html)
        patterns = re.compile(r'src="(.*?)".*?',re.S);
        items = re.findall(patterns,html);
        return items;
    return None;

def download_pic(items,start):
    if items:
        os.mkdir('D:\\images\\' + str(start));
        for imgurl in items:
            if imgurl.endswith("jpg") or imgurl.endswith("gif"):
                print("开始下载" + imgurl);
                try:
                    #print(os.path.split(imgurl)[1]);
                    urllib.request.urlretrieve(imgurl, 'D:\\images\\' + str(start) + "\\" + os.path.split(imgurl)[1]);
                    print("保存路径" + 'D:\\images\\' + str(start) + "\\")
                    print(imgurl + "下载完毕");
                except ValueError as e:
                    #print(e);
                    continue;
                except ContentTooShortError as e1:
                    continue;
    return ;
if __name__ == '__main__':
    for i in range (21,100):
        url = "http://www.papapatu.net/"
        print("换页");
        #start = start+i;
        url = url + str(i) + '.html';
        #print(url);
        #url = '';
        html = main(url);
        #print(html)
        #break;
        items = get_pic_url(html)
        for item in items:
            print(item);
        #break;
        download_pic(items,i);
        #url = "http://p1.pstatp.com/origin/2edf00047eff1b0af103";
        #urllib.request.urlretrieve(url,'D:\\images\\' + "aa.jpg");
