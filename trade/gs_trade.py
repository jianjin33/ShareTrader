class TradeParams:
    def __init__(self, dt, price):
        self.dt = dt
        self.price = price


class Order:
    def __init__(self):
        self.id = None
        self.buy_datetime = ''
        self.buy_price = 0
        self.sell_datetime = ''
        self.sell_price = 0
        self.volume = 0
        self.pnl = .0


class GSATrade(object):
    def __init__(self, cash) -> None:
        # 持仓信息，dict字典
        self._current_orders = {}
        # 历史订单信息
        self._history_orders = {}
        self._order_num = 0
        # 初始资金
        self._cash = cash

    # 根据可用资金计算开仓数量
    @staticmethod
    def calculate_volume(cash, price):
        return int(cash / price / 100) * 100

    # 统计每单交易收益
    @staticmethod
    def stat_pnl(order: Order):
        buy_amount = order.buy_price * order.volume
        sell_amount = order.sell_price * order.volume
        diff_amount = sell_amount - buy_amount
        order.pnl = (diff_amount
                     - buy_amount * (5 / 1_0000)  # 千分之0.5印花税
                     - sell_amount * (1 / 1_0000)  # 万一券商佣金
                     )

    def exist_order(self) -> bool:
        return len(self._current_orders) > 0

    def buy(self, params: TradeParams):
        if not self.exist_order():
            self._order_num += 1
            key = 'order-' + str(self._order_num)

            order = Order()
            order.id = key
            order.buy_datetime = params.dt
            order.buy_price = params.price
            order.volume = self.calculate_volume(self._cash, params.price)

            self._current_orders[key] = order
            self._cash -= order.volume * order.buy_price
            # 调用券商提供接口逻辑
            print('Buy - Price: {0}, Volume: {1}, Cash: {2}'.format(
                order.buy_price, order.volume, self._cash))

    def sell(self, params: TradeParams):
        if self.exist_order():
            key = list(self._current_orders.keys())[0]
            order: Order = self._current_orders[key]
            order.sell_datetime = params.dt
            order.sell_price = params.price

            self._cash += order.volume * order.sell_price
            self.stat_pnl(order)
            self._history_orders[key] = self._current_orders.pop(key)
            # 调用券商提供接口逻辑
            print('Sell - Price: {0}, PnL: {1}, Volume: {2}, Cash: {3}'.format(
                order.sell_price, order.pnl, order.volume, self._cash))

    def get_history_orders(self):
        return self._history_orders

    def get_current_orders(self):
        return self._current_orders

    def get_cash(self):
        return self._cash
