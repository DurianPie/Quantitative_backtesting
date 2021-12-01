### Stock_Visualize类

stock_visualize类（可视化类）集成了主要的可视化功能，功能之一是对策略回测结果的可视化（净值、日收益率、比较基准等不同维度）。

此外，参考实际应用中在制定策略、交易回测等方面可能产生的实际需求，还提供了若干可以辅助分析的功能。

stock_visualize类（可视化类）与其他模块的互动方式较为简单直接，即在其他类中产生的需要进行可视化的数据为输入（dataframe、np、list等形式，格式经过一定规范化），可视化类输出可视化结果。且基本上一个功能对应一个方法。

#### 可视化类的功能

1. ##### 股票k线图

   ```python
   def simple_one_stock(self,name, data):
   ```

   实际应用中，我们可能会想看看策略中买入/卖出的股票近期走势如何

   

   ![1.png](https://i.loli.net/2021/11/30/buAZnxsrTcBMCWO.png)

2. ##### 更完整的股票k线图

   ```python
   def complicated_one_stock(self,name, data):
   ```

   ![2.png](https://i.loli.net/2021/11/30/wGWJVBtnMhjcLfA.png)

3. ##### 全市场（全目标池）涨跌热力图

   ```python
   def market_hearmap(self,data):
   ```

   我们还很有可能关心的话题是，在我们准备投资的目标池里，每天的涨跌情况如何，而热力图可以直观的以颜色的深浅表示这个问题。

   ![3.png](https://i.loli.net/2021/11/30/cIHpOQbJCiMYTzs.png)

4. ##### 持仓结构饼状图

   ```python
   def holding_weights(self,data,type='pie'):
   ```

   以图形的方式展示当前的持仓结构,也可以选择条形图/柱状图等样式。

   ![4.png](https://i.loli.net/2021/11/30/M8Xbqh4DNgCzrlZ.png)

5. ##### 净值曲线

   ```python
   def one_strategy_backtest(self,data):
   ```

   在回测期内，整个策略的每日净值表现。

   绘图结果是可交互的，悬停可以查看数据点的具体信息，如图中悬停的点是策略净值最高的点，发生在2019-4-22。（以及可以滑动、放大等，制作说明文档的截图无法完整演示这一功能）

   ![5.png](https://i.loli.net/2021/11/30/AM5qpR9Dd3mhoH1.png)

6. ##### 净值曲线+基准

   在回测期内，整个策略的每日净值表现，并与基准相比。

   ![6.png](https://i.loli.net/2021/11/30/RNtjBKHSzkhJmWZ.png)

8. ##### 日收益率曲线

​		在回测期内，策略每天的收益率情况。

​		同样是可交互的，可以看到悬停点是策略产生最大收益的一天，+4.5%

![7.png](https://i.loli.net/2021/11/30/WaR7OMI4K1zYjgX.png)

##### 	8.其他限于时间没有展示or还没有完全完成的功能

​		持仓结构条形图，持仓结构—盈亏雷达图：同时展示当前持仓的比例与盈亏情况等等

#### 错误与异常控制：

1.可视化类本身自带规范化数据格式（让输入数据变为可以绘图的格式）的方法

2.异常控制，通过try except方法等，保证输入异常时，可以正确告知调用者可视化发生了异常。