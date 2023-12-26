from matplotlib import gridspec
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.dates import date2num
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data.base_data import BaseDataLoader as DL
from strategy.ma20_15 import MA20Minute15
from trade.gs_trade import GSATrade

plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False


class Backtester:
    def __init__(self):
        self.open = []
        self.equities = []

    # 净值计算
    def stat_equity(self, trade: GSATrade):
        current_orders = trade.get_current_orders()
        cash = trade.get_cash()

        asset = 0
        for order in current_orders.values():
            asset += self.open[0] * order.volume  # 收盘价 * 持仓
        equity = asset + cash
        self.equities.append(equity)

    def run_backtesting(self, ticks, ma: MA20Minute15):
        is_init = False
        for tick in ticks:
            self.open.insert(0, tick[1])
            if is_init:
                ma.strategy(tick[0], tick[1])
                # 统计每个周期结束时净值
                self.stat_equity(ma.trade)
            else:
                if len(self.open) >= 20:
                    is_init = True
                    ma.strategy(tick[0], tick[1])

    def stat_backtesting_result(self):
        orders_dict = trade_instance.get_history_orders()

        profit_orders = 0
        loss_orders = 0
        pnl_dict = {}
        pnl_result = 0
        for key in orders_dict.keys():
            pnl = orders_dict[key].pnl
            pnl_dict[key] = pnl
            pnl_result += pnl
            if pnl >= 0:
                profit_orders += 1
            else:
                loss_orders += 1
        print('All PNL:' + str(pnl_result))

        # 计算胜率
        win_rate = profit_orders / len(orders_dict)
        loss_rate = loss_orders / len(orders_dict)
        print('win_rate:{0} \n loss_rate:{1}'.format(win_rate, loss_rate))
        # win_rate:0.6666666666666666
        # loss_rate:0.3333333333333333

        # 推导式提取Order对象部分属性，并创建DataFrame
        df_data = {
            'id': [order.id for order in orders_dict.values()],
            'buy_datetime': [order.buy_datetime for order in orders_dict.values()],
            'buy_price': [order.buy_price for order in orders_dict.values()],
            'sell_datetime': [order.sell_datetime for order in orders_dict.values()],
            'sell_price': [order.sell_price for order in orders_dict.values()],
            'PNL': [order.pnl for order in orders_dict.values()],
        }

        orders_df = pd.DataFrame(df_data)
        orders_df.set_index(keys='id', inplace=True)
        print(orders_df)

        # 创建一个 Figure 对象和两个子图 Axes 对象
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(10, 7), sharex=False, height_ratios=[1, 1, 2])

        # ax1绘制PNL
        pnl_series = orders_df.loc[:, 'PNL']
        ax1.plot(pnl_series.index, pnl_series, color='b')
        ax1.bar(pnl_series.index, pnl_series, width=0.3, label='PNL', color=np.where(pnl_series >= 0, 'b', 'r'))
        ax1.set_title('每单PNL')
        ax1.set_ylabel('PNL')
        ax1.legend()
        ax1.grid()

        # ax2绘制净值曲线
        equities_series = pd.Series(self.equities)
        ax2.plot(equities_series, label='净值')
        ax2.set_title('净值')
        ax2.set_xticks([])
        ax2.set_ylabel('Equity')
        ax2.legend()
        ax2.grid()

        # ax3绘制蜡烛图，标记买卖点
        bar_15_df = pd.read_csv(get_data_path(),
                                usecols=['datetime', 'open', 'high', 'low', 'close'],
                                parse_dates=['datetime'])
        bar_15_df.loc[:, 'datetime'] = [date2num(x) for x in bar_15_df.loc[:, 'datetime']]
        candlestick_ohlc(
            ax3,
            bar_15_df.values,
            width=0.2,
            colorup='r',
            colordown='g',
            alpha=1.0,
        )
        for index, row in orders_df.iterrows():
            ax3.plot([row['buy_datetime'], row['sell_datetime']],
                     [row['buy_price'], row['sell_price']],
                     color='b',
                     marker='o')
        ax3.set_title('买卖点')
        ax3.set_xlabel('日期')
        ax3.set_ylabel('价格')
        ax3.legend()
        ax3.grid()

        # 调整布局
        plt.tight_layout()
        plt.show()


def get_data_path():
    stock_code = DL.get_stock_code('003030')
    path = DL.get_data_path(stock_code)
    print('backtesting data local path:' + path)
    return path


def get_data_for_backtesting():
    df = pd.read_csv(get_data_path(),
                     index_col='datetime',
                     parse_dates=['datetime'])
    tick_list = []
    for index, row in df.iterrows():
        tick_list.append((index, row['close']))
    # 再转为numpy的array
    ticks = np.array(tick_list)
    return ticks


# 初始回测资金
INIT_CASH = 50_000

if __name__ == '__main__':
    ticks_data = get_data_for_backtesting()
    trade_instance = GSATrade(cash=INIT_CASH)
    ma_strategy = MA20Minute15(trade_instance)

    backtester = Backtester()
    backtester.run_backtesting(ticks_data, ma_strategy)
    backtester.stat_backtesting_result()
