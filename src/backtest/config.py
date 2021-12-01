"""
Author: nijing
date: 20211125
"""
import datetime

class BaseConfig:
    def __init__(self) -> None:
        self.n_sample = 100 # 回测一个策略的次数
        self.is_random = True # 选取数据是否随机
        self.init_cash = 1000000 # 现金数额
        self.stock_info = {} # 开始持仓情况
        self.start_date = "2019-01-01" # 允许最早交易时间
        self.end_date = "2020-01-01" # 允许最晚交易时间
        self.strategy = "strategy1_" # 策略名称
        self.const_sold_interval = "7" # 固定卖股票间隔,应该告诉我买卖情况
        self.is_good_strategy_ratio = 0.8 # 判断一只策略是否是好策略的比例
        self.logname = 'log1_' + self.strategy + datetime.datetime.now().strftime("%Y-%m-%d-%H：%M：%S")


class RiskPreferConfig(BaseConfig):
    """
    针对风险喜好者的投策策略评判标准
    """
    def __init__(self) -> None:
        super().__init__()
        

class RiskDenfenseConfig(BaseConfig):
    """
    针对风险厌恶者的投策策略评判标准
    """
    def __init__(self) -> None:
        super().__init__()




