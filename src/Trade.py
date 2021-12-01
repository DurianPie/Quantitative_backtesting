# -*- encoding: utf-8 -*-
# Filename         :Trade.py
# Description      :
# Time             :2021/11/17 19:19:28
# Author           :王睿彪
# Version          :1.0
import copy


class Trade:
    def __init__(self, cash=100000) -> None:
        Position = {'cash': cash}
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
                print("sell stock %s at price %f" % (self.Position[stock], stock_price))
                del new_position[stock]
        self.Position = new_position

    def GetAccoutInfo(self):
        return self.Position

    def GetTotalAsset(self, daily_data):
        asset = 0  # 初始化资产为0
        money = 0
        stock = 0
        for key, value in self.Position.items():
            if key == "cash":
                asset += value  # 现金直接加入我们的资产中
                money = value
            else:
                if key in daily_data:
                    stock_price = daily_data[key][0]
                    asset += value * stock_price  # 股票的话就算一下当前的股票值多少钱
                    stock += value * stock_price

                else:
                    print("cannot get daily info for stock ", key)
                    cur_date_stocks = list(daily_data.keys())
                    print("cur_date_stocks:", cur_date_stocks)

                    return money, stock, asset, False
        # print('why?')
        return money, stock, asset, True
