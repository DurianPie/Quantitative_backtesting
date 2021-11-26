from src.Stock import *


class IOManager:

    @staticmethod
    def __parse_data(data):
        """
        处理输入
        :param data:
        :return: {"股票名称": Stock对象}
        """
        stocks = {}
        for key, val in data.items():
            nan_data = val.isna()
            rows, cols = list(val.index), list(val.columns)
            for row in rows:
                day_info = []
                for col in cols:
                    if nan_data[col][row]:
                        # 缺失值过滤
                        break
                    day_info.append(val[col][row])
                if stocks.__contains__(row):
                    stocks[row].insert({key: day_info})
                else:
                    stock = Stock(row, {key: day_info})
                    stocks.update({row: stock})
        for key, val in stocks.items():
            val.sort_by_date()
        for key, val in stocks.items():
            val.get_all_info()
        return stocks

    @staticmethod
    def read_file(file_path):
        import pickle
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        # print(data)
        return IOManager.__parse_data(data)
