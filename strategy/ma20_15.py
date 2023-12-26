
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from trade.gs_trade import (GSATrade,
                            TradeParams)

"""
简单策略：
15分钟级别，低于MA20 4%买，高于MA20 4%卖。
暂时不设置止损
"""


class MA20Minute15(object):
    def __init__(self, trade: GSATrade) -> None:
        self.trade = trade
        self._close = []

    def _buy(self, dt,  price):
        trade_params = TradeParams()
        trade_params.dt = dt
        trade_params.price = price
        self.trade.buy(trade_params)

    def _sell(self, dt, price):
        trade_params = TradeParams()
        trade_params.dt = dt
        trade_params.price = price
        self.trade.sell(trade_params)

    # 不使用TA-Lib，练习手动计算ma20也比较简单
    def _ma20(self, close):
        self._close.insert(0, close)
        sum = 0
        ma20 = 0
        for item in self._close[1:21]:
            sum += item
        ma20 = sum / 20
        return ma20

    def strategy(self, dt, close):
        ma20 = self._ma20(close)
        if close < 0.99 * ma20:
            self._buy(dt, close)
        elif close > 1.01 * ma20:
            self._sell(dt, close)
        else:
            pass
