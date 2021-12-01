import csv
from datetime import datetime

class Log(): #单条
    def __init__(self, time, money, holdings, value, op):
        self.time = time 
        self.money = money 
        self.holdings = holdings #当前持股
        self.value = value # 当前总价值,即所有股票卖出去加上流动资金的总和
        self.op = op # 这一轮的操作


class Logs():
    def __init__(self, logname, strategyname):
        if logname is None:
            logname = ''
        if strategyname is None:
            strategyname = ''
        self.logname = logname + strategyname + datetime.now().strftime("%Y-%m-%d-%H：%M：%S")
        self.logs = []

    def record(self, log):
        self.logs.append(log)

    def print(self):
        for log in self.logs:
            print(log.time, log.value, log.money, log.holdings, log.operated)

    def output(self, set_name = None):
        if set_name is not None:
            fname = set_name
        else:
            fname = self.logname
        with open( fname +'.csv', 'a', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            for log in self.logs:
                csv_writer.writerow([log.time, log.value, log.money, log.holdings, log.op])











