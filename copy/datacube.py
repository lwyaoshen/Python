# -*- coding: utf-8 -*-
import pdb
import tushare as ts
import pandas
import os
import time
import json

from collections import OrderedDict

import sys


import util
import config

#保存数据
#params：
#columns:有哪些列
#datas:数据来源
#domain:不晓得干嘛的
#type:类别
#code:股票代码
#date_start:起始时间
#date_end:结束时间
#先通过code, date_start, date_end, type, domain去生成保存的路径以及文件名
#调用utils中的save_data方法写入数据
def save_data(columns, datas, domain, type, code, date_start=config.start, date_end=config.end):
    path = util.define_file_path(code, date_start, date_end, type, domain)
    util.save_data(path, columns, datas)



#从csv中获得数据
#params:
#domian:不晓得干嘛的
#type:类别
#code:股票代码
#date_start:开始时间
#date_end:结束时间
#先通过code, date_start, date_end, type, domain去确定读取路径
#再调用util.extract_data()获取数据
def get_data(domain, type, code, date_start=config.start, date_end=config.end):
    '''
        return columns, datas
    '''
    path = util.define_file_path(code, date_start, date_end, type, domain)
    return util.extract_data(path)

#返回所有股票的code,name.行业信息



def get_all_gegu():
    '''
        返回所有股票code、name、行业信息
        {hangye => [(code, name), (code, name), ... ]}
    '''
    hangye_gegu_map = {}
    gegu_hangye_path = './head/gegu_hangye_SH.csv'
    columns, datas = util.extract_data(gegu_hangye_path)
    codes = util.extract_columns(datas, columns, 'code')
    names = util.extract_columns(datas, columns, 'name')
    cnames = util.extract_columns(datas, columns, 'cname')

    for index, code in enumerate(codes):
        cname = cnames[index]
        name = names[index]
        hangye_gegu_map.setdefault(cname, [])
        hangye_gegu_map[cname].append((code, name))

    gegu_hangye_path = './head/gegu_hangye_SZ.csv'
    columns, datas = util.extract_data(gegu_hangye_path)
    codes = util.extract_columns(datas, columns, 'code')
    names = util.extract_columns(datas, columns, 'name')
    cnames = util.extract_columns(datas, columns, 'cname')

    for index, code in enumerate(codes):
        cname = cnames[index]
        name = names[index]
        hangye_gegu_map.setdefault(cname, [])
        hangye_gegu_map[cname].append((code, name))

    return hangye_gegu_map


def get_gegu_hangye():
    gegu_hangye_map = {}
    hangye_gegu_map = get_all_gegu()
    for hangye, code_names in hangye_gegu_map.items():
        for code, _ in code_names:
            gegu_hangye_map[code] = hangye
    return gegu_hangye_map


def get_all_hangye():
    '''
        返回所有行业
        [hangye1, hangye2, ... ]
    '''
    hangye_gegu_map = get_all_gegu()
    return hangye_gegu_map.keys()


def get_all_dapan():
    '''
        返回所有大盘code, name
        [(code, name), (code, name), ... ]
    '''
    dapans = []
    fpath = './head/dapan.csv'
    columns, datas = util.extract_data(fpath)
    codes = util.extract_columns(datas, columns, 'code')
    names = util.extract_columns(datas, columns, 'name')
    for index, code in enumerate(codes):
        dapans.append((code, names[index]))
    return dapans


def get_all_gegu_totals():
    '''
        返回个股股本总量, 股本总数 * 收盘价 = 股票市值
        {code => totals}
    '''
    code_totals_map = {}
    fpath = './head/gegu_basic.csv'
    columns, datas = util.extract_data(fpath)
    codes = util.extract_columns(datas, columns, 'code')
    totals = util.extract_columns(datas, columns, 'totals', float)
    for index, code in enumerate(codes):
        code_totals_map[code] = totals[index]
    return code_totals_map


def get_all_gegu_outstandings():
    '''
        返回个股流通股本数
        {code => outstanding}
    '''
    code_outstandings_map = {}
    fpath = './head/gegu_basic.csv'
    columns, datas = util.extract_data(fpath)
    codes = util.extract_columns(datas, columns, 'code')
    totals = util.extract_columns(datas, columns, 'outstanding', float)
    for index, code in enumerate(codes):
        code_outstandings_map[code] = totals[index]
    return code_outstandings_map


def get_hangye_gegu_datas(cname):
    max_columns = None
    hangye_gegu_datas = {}
    gegus = get_all_gegu()
    codes = gegus.get(cname)
    if not codes:
        return max_columns, hangye_gegu_datas

    for (code, name) in codes:
        columns, datas = get_data(config.domain_extract, config.type_gegu, code)
        if not columns:
            continue
        if not max_columns:
            max_columns = columns
        dates = util.extract_columns(datas, columns, 'date')

        hangye_gegu_datas[code] = OrderedDict()
        for index, date in enumerate(dates):
            hangye_gegu_datas[code][date] = datas[index]

    return max_columns, hangye_gegu_datas


gegu_columns_cache = None
gegu_datas_cache = None


def get_all_gegu_datas():
    '''
        返回个股详细数据
        columns: 字段列表
        datas: {cname => {code => {date => data}}}
        date遍历时有序, 从晚到早
    '''
    global gegu_columns_cache, gegu_datas_cache
    if gegu_datas_cache:
        return gegu_columns_cache, gegu_datas_cache

    max_columns = None
    gegu_datas = {}
    cnames = get_all_hangye()

    print
    'datacube read all_gegu_datas'
    for cname in cnames:
        print
        'datacube read %s hangye datas' % (cname)
        columns, hangye_gegu_datas = get_hangye_gegu_datas(cname)
        if not columns:
            continue
        if not max_columns:
            max_columns = columns
        gegu_datas[cname] = hangye_gegu_datas

    gegu_datas_cache = gegu_datas
    gegu_columns_cache = max_columns
    return max_columns, gegu_datas


hangye_columns_cache = None
hangye_datas_cache = None


def get_all_hangye_datas():
    '''
        返回行业详细数据
        columns: 字段列表
        datas: {cname => {date => data}}
        date遍历时有序, 从晚到早
    '''
    global hangye_columns_cache, hangye_datas_cache
    if hangye_datas_cache:
        return hangye_columns_cache, hangye_datas_cache

    max_columns = None
    hangye_datas = {}
    cnames = get_all_hangye()

    for cname in cnames:
        columns, datas = get_data(config.domain_extract, config.type_hangye, cname)
        if not columns:
            continue
        if not max_columns:
            max_columns = columns
        hangye_datas.setdefault(cname, {})
        dates = util.extract_columns(datas, columns, 'date')
        for index, date in enumerate(dates):
            hangye_datas[cname][date] = datas[index]

    gegu_datas_cache = hangye_datas
    gegu_columns_cache = max_columns
    return max_columns, hangye_datas


if __name__ == '__main__':
    #ret = get_all_hangye()
    #print
    #json.dumps(ret, ensure_ascii=False)
    #save_data(columns, datas, domain, type, code, date_start=config.start, date_end=config.end)
    #path = util.define_file_path(code, date_start, date_end, type, domain)
    #util.save_data(path, columns, datas)



    pass



