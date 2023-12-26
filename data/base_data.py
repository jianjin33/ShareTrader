from enum import Enum


class Interval(Enum):
    """
    各周期
    """
    MINUTE_1 = '1'
    MINUTE_5 = '5'
    MINUTE_15 = '15'
    MINUTE_30 = '30'
    MINUTE_60 = '60'  # 1h


LOCAL_DATA_DIR = '\\Workspaces\\ShareTrader\\data\\'


class BaseDataLoader(object):
    name: str = object

    """
    获取当前股票历史数据
    """

    def load_history(self, Params):
        pass

    """
    通过股票代码首字符判断交易所
    """

    @staticmethod
    def get_stock_prefix(stock_code):
        firstChar = stock_code[0]
        if firstChar == '6':
            prefix = 'sh'
        elif firstChar == '3':
            prefix = 'sz'
        elif firstChar == '0':
            prefix = 'sz'
        else:
            raise Exception('unknown stock code')
        return prefix

    @staticmethod
    def get_original_data_path(stock_code):
        return LOCAL_DATA_DIR + stock_code + '.csv'

    @staticmethod
    def get_data_path(stock_code):
        return LOCAL_DATA_DIR + stock_code + '_process.csv'


class DataParams:
    code = ''
    # 2023-9-11
    start_time = ''
    end_time = ''
    interval: Interval = None
