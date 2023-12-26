
class TradeParams():
    def __init__(self):
        pass

    dt = ''
    price = 0


class Order():
    def __init__(self):
        pass

    id = None
    open_datetime = ''
    open_price = 0
    close_datetime = ''
    close_price = 0
    volume = 0
    pnl = .0


class GSATrade(object):

    def __init__(self, cash) -> None:
        # 持仓信息，dict字典
        self._current_orders = {}
        # 历史订单信息
        self._history_orders = {}
        self._order_num = 0
        # 初始资金
        self._cash = cash

    def exist_order(self) -> bool:
        return len(self._current_orders) > 0

    # 根据可用资金计算开仓数量
    def calculate_volume(self, price: int):
        return int(self._cash / price / 100) * 100

    # 统计每单交易收益
    def stat_pnl(self, order: Order):
        buy_amount = order.open_price * order.volume
        sell_amount = order.close_price * order.volume
        diff_amount = sell_amount - buy_amount
        order.pnl = (diff_amount
                     - buy_amount * (5 / 1_0000)  # 千分之0.5印花税
                     - sell_amount * (1 / 1_0000)  # 万一券商佣金
                     )

    def buy(self, params: TradeParams):
        if not self.exist_order():
            self._order_num += 1
            key = 'order-' + str(self._order_num)

            order = Order()
            order.id = key
            order.open_datetime = params.dt
            order.open_price = params.price
            order.volume = self.calculate_volume(params.price)

            self._current_orders[key] = order
            self._cash -= order.volume * order.open_price
            print('buy price:{0},volumn:{1},cash:{2}'.format(
                order.open_price, order.volume, self._cash))

    def sell(self, params: TradeParams):
        if self.exist_order():
            key = list(self._current_orders.keys())[0]
            order: Order = self._current_orders[key]
            order.close_datetime = params.dt
            order.close_price = params.price

            self._cash += order.volume * order.close_price
            self.stat_pnl(order)
            self._history_orders[key] = self._current_orders.pop(key)
            print('sell price:{0},pnl:{1},volume:{2},cash:{3}'.format(
                order.close_price, order.pnl, order.volume, self._cash))

    def get_history_orders(self):
        return self._history_orders

    def get_current_orders(self):
        return self._current_orders

    def get_cash(self):
        return self._cash
