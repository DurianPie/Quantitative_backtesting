"""
Author: nijing
date: 20211125
"""

from pickle import TRUE
from src.backtest.back_test_log import *
from src.Strategy import *
from src.IOUtils import *
from src.backtest.config import *
from src.backtest.eval_strategy import *

import random
import os

class BackTest:
    def __init__(self, author="zhangsan"):
        self.test_author = author
        self.test_info = [] # each item is a strategy test experiment
    

    def set_config(self, config):
        self.config = config

    def is_can_exchange(self, data, date, trade):
        """
        function for judyge whether can exchange in special day
        """
        accout_info = trade.GetAccoutInfo()
        daily_data = data.get_info_by_day(date.strftime('%Y-%m-%d'))
        for stock in accout_info.keys():
            if stock != 'cash' and stock not in daily_data:
                print("stock %s cannot query at %s" % (stock, date.strftime('%Y-%m-%d')))
                return False
        
        return True

    
    def test(self, data):
        """
        main test entrance
        """
        start = datetime.datetime.strptime(self.config.start_date, '%Y-%m-%d')
        end = datetime.datetime.strptime(self.config.end_date, '%Y-%m-%d')
        delta_day = end.__sub__(start).days

        delta_days_list = []

        if self.config.is_random:
            for i in range(self.config.n_sample):
                sample_deta_day = random.randint(0, delta_day)
                delta_days_list.append(sample_deta_day)
        else:
            # linear sample
            delta_days_list = [int(i * delta_day/self.config.n_sample) for i in range(self.config.n_sample)]
        
        print("start:end", start, end)
        print(delta_days_list)
        
        for i, delta_day in enumerate(delta_days_list):
            is_first_time = True
            new_start_date = start + datetime.timedelta(days=delta_day)
            trade = Trade()
            result = TestResult(self.config.strategy)

            if self.config.strategy == "strategy1":
                s = Strategy()  # 每隔7天卖出, 买入前7天股票跌入最大的
                date = new_start_date
                day_from_last_exchange = 0
                
                while date <= end:
                    day_from_last_exchange += 1
                    if is_first_time:
                        trade = Trade(self.config.init_cash)
                        is_first_time = False
                    ready_status = self.is_can_exchange(data, date, trade)
                    print("%s exchange status %d !" % (date.strftime('%Y-%m-%d'), ready_status))

                    if not ready_status:
                        date = date + datetime.timedelta(1)
                    else:
                        if day_from_last_exchange >= int(self.config.const_sold_interval):
                            print("run strategy at ", date.strftime('%Y-%m-%d'))
                            s.strategy_1(date.strftime('%Y-%m-%d'), data, trade)
                            day_from_last_exchange = 0
                    daily_data = data.get_info_by_day(date.strftime('%Y-%m-%d'))
                    asset, status = trade.GetTotalAsset(daily_data)
                    if not status:
                        print("cannot getAssetinfo at %s" % date.strftime('%Y-%m-%d'))
                    else:
                        print("asset %s at %f" % (date.strftime('%Y-%m-%d'), asset))
                        result.addInfo(date, asset)

                    date = date + datetime.timedelta(1)
            print("finish test %d" % i)
            self.test_info.append(result)

        print("finish test!")


    def eval(self):
        evaluator = EvalStrategy(self.config)
        if evaluator.is_positve_margin(self.test_info):
            return 1
        else:
            return 0

    def plot(self, backtest_logs):
        pass

    def get_test_log(self):
        return self.backtest_logs
    
    def save_eval_result(self):
        result_dir = "result/%s" % self.config.strategy
        os.makedirs(result_dir, exist_ok=True)
    
        for i in range(len(self.test_info)):
            with open("%s/test_%d" % (result_dir, i), "w") as wf:
                result = self.test_info[i]
                for date, asset in result.exchange_info.items():
                    line = "%s %f" %(date, asset)
                    wf.write(line)
                    wf.write("\n")


if __name__ == '__main__':
    data = IOUtils('data/data.pkl')
    # data = {}

    back_test = BackTest()

    config = BaseConfig()
    back_test.set_config(config)

    back_test.test(data)

    eval_result = back_test.eval()

    if eval_result:
        print ("after %d test, %s is good strategy!" % (int(config.n_sample), config.strategy))
    else:
        print ("after %d test, %s is bad strategy!" % (int(config.n_sample), config.strategy))
    
    back_test.save_eval_result()


