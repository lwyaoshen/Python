import pdb
import tushare as ts
import pandas
import os
import time
import sys
import json



import util
import config
import datacube

#导出管理器类
#封装了一个pipeline_tasks list
class ExtractExecutor(object):
    def __init__(self):
        self.pipeline_tasks = []

    def add_task(self, pipeline_task):
        self.pipeline_tasks.append(pipeline_task)

    def execute(self):
        for pipeline_task in self.pipeline_tasks:
            columns, datas = pipeline_task.pipeline()
            datacube.save_data(columns, datas, pipeline_task.domain, pipeline_task.type, pipeline_task.code,
                               pipeline_task.date_start, pipeline_task.date_end)


class ExtractPipeline(object):
    def __init__(self, type, code, date_start=config.start, date_end=config.end):
        self.domain = config.domain_extract
        self.type = type
        self.code = code
        self.date_start = date_start
        self.date_end = date_end

        self.target_functions = []

    def pipeline(self):
        '''
            输出csv格式的columns，datas
        '''
        raise Exception('you must implement this function')


default_target_func = lambda data, index, column_index: data[column_index]
none_target_func = lambda data, index, column_index: None



def preclose_target_func(closes, index):
    return closes[index + 1] if index < len(closes) - 1 else closes[index]

def change_target_func(closes, index):
    return (closes[index] - closes[index + 1]) / closes[index + 1] if index < len(closes) - 1 else 0

def ma_target_func(n, closes, index):
    return sum(closes[index:index+n])/len(closes[index:index+n])

def v_ma_target_func(n, volumes, index):
    return sum(volumes[index:index+n])/len(volumes[index:index+n])

def fangliang_target_func(closes, volumes, index):
    ma20 = ma_target_func(20, closes, index)
    v_ma20 = v_ma_target_func(20, volumes, index)
    return closes[index] > ma20 and volumes[index] >= v_ma20




