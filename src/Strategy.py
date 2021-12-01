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

def takeSecond(elem):
    return elem[1]

class Strategy:
    @staticmethod
    def strategy_1(cur_date, data, trade, exceed=True):
        """
        
        Arguments
        ---------
        date: 操作日期
        data: 交易数据
        trade: 交易类，含有持仓信息
        
        Returns
        -------
        
        """
        advice = {
            'sell': {},
            'buy': {}
        }
        cur = datetime.datetime.strptime(cur_date, '%Y-%m-%d').date()
        start = cur - datetime.timedelta(days=7)
        while not data.check_day_info(str(start)):
            start = start - datetime.timedelta(days=1)

        daily_data = data.get_info_by_day(str(cur_date))
        start_daily_data = data.get_info_by_day(str(start))
        
        cur_date_stocks = list(daily_data.keys())
        start_date_stocks = list(start_daily_data.keys())
        # print(cur_date, "cur_date_stocks:", cur_date_stocks)
        # print(start, "start_date_stocks:", start_date_stocks)
        same_stocks = list(set(cur_date_stocks).intersection(set(start_date_stocks)))

        stocks_value = [(s, (daily_data[s][0] - start_daily_data[s][0])/start_daily_data[s][0]) for s in same_stocks]
        stocks_value.sort(key=takeSecond)
        
        if exceed:
            trade.selloffall(daily_data)
        else:
            advice['sell']['all'] = 1

        if len(stocks_value) == 0:
            print("cannot buy any stock because last 7 day has no same stock with cur_date:%s!" % cur_date)
        money = trade.Position['cash'] / 10
        buy_stock_num = min(10, len(stocks_value))

        for i in range(buy_stock_num):
            if exceed:
                status = trade.buy_stock(daily_data, stocks_value[i][0], cost=money)
            else:
                advice['buy'][stocks_value[i][0]] = money
        return advice

    @staticmethod
    def strategy_2(cur_date, data, trade, exceed=True):
        """
        
        Arguments
        ---------
        date: 操作日期
        data: 交易数据
        trade: 交易类，含有持仓信息
        
        Returns
        -------
        
        """
        advice = {
            'sell': {},
            'buy': {}
        }
        cur = datetime.datetime.strptime(cur_date, '%Y-%m-%d').date()
        start = cur - datetime.timedelta(days=7)
        while not data.check_day_info(str(start)):
            start = start - datetime.timedelta(days=1)

        daily_data = data.get_info_by_day(str(cur_date))
        start_daily_data = data.get_info_by_day(str(start))
        
        cur_date_stocks = list(daily_data.keys())
        start_date_stocks = list(start_daily_data.keys())
        # print(cur_date, "cur_date_stocks:", cur_date_stocks)
        # print(start, "start_date_stocks:", start_date_stocks)
        same_stocks = list(set(cur_date_stocks).intersection(set(start_date_stocks)))

        stocks_value = [(s, (daily_data[s][0] - start_daily_data[s][0])/start_daily_data[s][0]) for s in same_stocks]
        stocks_value.sort(key=takeSecond, reverse=True)

        if exceed:
            trade.selloffall(daily_data)
        else:
            advice['sell']['all'] = 1

        if len(stocks_value) == 0:
            print("cannot buy any stock because last 7 day has no same stock with cur_date:%s!" % cur_date)
        money = trade.Position['cash'] / 10
        buy_stock_num = min(10, len(stocks_value))

        for i in range(buy_stock_num):
            if exceed:
                status = trade.buy_stock(daily_data, stocks_value[i][0], cost=money)
            else:
                advice['buy'][stocks_value[i][0]] = money
        return advice

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
