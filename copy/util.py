# -*- coding: utf-8 -*-
import pdb
import tushare as ts
import pandas
import os
import time
import sys
import json
import datetime
import elasticsearch
#sys.setdefaultencoding('utf-8')


#不晓得干嘛的
#params:
#message:
#kargs:
#ex:#info_message('hello',name='ys',age=22)
    #输出：hello,name [ys],age [22]
def info_message(message, **kargs):
    m = []
    m.append(message)
    for k, v in kargs.items():
        m.append('%s [%s]' % (k, v))
    print(','.join(m))


#拼接保存路径
#ex:./ history / 200_2017_09_01_2017_09_10_gegu.csv
def define_file_path(code, start, end, type, dir):
    return './%s/%s_%s_%s_%s.csv' % (dir, code, start, end, type)

#保存数据
#params:
#fpath:保存路径
#coluns:有哪些列
#datas:数据
def save_data(fpath, columns, datas):
    fp = open(fpath, 'w')
    fp.write(','.join(columns) + '\n')
    for data in datas:
        fp.write(','.join([str(x) for x in data]) + '\n')
    fp.close()



#从csv中导出数据
#params：
#fpath:路径
#return:
#column:有哪些列
#datas:数据
#ex:[['0', '600000', '浦发银行'], ['1', '600016', '民生银行']]
def extract_data(fpath):
    '''
        从csv文件中提取columns以及datas
    '''
    column = None
    datas = []
    if not os.path.exists(fpath):
        return column, datas
    for line in open(fpath):
        if not column:
            column = line.strip('\n').split(',')
            continue
        terms = line.strip('\n').split(',')
        if len(terms) != len(column):
            print('illegal line:', line)
            continue
        datas.append(terms)
    return column, datas



#导出某一列的所有数据
#params:
#datas:数据来源
#columns:有哪些列
#key:具体需要导出那一列
#f:指定方法，默认为str方法，将内容进行统一转换为字符串
#return:
#返回封装了某一列所有数据list<str>
def extract_columns(datas, columns, key, f = str):
    '''
        提取列数据
    '''
    index = columns.index(key) if key in columns else -1
    if index == -1:
        return None
    columns = []
    for x in datas:
        try:
            columns.append(f(x[index]))
        except Exception as e:
            columns.append(f('0'))
    return columns

one_day = datetime.timedelta(days = 1)

if __name__=='__main__':

    #info_message('hello',name='ys',age=22)
    #输出：hello,name [ys],age [22]

    #print(define_file_path(code='200', start='2017-09-01', end='2017-09-10', type='gegu', dir='history'))
    #输出：./ history / 200_2017 - 09 - 01_2017 - 09 - 10_gegu.csv

    #save_data()

    #column, datas = extract_data('D://history.csv')
    #print(column)
    #print(datas)
    #输出：['', 'code', 'name']
    #[['0', '600000', '浦发银行'], ['1', '600016', '民生银行']]

    #print(extract_columns(datas,column,'name',f=str))
    #输出：['浦发银行', '民生银行', '中国石化', '南方航空', '中信证券']
    pass