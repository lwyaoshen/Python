import tushare as ts
import datetime
import config
import util
#第一个买入条件：10天之内出现2次250日的地量
#


def bought_in_condition_first(datas):

    object_list = list(map(q,datas));

    volume_list = list(map(f,datas))

    rest_list = volume_list[:-1]

    if volume_list[-1] == min(volume_list):

        three_to_seven_list = volume_list[-3:-7]
        for index,value in enumerate(three_to_seven_list):
            if min(rest_list) == value:
                index = rest_list.index(min(rest_list))
                final_index = -(7-index)
                object = object_list[final_index]

                config.second_lowest_amount['close_price'] = object['close_price']
                config.second_lowest_amount['date'] = object['date']

                object2 = object_list[-1]

                config.first_lowest_amount['close_price'] = object2['close_price']
                config.first_lowest_amount['date'] = object2['date']
                return True

        return False


    else:
        return False




def q(x):
    return {
        'close_price':x[3],
        'date':x[0]

    }

def f(x):
    return x[5]
def f1(x):
    return x[3]

def f2(x):
    return x[0]


#第二个买入条件：第二次地量对应收盘价>第一次地量收盘价
def bought_in_condition_second():
    return config.first_lowest_amount['close_price']>config.second_lowest_amount['close_price']

#第三个买入条件：两次地量出现的时间差在3-7天的闭区间之内
def bought_in_condition_third():
    interval = compare_date(config.first_lowest_amount['date'],config.second_lowest_amount['date'])
    return  interval>=3 and interval<=7



def compare_date(date1=None,date2=None):
    d1 = datetime.datetime.strptime(date1,'%Y-%m-%d')
    d2 = datetime.datetime.strptime(date2,'%Y-%m-%d')
    delta = d1 - d2
    return delta.days
#第一个卖出条件：当天收盘价 = 买入价格 * （1+0.05|1-0.05）
#以第二天开盘价卖出
def sale_out_condition_first():




    pass

if __name__ =='__main__':
    pass
    #print(type(compare_date()))

