"""
Author: nijing
date: 20211125
"""

class BaseConfig:
    def __init__(self) -> None:
        self.n_sample = 10 # 回测一个策略的次数
        self.is_random = True # 选取数据是否随机
        self.init_cash = 1000000 # 现金数额
        self.stock_info = {} # 开始持仓情况
        self.start_date = "2019-01-01" # 允许最早交易时间
        self.end_date = "2019-03-01" # 允许最早交易时间
        self.strategy = "strategy1" # 策略名称
        self.const_sold_interval = "7" #固定卖股票间隔




