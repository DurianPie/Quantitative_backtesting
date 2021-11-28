class Stock:
    """
    单支股票信息
    """
    factor = ['open', 'close', 'high', 'low', 'volume', 'money', 'factor', 'avg',
              'pre_close', 'high_limit', 'low_limit', 'paused', 'change_pct',
              'change', 'amplitude', 'up_to_limit', 'down_to_limit', 'is_st',
              'boll_down', 'CR20', 'boll_up', 'growth', 'TRIX5', 'beta', 'VOL5',
              'WVAD', 'RSI', 'BBI', 'BIAS', 'MA', 'MTM', 'CCI', 'MACD', 'OBV', 'PSY']

    def __init__(self, name, info):
        self.__name = name
        self.__info = info

    def insert(self, day_info):
        self.__info.update(day_info)

    def get_all_info(self):
        """
        返回该股票的所有历史信息
        :return: {"2010-01-04": [open, close, high, ..., MACD, OBV, PSY], ...}
        """
        # print(self.__name, len(self.__info))
        # for key, val in self.__info.items():
        #     print(key, len(val))
        return self.__info

    def get_info_by_day(self, day):
        """
        返回一支股票在某一天的所有信息
        :param day:
        :return:
        """
        if self.__info.__contains__(day):
            return self.__info.get(day)
        else:
            # print("{} 股票在{}的信息不存在".format(self.__name, day))
            return None

    def get_val(self, day, key):
        if not Stock.factor.__contains__(key):
            print("关键字" + key + "错误")
            return None
        if not self.__info.__contains__(day):
            print("不含该天数据")
            return None
        return self.__info[day][Stock.factor.index(key)]

    def calculate_profit(self, start, end):
        """
        计算该股票在起止时间内的涨幅 (止收盘-起开盘)/起开盘
        首先二分到大于等于start的第一天，再二分到小于等于end的最后一天
        :param start:
        :param end:
        :return:
        """
        if start > end or (start == end and (not self.judge_day_valid(start))):
            print(start + " : " + end + " 日期不合法1")
            return None
        date = list(self.__info.keys())
        if start > date[len(date) - 1] or end < date[0]:
            print(start + " : " + end + " 日期不合法2")
            return None

        # 二分大于等于start的第一天
        l, r = 0, len(date) - 1
        mid = 0
        while l < r:
            mid = (l + r) // 2
            if date[mid] >= start:
                r = mid
            else:
                l = mid + 1
        start = date[mid]
        # 二分小于等于end的最后一天
        l, r = 0, len(date) - 1
        mid = 0
        while l < r:
            mid = (l + r + 1) // 2
            if date[mid] <= end:
                l = mid
            else:
                r = mid - 1
        end = date[mid]
        end_val = self.__info[end][Stock.factor.index("close")]
        start_val = self.__info[start][Stock.factor.index("open")]
        return (end_val - start_val) / start_val

    def sort_by_date(self):
        temp = {}
        for key in sorted(self.__info):
            temp[key] = self.__info[key]
        self.__info = temp

    def judge_day_valid(self, day):
        if (not self.__info.__contains__(day)) or str(self.__info[day][0]) == "nan":
            print(self.__name + "无" + day + "信息")
            return False
        return True
