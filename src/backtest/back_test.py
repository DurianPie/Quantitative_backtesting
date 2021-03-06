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
from src.log import *
import random
import os
import csv
import pandas as pd

class BackTest:
    def __init__(self, author="Adimin"):
        self.test_author = author
        self.test_info = []  # each item is a strategy test experiment
    

    def set_config(self, config):
        self.config = config

    def is_can_exchange(self, data, date, trade):
        """
        function : judge whether can exchange in special day
        """
        account_info = trade.GetAccoutInfo()  # 获取当前仓位
        daily_data = data.get_info_by_day(date.strftime('%Y-%m-%d'))  # data是从test()传入的 调用 IOUtils.py中的函数 获取当日所有的信息
        for stock in account_info.keys():
            if stock != 'cash' and stock not in daily_data:  # 没有现金并且也
                print("stock %s cannot query at %s" % (stock, date.strftime('%Y-%m-%d')))
                return False
        
        return True

    def exceed_advice(self, trade, advice, daily_data):
        if 'all' in advice['sell']:
            trade.selloffall(daily_data)
        else:
            for stock in advice['sell']:
                trade.sell_stock(daily_data, stock, price=advice['sell'][stock])
        for stock in advice['buy'].keys():
            try:
                trade.buy_stock(daily_data, stock, cost=advice['sell'][stock])
            except:
                print(advice)
                trade.print()
                print(daily_data.keys())
                raise
        return

    def test_single(self, data, date, end, test_log, trade):
        day_from_last_exchange = 0  # 距离上次交易经历了多少天 初始化
        while date <= end:
            day_from_last_exchange += 1
            # is_trade_day = self.is_can_exchange(data, date, trade)  
            is_trade_day = data.check_day_info(date.strftime('%Y-%m-%d')) # 检验当日数据是否存在
            # print("%s exchange status %d !" % (date.strftime('%Y-%m-%d'), is_trade_day))

            if not is_trade_day:
                print(date)
                date = date + datetime.timedelta(1)
                continue
            daily_data = data.get_info_by_day(date.strftime('%Y-%m-%d'))  # 获得当天股票信息
            if day_from_last_exchange < int(self.config.const_sold_interval):  # 不能交易直接往后一天
                date = date + datetime.timedelta(1)
            else:
                print("run strategy at ", date.strftime('%Y-%m-%d'))  # 这个时候就可以运行我们的策略了
                if self.config.strategy == "strategy1_":
                    advice = Strategy.strategy_1(date.strftime('%Y-%m-%d'), data, trade)
                elif self.config.strategy == "strategy2_":
                    advice = Strategy.strategy_2(date.strftime('%Y-%m-%d'), data, trade)
                trade.print()
                self.exceed_advice(trade, advice, daily_data)
                day_from_last_exchange = 0  # 重新更新距离上次交易时间
            money, stock, asset, status = trade.GetTotalAsset(daily_data)
            if not status:
                print("cannot get Asset_info at %s" % date.strftime('%Y-%m-%d'))
            else:
                print("asset %s at %f" % (date.strftime('%Y-%m-%d'), asset))
                #print(date)
                test_log.addInfo(date, money, stock, asset, status)
            date = date + datetime.timedelta(1)

    def test(self, data):
        """
        main test entrance
        """
        #config定义初始时间 && 结束时间 计算delta
        start = datetime.datetime.strptime(self.config.start_date, '%Y-%m-%d')
        end = datetime.datetime.strptime(self.config.end_date, '%Y-%m-%d')
        delta_day = end.__sub__(start).days

        delta_days_list = []

        if self.config.is_random:  # random
            for i in range(self.config.n_sample):  # 回测的次数
                sample_delta_day = random.randint(0, delta_day)  # 获得随机的日期
                delta_days_list.append(sample_delta_day)
        else:
            # linear sample
            delta_days_list = [int(i * delta_day/self.config.n_sample) for i in range(self.config.n_sample)]
        
        print("start:end", start, end)
        print(delta_days_list)
        
        for i, delta_day in enumerate(delta_days_list):
            new_start_date = start + datetime.timedelta(days=delta_day)  # 随机设置一个开始日期
            trade = Trade(self.config.init_cash)  # 开始交易
            test_log = TestResult(self.config.strategy)  # eval_strategy 里面的的回测结果
            date = new_start_date  # date更新为新的开始日期
            self.test_single(data, date, end, test_log, trade)
            
            print("finish test %d" % i)
            self.test_info.append(test_log)  # 存储整个test过程中的结果

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
        logs = Logs(self.config.logname, self.config.strategy)
        for i in range(len(self.test_info)):
            with open("%s/test_%d.csv" % (result_dir, i), "w") as wf:
                result = self.test_info[i]
                for date, vals in result.exchange_info.items():
                    line = "%s, %f" %(date, vals['asset'])
                    wf.write(line)
                    wf.write("\n")


    def save_log(self):
        logs = Logs(self.config.logname, self.config.strategy)
        for i in range(len(self.test_info)):
            result = self.test_info[i]
            for date, vals in result.exchange_info.items():
                logs.add(Log(date, vals['money'], vals['stock'], vals['asset'], vals['status']))
                # print(date, vals['money'], vals['stock'], vals['asset'], vals['status'])

        logs.output(self.config.logname)

