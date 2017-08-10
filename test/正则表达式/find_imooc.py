import re;
#str = 'imooc_python'
#pattern = re.compile(r'imooc_');
#ma = pattern.match(str);
#print(ma.group());
#print(ma.span());
#print(ma.string);


#str2 = 'ImoOc PYTHON';
#pattern = re.compile(r'(imooc)',re.I);
#ma = pattern.match(str2);
#print(ma.group());
#print(ma.groups());
#print(ma.string);


#ma = re.match(r'a','a');
#print(ma.group());

#ma = re.match(r'a','b');
#type(ma);

#ma = re.match(r'.','b');
#print(ma.group())

#ma = re.match(r'.','5');
#print(ma.group());

#ma = re.match(r'{.}','{a}');
#print(ma.group())

#ma = re.match(r'{.}','{0}');
#print(ma.group())

#ma = re.match(r'{[abc]}','{a}');
#print(ma.group());

#ma = re.match(r'{[abc]}','{d}');
#print(ma.group());

#ma = re.match(r'{[a-z]}','{d}');
#print(ma.group());

#ma = re.match(r'{[a-zA-Z]}','{B}');
#print(ma.group());

#ma = re.match(r'{[a-zA-Z0-9]}','{6}');
#print(ma.group());

#ma = re.match(r'{\w}','{n}');
#print(ma.group());

#ma = re.match(r'{\W}','{`}');
#print(ma.group());

#ma = re.match(r'{\W}','{ }');
#print(ma.group())

#ma = re.match(r'\[[\w]\]','[a]');
#print(ma.group());

#ma = re.match(r'\d','5')
#print(ma.group());

#ma = re.match(r'\D','d');
#print(ma.group());

#ma = re.match(r'[\w]{4,10}@163.com','imooc@163.com');
#print(ma.group());

#ma = re.match(r'[\w]{4,10}@163.com','imooc@163.comabc');
#print(ma.group());

#ma = re.match(r'[\w]{4,10}@163.com$','imooc@163.comabc');
#print(ma.group());

#ma = re.match(r'^[\w]{4,10}@163.com$','_imooc@163.com');
#print(ma.group());

#ma = re.match(r'\Aimooc[\w]*','imoocpython');
#print(ma.group());

#ma = re.match(r'\Aimooc[\w]*','iimoocpython');
#print(ma.group());

#ma = re.match(r'[1-9]?\d$','01');
#print(ma.group());

#ma = re.match(r'[1-9]?\d$','99');
#print(ma.group())

#ma = re.match(r'[1-9]?\d$|100','100');
#print(ma.group());

#ma = re.match(r'[\w]{4,6}@163.com','imooc@163.com');
#print(ma.group());

#ma = re.match(r'[\w]{4,6}@(163|126).com$','imooc@163.com');
#print(ma.group());

ma = re.match(r'[\w]{4,6}@(163|126).com$','imooc@126.com');
print(ma.group());