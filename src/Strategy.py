# -*- encoding: utf-8 -*-
# Filename         :Strategy.py
# Description      :
# Time             :2021/11/17 19:19:57
# Author           :王睿彪
# Version          :1.0
from src.IOUtils import *
from src.Trade import Trade
import datetime

def get_stock_price(daily_data, stock_name):
    return daily_data[stock_name][0]

class Strategy:
    @staticmethod
    def strategy_1(cur_date, data, Trade):
        """
        
        Arguments
        ---------
        date: 操作日期
        data: 交易数据
        Trade: 交易类，含有持仓信息
        
        Returns
        -------
        
        """
        cur = datetime.datetime.strptime(cur_date, '%Y-%m-%d').date()
        start = cur - datetime.timedelta(days=7)
        daily_data = data.get_info_by_day(cur_date)
        start_daily_data = data.get_info_by_day(str(start))
        stocks = list(daily_data.keys())
        stocks.sort(key = lambda s:(daily_data[s][0] - start_daily_data[s][0])/(start_daily_data[s][0]))
        for stock in stocks:
            print(stock, (daily_data[stock][0] - start_daily_data[stock][0])/(start_daily_data[stock][0]))
        Trade.selloffall(daily_data)
        money = Trade.Position['cash'] / 10
        
        if (len(stocks) < 10):
            return
        for i in range(10):
            Trade.buy_stock(daily_data, stocks[i], cost=money)
        return

def main():
    data = IOUtils('data/data.pkl')
    T = Trade()
    date = '2019-01-03'
    s = Strategy()
    daily_data = data.get_info_by_day(date)
    T.print()
    T.buy_stock(daily_data, '600150.XSHG', cost=1000)
    T.print()
    s.strategy_1(date, data, T)
    T.print()

if __name__ == '__main__':
    main()
