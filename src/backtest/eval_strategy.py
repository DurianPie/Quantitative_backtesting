"""
Author: nijing
date: 20211125
"""
import collections

class TestResult:
    def __init__(self, strategy_name) -> None:
        self.strategy_name = strategy_name
        self.exchange_info = collections.OrderedDict()

    def addInfo(self, date, asset):
        self.exchange_info[date] = asset
    
    def size(self):
        return len(self.exchange_info)
    
    def is_positve_margin(self):
        if self.size() > 0:
            first_item = list(self.exchange_info.items())[0]
            last_item = list(self.exchange_info.items())[-1]
            if (last_item[1] > first_item[1]):
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

