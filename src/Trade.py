# -*- encoding: utf-8 -*-
# Filename         :Trade.py
# Description      :
# Time             :2021/11/17 19:19:28
# Author           :王睿彪
# Version          :1.0
import copy

class Trade:
    def __init__(self, cash=100000) -> None:
        Position={'cash':cash}
        # Position 存储当前仓位，cash为现金值 如{'600150.XSHG': 20, 'cash': 1000}
        self.Position = Position
    
    def print(self):
        print(self.Position)

    def buy_stock(self, daily_data, stock_name, amount=None, cost=None):
        if amount == None and cost == None:
            return False
        elif amount == None:
            amount = cost / daily_data[stock_name][0]
        else:
            cost = daily_data[stock_name] * amount
        if self.Position['cash'] < cost:
            return False
        else:
            self.Position['cash'] = self.Position['cash'] - cost
            if stock_name in self.Position.keys():
                self.Position[stock_name] = self.Position[stock_name] + amount
            else:
                self.Position[stock_name] = amount
            return True

    def selloffall(self, daily_data):
        """
        清空当前持仓
        Arguments
        ---------
        daily_data: 每日各股票信息dict 
        
        Returns
        -------
        
        """
        new_position = copy.deepcopy(self.Position)
        for stock in self.Position.keys():
            if stock != 'cash' and stock in daily_data:
                stock_price = daily_data[stock][0]
                new_position['cash'] += self.Position[stock] * stock_price
                del new_position[stock]
        self.Position = new_position
                