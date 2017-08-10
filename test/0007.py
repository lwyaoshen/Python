import os
def count(path):
    codeNumber, blank, comments = 0, 0, 0;
    files = open(path,'rb');
    for line in files:
        line = line.strip();
        if line =='':
            blank+=1;
        if len(line)>0 and line[0] =='#':
            comments+=1;
        else:
            codeNumber+=1;
    files.close();
    return codeNumber,blank,comments;

if __name__ == '__main__':
    path = os.getcwd();
    #print(path)
    for list in os.listdir(path):

        if list=='.idea':
            continue;
        path = os.path.join(path,list);
        #print(list)
        codeNumber,blank,comments = count(path);
        print(list + "/代码行数：" + str(codeNumber) + "/空白行:" + str(blank) + "/注释行数：" + str(comments));
        path = os.getcwd();






