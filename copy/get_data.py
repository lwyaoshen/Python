import pdb
import tushare as ts
import pandas
import os
import time
import json

import sys


import elasticsearch
import util
import datacube
import config

es_client = elasticsearch.Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])

start = '2016-09-01'
end = '2017-09-02'

#不晓得
def get_head():
    df = ts.get_index()
    df.to_csv('./head/dapan.csv')

    time.sleep(60)
    df = ts.get_industry_classified()
    df.to_csv('./head/gegu.csv')

    time.sleep(60)
    df = ts.get_stock_basics()
    df.to_csv('./head/gegu_basic.csv')


def get_data(code, start, end, type):
    fpath = util.define_file_path(code, start, end, type, config.domain_data)
    if os.path.exists(fpath):
        print
        '%s exists' % fpath
        return 1
    if type == 'dapan':
        df = ts.get_h_data(code, index=True, start=start, end=end)
    elif type == 'gegu':
        df = ts.get_hist_data(code, start=start, end=end)
    elif type == 'fenbi':
        df = ts.get_tick_data(code, date=start)
    if not isinstance(df, pandas.DataFrame) or df.empty:
        print('get data failed. code:', code)
        return 1
    df.to_csv(fpath)
    print('write data, %s' % fpath)
    return 0


def get_data_dapan():
    dapans = datacube.get_all_dapan()
    for (code, name) in dapans:
        get_data(code, start, end, 'dapan')
        time.sleep(60)


def get_data_gegu():
    ret = datacube.get_all_gegu()
    for cname, codes in ret.items():
        for (code, name) in codes:
            r = get_data(code, start, end, 'gegu')
            if r == 0:
                time.sleep(60)


def get_shishifenbi(fp):
    ret = datacube.get_all_gegu()
    allcodes = []
    columns = ['name', 'open', 'pre_close', 'price', 'high', 'low', 'bid', 'ask', 'volume', 'amount', 'b1_v', 'b1_p',
               'b2_v', 'b2_p', 'b3_v', 'b3_p', 'b4_v', 'b4_p', 'b5_v', 'b5_p', 'a1_v', 'a1_p', 'a2_v', 'a2_p', 'a3_v',
               'a3_p', 'a4_v', 'a4_p', 'a5_v', 'a5_p', 'date', 'time', 'code']
    fp.write(','.join(columns) + '\n')
    for cname, codes in ret.items():
        allcodes.extend([x[0] for x in codes])

    index = 0
    while index < len(allcodes):
        slice = allcodes[index:index + 30]
        index += 30

        df = ts.get_realtime_quotes(slice)

        for index, data in df.iterrows():
            row = [data[x] for x in columns]
            fp.write(','.join(row) + '\n')

        time.sleep(1)


def get_data_shishifenbi():
    t = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    fpath = './fenbi/%s.csv' % (t)
    fp = open(fpath, 'w')
    while True:
        get_shishifenbi(fp)


def get_increment_data():
    dapans = datacube.get_all_dapan()
    for (code, name) in dapans:
        if 0 == get_data(code, config.increment_start, config.increment_end, config.type_dapan):
            time.sleep(10)

    ret = datacube.get_all_gegu()
    for cname, codes in ret.items():
        for (code, name) in codes:
            r = get_data(code, config.increment_start, config.increment_end, config.type_gegu)
            if r == 0:
                time.sleep(5)


def merge_data():
    dapans = datacube.get_all_dapan()
    for (code, _) in dapans:
        max_columns = None
        columns, datas1 = datacube.get_data(config.domain_data, config.type_dapan, code)
        if not columns:
            datas1 = []
        else:
            max_columns = columns
        columns, datas2 = datacube.get_data(config.domain_data, config.type_dapan, code, config.increment_start,
                                            config.increment_end)
        if not columns:
            datas2 = []
        else:
            max_columns = columns

        if not max_columns:
            continue
        datas2.extends(datas1)
        datacube.save_data(max_columns, datas2, config.domain_data, type, code, config.start, config.increment_end)

    ret = datacube.get_all_gegu()
    for cname, codes in ret.items():
        for (code, name) in codes:
            max_columns = None
            columns, datas1 = datacube.get_data(config.domain_data, config.type_gegu, code)
            if not columns:
                datas1 = []
            else:
                max_columns = columns
            columns, datas2 = datacube.get_data(config.domain_data, config.type_gegu, code, config.increment_start,
                                                config.increment_end)
            if not columns:
                datas2 = []
            else:
                max_columns = columns

            if not max_columns:
                continue
            datas2.extends(datas1)
            datacube.save_data(max_columns, datas2, config.domain_data, type, code, config.start, config.increment_end)


if __name__ == '__main__':
    get_increment_data()
    merge_data()
# get_head()
#     get_data_dapan()
#     get_data_gegu()
#     get_data_fenbi()
#     get_data_shishifenbi()




