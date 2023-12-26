from base_data import (BaseDataLoader as DL,
                       DataParams,
                       Interval)
import pandas as pd


class DataProcesser(object):
    def _process_minute_k(self, params: DataParams):
        pass

    def process(self, params: DataParams):
        data_path = DL.get_original_data_path(params.code)
        print(data_path)
        df = pd.read_csv(data_path)

        if params.interval in (Interval.MINUTE_1,
                               Interval.MINUTE_5,
                               Interval.MINUTE_15,
                               Interval.MINUTE_30,
                               Interval.MINUTE_60):
            self._process_minute_k(params)
            # 推导式处理time列，int转str，截取丢弃后三位0
            df['time'] = [str(t)[:-3] for t in df['time']]
            # 通过pd将 20231107150000 转为 2023-11-07 15:00:00
            df['time'] = pd.to_datetime(df['time'])
            # time重命名为datatime
            df.rename(columns={'time': 'datetime'}, inplace=True)
        else:
            raise 'process not impl'

        process_data_path = DL.get_data_path(params.code)
        df.to_csv(process_data_path, index=False)
