from src.IOManager import *


class IOUtils:
    """
    提供给策略的各种接口
    """

    def __init__(self, file_path):
        self.data = IOManager.read_file(file_path)

    def get_info_by_day(self, day):
        """
        返回所有股票在某一天的所有信息
        :param day:
        :return:
        """
        
        daily_data = {}
        for stock_name in self.data.keys():
            stock_data = self.data[stock_name].get_info_by_day(day)
            if stock_data != None:
                daily_data[stock_name] = stock_data
        return daily_data

    def find_largest_within(self, cur, k):
        """
        近k天涨幅最大的股票[max(0, cur-k+1)天开盘价...cur天的收盘价]
        :param k:
        :param cur:
        :return:
        """
        import datetime
        end = datetime.datetime.strptime(cur, '%Y-%m-%d').date()
        start = end - datetime.timedelta(days=k)
        maxv = -1e5
        name = []
        for key, val in self.data.items():
            profit = val.calculate_profit(str(start), str(end))
            if maxv < profit:
                name.clear()
                name.append(key)
                maxv = profit
            elif maxv == profit:
                name.append(key)
        return name


if __name__ == '__main__':
   strategy = IOUtils('data/data.pkl')
   res = strategy.find_largest_within('2019-04-01', 7)
   print(res)