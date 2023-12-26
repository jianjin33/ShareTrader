from base_data import (BaseDataLoader as DL,
                       DataParams,
                       Interval)
import baostock as bs
import pandas as pd


# http://baostock.com/baostock/index.php
def _load_minute_k(params: DataParams):
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    # 获取沪深A股历史K线数据
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    # adjustflag 默认不复权：3；1：后复权；2：前复权
    rs = bs.query_history_k_data_plus(params.code,
                                      "date,time,code,open,high,low,close,volume,amount,adjustflag",
                                      start_date=params.start_time,
                                      end_date=params.end_time,
                                      frequency=params.interval.value,
                                      adjustflag="2")
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    # 结果集输出到csv文件
    path = DL.get_original_data_path(params.code)
    print("origin data path: {0}".format(path))
    result.to_csv(path, index=False)
    print(result)

    # 登出系统
    bs.logout()


class BaoStockDataLoader(DL):

    def load_history(self, params: DataParams):
        print('get stock info:{0}'.format(params.code))

        if params.interval in (Interval.MINUTE_1, Interval.MINUTE_5, Interval.MINUTE_15,
                               Interval.MINUTE_30, Interval.MINUTE_60):
            _load_minute_k(params)
        else:
            print('BaoStock non-supported interval:' + str(params.interval))
