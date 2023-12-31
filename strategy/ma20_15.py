from strategy.base_strategy import BaseStrategy
from trade.gs_trade import (GSATrade,
                            TradeParams)

"""
简单策略：
15分钟级别，低于MA20 2%买，高于MA20 1%卖。
不设止损
"""


class MA20Minute15(BaseStrategy):
    def __init__(self, trade: GSATrade) -> None:
        self.trade = trade
        self._close = []

    def _buy(self, dt, price):
        trade_params = TradeParams(dt=dt, price=price)
        self.trade.buy(trade_params)

    def _sell(self, dt, price):
        trade_params = TradeParams(dt=dt, price=price)
        self.trade.sell(trade_params)

    # 不使用TA-Lib，手动计算ma20也比较简单
    def _ma20(self, close):
        self._close.insert(0, close)
        sum20 = 0
        for item in self._close[1:21]:
            sum20 += item
        return sum20 / 20

    def strategy(self, dt, close):
        ma20 = self._ma20(close)
        if close < 0.98 * ma20:
            self._buy(dt, close)
        elif close > 1.01 * ma20:
            self._sell(dt, close)
        else:
            pass
