from data_baostock import *
from data_processer import DataProcesser

data_loader = BaoStockDataLoader()

params_15m = DataParams()
params_15m.code = '003030'
params_15m.start_time = '2022-12-26'
params_15m.end_time = '2023-12-25'
params_15m.interval = Interval.MINUTE_15

data_loader.load_history(params_15m)

data_processer = DataProcesser()
data_processer.process(params_15m)
