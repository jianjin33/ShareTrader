import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from trade.gs_trade import GSATrade
from strategy.ma20_15 import MA20Minute15
from data.data_center import get_data_path


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'Arial Unicode MS'

open = []

# 初始资金
init_cash = 50_000

equitys = []


def get_data_for_backtesting():
    path = get_data_path('601038')
    print('backtesting data local path:' + path)
    df = pd.read_csv(path,
                     index_col='datetime',
                     parse_dates=['datetime'])
    tick_list = []
    for index, row in df.iterrows():
        tick_list.append((index, row['close']))
    # 再转为numpy的array
    ticks = np.array(tick_list)
    return ticks


# 净值计算
def stat_equity(orders, cash):
    asset = 0
    for order in orders.values():
        asset += open[0] * order.volume  # 收盘价 * 持仓
    return asset + cash


def run_backtesting(ticks, ma: MA20Minute15):
    is_init = False
    for tick in ticks:
        open.insert(0, tick[1])
        if is_init:
            ma.strategy(tick[0], tick[1])
            equity = stat_equity(
                ma.trade.get_current_orders(), ma.trade.get_cash())
            equitys.append(equity)
        else:
            if len(open) >= 20:
                is_init = True
                ma.strategy(tick[0], tick[1])


def stat_backtesting_result(orders):
    profit_orders = 0
    loss_orders = 0
    pnl_dict = {}
    pnl_result = 0
    for key in orders.keys():
        pnl = orders[key].pnl
        pnl_dict[key] = pnl
        pnl_result += pnl
        if pnl >= 0:
            profit_orders += 1
        else:
            loss_orders += 1
    print('all pnl:' + str(pnl_result))

    win_rate = profit_orders / len(orders)
    loss_rate = loss_orders / len(orders)
    print('win_rate:{0},loss_rate:{1}'.format(win_rate, loss_rate))
    # win_rate:0.6666666666666666
    # loss_rate:0.3333333333333333
    orders_series = pd.Series(pnl_dict)
    print(orders_series)
    # orders_series.plot.bar()

    orders_df = pd.DataFrame(orders_series).T
    print(orders_df)
    # orders_df.plot.bar()

    equitys_series = pd.Series(equitys)
    equitys_series.plot()
    plt.grid()

    plt.show()


if __name__ == '__main__':
    ticks = get_data_for_backtesting()
    trade = GSATrade(init_cash)
    ma = MA20Minute15(trade)
    run_backtesting(ticks, ma)
    orders = trade.get_history_orders()
    stat_backtesting_result(orders)
