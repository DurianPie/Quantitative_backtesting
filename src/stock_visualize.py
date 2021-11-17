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
    def data_for_mpf(self,data): #将df调整为可以画图的格式
        data.columns = ['Open','High','Low','Close','Volume']
        data.index = pd.to_datetime(data.index)
        return data
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
            #还可以增加设置参数 

    def market_hearmap(self,data):  #和下边一个函数都还需要修改，图的参数应该由函数传参
        fig = px.treemap(data, \
                 path=['SEC_NAME'],\
                 values=[1,1,1,1,1,1,1,1], \
                 color='PCT_CHG', \
                 range_color = [-2, 2], \
                 hover_data= {'PCT_CHG':':.2%'\
                             'SEC_NAME'}, \
                 height = 1080,\
                 width = 876,\
                 color_continuous_scale='Geyser',\
                 color_continuous_midpoint=0 , )
        fig.show()

    def strategy_heatmap(self,data):
        fig = px.treemap(data, \
                 path=['SEC_NAME'],\
                 values=[1,1,1,1], \
                 color='PCT_CHG', \
                 range_color = [-2, 2], \
                 hover_data= {'PCT_CHG':':.2%'\
                             'SEC_NAME'}, \
                 height = 1080,\
                 width = 1920,\
                 color_continuous_scale='Geyser',\
                 color_continuous_midpoint=0 , )
        fig.show()
    def holding_weights(self,data):
        fig = px.pie(data, names='name',values='weight')
        fig.show()

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

data1 = case.data_for_mpf(data1)

#case.simple_one_stock('600519.SH',data1)
#case.complicated_one_stock('600519.SH',data1)

data2 = w.wsd(['000300.SH','000001.SH','300750.SZ'],'close','-60D',usedf=True)
data2 = data2[1]
for index,row in data2.iteritems():
    data2[index] /= data2[index][0] 
#case.one_strategy_backtest(data2)


data3 = w.wss(['600010.SH','000001.SZ','300750.SZ','600519.SH'],['pct_chg,sec_name'],"tradeDate=20211117;priceAdj=U;cycle=D",\
        usedf=True)
data3= data3[1]
case.market_hearmap(data3)


data4 = {'name':['股票1','股票2','股票3'],'weight':[0.15,0.55,0.3]}
data4 = pd.DataFrame(data4)
case.holding_weights(data4)
'''