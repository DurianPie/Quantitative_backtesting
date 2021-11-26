"""
Author: nijing
date: 20211125
"""

from src.backtest.back_test_log import *
from src.Strategy import *
from src.IOUtils import *
from src.backtest.config import *
import random


class BackTest:
    def __init__(self, author="zhangsan"):
        self.test_author = author
    

    def set_config(self, config):
        self.config = config


    def test(self, data):
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
        
        for delta_day in delta_days_list:
            is_init = True
            one_back_test = BackTest()
            new_start_date = start + datetime.timedelta(days=delta_day)
            T = Trade()
            if self.config.strategy == "strategy1":
                s = Strategy()
                # 每隔7天卖出, 买入前7天股票跌入最大的
                while new_start_date <= end:
                    if is_init:
                        T = Trade(self.config.init_cash)
                        is_init = False
                    s.strategy_1(new_start_date.strftime('%Y-%m-%d'), data, T)
                    print(type(new_start_date))
                    new_start_date = new_start_date +\
                           datetime.timedelta(days=int(self.config.const_sold_interval))
                    if (new_start_date > end):
                        #todo: too compute the final cost
                        final_cost = 0
                        self.backtest_logs = {}

    def eval(self, backtest_logs):
        # todo: to use log, but the current log cannot save clearly
        return 1


    def plot(self, backtest_logs):
        pass

    def get_test_log(self):
        return self.backtest_logs



if __name__ == '__main__':
    data = IOUtils('data/data.pkl')

    back_test = BackTest()
    config = BaseConfig()
    back_test.set_config(config)

    back_test.test(data)


    back_test_log = back_test.get_test_log()
    eval_result = back_test.eval(back_test_log)

    if eval_result:
        print ("good strategy!")
    else:
        print ("bad strategy!")

    
    



    
