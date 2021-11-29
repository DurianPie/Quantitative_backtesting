"""
Author: nijing
date: 20211125
"""
import collections

class TestResult:
    def __init__(self, strategy_name) -> None:
        self.strategy_name = strategy_name
        self.exchange_info = collections.OrderedDict()

    def addInfo(self, date, money, stock, asset, status):
        self.exchange_info[date] = {}
        self.exchange_info[date]['money'] = money
       # self.exchange_info[date].append(money)
        self.exchange_info[date]['stock'] = stock
        self.exchange_info[date]['asset'] =asset
        if status == 1:
            self.exchange_info[date]['status'] = 'Yep'
        else:
            self.exchange_info[date]['status'] = 'Nope'

    
    def size(self):
        return len(self.exchange_info)
    
    def is_positve_margin(self):
        if self.size() > 0:
            f_t = list(self.exchange_info.items())[0]
            e_t = list(self.exchange_info.items())[-1]
            first_list = list(f_t[1].items())
            last_list = list(e_t[1].items())

            first_item = first_list[2][1]
            last_item = last_list[2][1]
            if (last_item > first_item):
                return True
        return False



class EvalStrategy:
    def __init__(self, config) -> None:
        self.config = config

    def is_positve_margin(self, strategy_test_results):
        vaild_n = 0
        positve_margin_n = 0
        for test_result in strategy_test_results:
            if test_result.size() > 0:
                vaild_n += 1
                if test_result.is_positve_margin():
                    positve_margin_n += 1
        if positve_margin_n > 0 and positve_margin_n >= vaild_n * self.config.is_good_strategy_ratio:
            return True
        
        return False

