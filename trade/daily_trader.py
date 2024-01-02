# _*_ coding: utf-8 -*-

from time import sleep
import requests
from dateutil import parser
from datetime import datetime, time
from data.base_data import BaseDataLoader as DL
from strategy.base_strategy import BaseStrategy
from strategy.ma20_15 import MA20Minute15
from trade.gs_trade import GSATrade

# https://qt.gtimg.cn/q=sz003030
STOCK_INFO_URL = 'https://qt.gtimg.cn/q='


class DailyTrader(object):
    def __init__(self, strategy: BaseStrategy):
        # 开盘价
        self._open = []
        # 收盘价
        self._close = []
        # 最高价
        self._high = []
        # 最低价
        self._low = []
        # 时间
        self._dt = []
        self._volume = []
        self._tick = None  # tuple元组数据
        self._last_bar_start_minute = None
        self._is_new_bar = False
        self._strategy = strategy

    # 通过股票代码获取股票信息
    def get_stock_info(self):
        prefix = DL.get_stock_prefix(stock_code)
        page = requests.get(STOCK_INFO_URL + prefix + stock_code)
        stock_info = page.text.split('~')

        open = float(stock_info[6])
        close = float(stock_info[4])
        high = float(stock_info[33])
        low = float(stock_info[34])
        # datetime = parser.parse(stock_info[30] + ' ' + stock_info[31])
        datetime = parser.parse(stock_info[30])
        print(stock_info)

        self._tick = (datetime, close)
        print(self._tick)

    def generate_bar(self):
        if len(self._high) == 0:
            self._open.insert(0, self._tick[1])
            self._close.insert(0, self._tick[1])
            self._high.insert(0, self._tick[1])
            self._low.insert(0, self._tick[1])
            self._dt.insert(0, self._tick[0])

        if self._tick[0].minute % 15 == 0 \
                and self._tick[0].minute != self._last_bar_start_minute:
            # create bar
            self._last_bar_start_minute = self._tick[0].minute
            self._open.insert(0, self._tick[1])
            self._close.insert(0, self._tick[1])
            self._high.insert(0, self._tick[1])
            self._low.insert(0, self._tick[1])
            self._dt.insert(0, self._tick[0])
            self._is_new_bar = True
            # 执行策略
            self._strategy.strategy(self._dt[0], self._close[0])
        else:
            # update bar
            self._high[0] = max(self._high[0], self._tick[1])
            self._low[0] = min(self._high[0], self._tick[1])
            self._close[0] = self._tick[1]
            self._dt[0] = self._tick[0]
            self._is_new_bar = False


if __name__ == '__main__':
    # prepare... ignore
    trade = GSATrade(cash=0)
    ma = MA20Minute15(trade)

    stock_code = '003030'
    daily_trader = DailyTrader(ma)

    while (time(9, 30) < datetime.now().time() < time(11, 30)
           or time(13) < datetime.now().time() < time(15)):
        daily_trader.get_stock_info()
        daily_trader.generate_bar()
        # importance
        sleep(10)
