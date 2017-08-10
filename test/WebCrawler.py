from urllib import request

class WebClraler:
    def getHtml(url):
        html = request.urlopen("http://www.baidu.com");
        content = html.read();
        html.close();
        return content;
if __name__ == '__main__':
    content = WebClraler.getHtml("http://www.baidu.com");
    print(content);