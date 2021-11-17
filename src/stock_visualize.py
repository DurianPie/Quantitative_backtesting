import numpy as np
import pandas as pd
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
import Stock
import mplfinance as mpf
import plotly_express as px



"""
    预计主要使用到ploty, plty.express , mlpfinance当然还少不了matplotlib
"""
class stock_visualize():
    def __init__(self):
        self.intro  = '用于个股和组合的可视化分析'
    def testing(self):
        print("换一个文件可以输出")
        
    def simple_one_stock(self,name, data): #name为字符串， data为dataframe，且index，columns有格式
        try:
            mpf.plot(data,title=name, type='candle',style='classic' )
            plt.show()
            print('打印成功')
        except:
            print('打印复杂k线图遇到问题')
        

    def complicated_one_stock(self,name, data): #name为字符串， data为dataframe，且index，columns有格式
        try:
            mpf.plot(data,title=name, type='candle',style='binance',volume=True,mav=(5,10) )
            plt.show()
            print('打印成功')
        except:
            print('打印简单k线图遇到问题')

    def one_strategy_backtest(self,data):  #需要输入策略和基准，data格式为dataframe
        try:
            fig =px.line(data)
            fig.show()
            print('打印成功')
        except:
            print('遇到问题')

from WindPy import w
w.start()
case = stock_visualize()
#w.isconnected()
'''
data1 = w.wsd('600519.SH',['open','high','low','close','volume'],'-60D',usedf=True)

data1 = data1[1]
data1.columns = ['Open','High','Low','Close','Volume']
print(data1.columns)
data1.index = pd.to_datetime(data1.index)

case.simple_one_stock('600519.SH',data1)
case.complicated_one_stock('600519.SH',data1)
'''
data2 = w.wsd(['000300.SH','000001.SH','300750.SZ'],'close','-60D',usedf=True)
data2 = data2[1]
for index,row in data2.iteritems():
    data2[index] /= data2[index][0] 
case.one_strategy_backtest(data2)