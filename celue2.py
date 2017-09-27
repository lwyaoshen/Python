import json
import datacube
import config
import util
import tushare as ts
import condition
def output_hangye_fangliang(s, e):
    # date => [hangye]
    ret = {}
    hangyes = datacube.get_all_hangye()
    for hangye in hangyes:
        fpath = util.define_file_path(hangye, config.start, config.end, 'hangye', 'extract')
        columns, datas = util.extract_data(fpath)
        if not columns:
            print(fpath)
            continue
        dates = util.extract_columns(datas, columns, 'date')
        fangliangs = util.extract_columns(datas, columns, 'fangliang')
        pinghuans = util.extract_columns(datas, columns, 'pinghuanxiangshang')
        volumes = util.extract_columns(datas, columns, 'volume', float)
        v_ma10s = util.extract_columns(datas, columns, 'v_ma10', float)

        max_ratio  = 0
        max_data = None
        for (index, date) in enumerate(dates):
            if date < s or date > e:
                continue
            if fangliangs[index] == 'True' and pinghuans[index] == 'True':
                print(date, hangye)
                print(columns)
                print(json.dumps(datas[index], ensure_ascii=False))
                ret.setdefault(date, [])
                ret[date].append((hangye, datas[index]))
            # print columns
            # print json.dumps(datas[index], ensure_ascii=False)
    return ret



def output(s, e):
    result = []
    ret = output_hangye_fangliang(s, e)
    result = ts.get_stock_basics()
    code_list = result['code'].tolist()
    industry_list = result['industry'].tolist()

    for index,code in enumerate(code_list):
        fpath = util.define_file_path(dir=industry_list[index],
                                      code=code,
                                      start=config.start,
                                      end=config.end,
                                      type='extract'
                                      )
        columns, datas = util.extract_data(fpath)

        if condition.bought_in_condition_first(datas) and condition.bought_in_condition_second():
            result.append({'codes': code})














    print(result)



    for date, hangyes in ret.items():
        for (hangye,hangye_data) in hangyes:
            codes = output_gegu_top20_net_capital_inflow(date, hangye)
            result.append({'date': date, 'hangye': hangye, 'hangye_info':hangye_data, 'codes': codes})
    return result