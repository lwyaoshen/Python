import requests

response = requests.get('http://www.mzitu.com/92107/3')
max_num =  max_num = response.xpath('/html/body/div[3]/div[1]/div[4]/a[7]/span/text()').extract_first();
print(max_num)