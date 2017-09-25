import tushare as ts
import os
result = ts.get_sz50s()
#print(result['code'].tolist())
if not os.path.exists('D:/history//code'):
    os.mkdir('D://history//code')


for code in result['code'].tolist():
    '''
    code：股票代码，即6位数字代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
    start：开始日期，格式YYYY-MM-DD
    end：结束日期，格式YYYY-MM-DD
    ktype：数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
    retry_count：当网络异常后重试次数，默认为3
    pause:重试时停顿秒数，默认为0
    '''
    gegu = ts.get_hist_data(code=code,start='2017-07-01',end='2017-09-01')
    f = open('D://history' + '//code' + '//' + code + 'history.csv', 'w')
    #f = open('D://history' + '//code' + '//' + code + 'history.csv', 'wb')
    gegu.to_csv('D://history' + '//code' + '//' + code + 'history.csv')