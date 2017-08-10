#问题描述：任一个英文的纯文本文件，统计其中的单词出现的个数。

def count(readPath,writePath):
    file = open(readPath);
    content = file.read();
    words = content.split(" ");
    write = open(writePath,'w');


    dict = {}
    for word in words:
        if word in dict:
            dict[word]+=1;
        else:
            dict[word] = 1;
    dict = sorted(dict.items(),key = lambda dict:dict[1]);
    for a,b in dict:
        write.write(a + str(b) + '\n');

if __name__ == '__main__':
    count("C://read.txt","C://write.txt");



