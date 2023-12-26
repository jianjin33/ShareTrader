# _*_ coding: utf-8 -*-

from time import sleep
from pywinauto.application import Application
from pywinauto.keyboard import send_keys


def start():
    while True:
        try:
            app = Application(backend="uia").start(
                'D:/Program Files/同花顺/xiadan.exe', timeout=10)
            # 窗口置顶
            win = app.top_window()
            return app, win
        except Exception as e:
            print(e)
            app = Application(backend="uia").connect(
                path='D:/Program Files/同花顺/xiadan.exe')
            if app is not None:  # 如果已有应用在运行，则尝试杀死进程
                app.kill()
            sleep(3)  # 等待一会再尝试启动


class ThsTrader:
    @staticmethod
    def buy(code: str, price: float, amount: int):
        price = str(price)
        amount = str(amount)
        print('code:{0} price:{0} amount{1}'.format(code, price, amount))
        app, win = start()
        try:
            # win.set_focus()
            sleep(1)
            f4_tree_item = app.top_window().child_window(
                title="查询[F4]", control_type="TreeItem")
            # f4_tree_item = app.top_window()['TreeItem9', '查询[F4]TreeItem', '查询[F4]']
            print(f4_tree_item)
            f4_tree_item.set_focus()

            send_keys('{F1}')
            sleep(1)
            print('input code')
            send_keys(code)
            sleep(1)
            send_keys('{TAB}')
            send_keys('{BACK 6}')
            sleep(0.5)
            print('input price')
            send_keys(price)
            send_keys('{TAB}')
            sleep(0.5)
            print('input amount')
            send_keys(amount)
            send_keys('{TAB}')
            sleep(0.5)
            send_keys('{ENTER 3}')
            app.kill()
            return 'buy ok'
        except Exception as e:
            app.kill()
            return e

    @staticmethod
    def sell(code: str, price: float, amount: int):
        price = str(price)
        amount = str(amount)
        print('code:{0} price:{0} amount{1}'.format(code, price, amount))

        app, win = start()
        win.set_focus()
        try:
            sleep(1)
            f4_tree_item = app.top_window().child_window(
                title="查询[F4]", control_type="TreeItem")
            f4_tree_item.set_focus()

            send_keys('{F2}')
            sleep(0.5)
            print('input code')
            send_keys(code)
            sleep(0.5)
            send_keys('{TAB}')
            send_keys('{BACK 6}')
            sleep(0.5)
            print('input price')
            send_keys(price)
            send_keys('{TAB}')
            sleep(0.5)
            print('input amount')
            send_keys(amount)
            send_keys('{TAB}')
            send_keys('{ENTER 3}')
            app.kill()
            return 'sell ok'
        except Exception as e:
            app.kill()
            return e

    @staticmethod
    def cancel():
        app, win = start()
        sleep(0.5)
        try:
            win.set_focus()
            sleep(0.5)
            send_keys('{F3}')
            sleep(0.5)
            send_keys('{TAB 2}')
            send_keys('{ENTER}')
            sleep(0.5)
            send_keys('{ENTER}')
            sleep(3)
            app.kill()
            return 'cancel ok'
        except Exception as e:
            app.kill()
            return e


def for_test():
    # start方法为打开对于exe程序
    # 已经开启程序，重复调start会抛异常 raise RuntimeError("No windows for that process could be found")
    app = Application(backend="uia").start('D:/Program Files/同花顺/xiadan.exe')
    sleep(1)
    print(app.top_window().dump_tree())
    # 直接调用dump_tree不完整，因为window打开需要一定时间，需要一定等待
    # 通过tree 获取window或child window，通过id或TreeItem名称，找出并操作TreeItem
    # Pane - ''    (L0, T0, R0, B0)
    # ['Pane', 'Pane0', 'Pane1']
    # None


# if __name__ == '__main__':
#     # for_test()
#     trader = ThsTrader()
#     print(trader.buy('003030', 16.37, 100))
#     print(trader.sell('003030', 25.55, 100))
