# 股票回测系统——Group 23

## 类的介绍


### Stock类
股票数据管理类 

   - 成员数据
     - `Info` 字典类型，每个元素：key值为日期，value为所有因子。
     - e.g.
   {"2010-01-04": [open, close, high, ..., MACD, OBV, PSY],
   "2010-01-05": [...], }
     - `name` 股票名称
   - `get_info_by_day`: 返回一支股票在某一天的所有信息
   - `calculate_profit(self, start, end)`:
     - i. 计算该股票在起止时间内[start, end]的涨幅
     - ii.实现逻辑：为了避免start或者end天不存在的情况，会首先二分到大于等于start的第一天
   以及小于等于end的最后一天，再使用日期作为key值直接索引出当天的开盘or收盘价。

   

### IOManager类
pandas文件读入以及数据处理 

   a. `pickle.load`从pandas读入 `key`值为日期，`value`为DataFrame （pandas对象）
   b. `IOManager.__parse_data()`:
   i. 返回股票对象的字典(dict)

   ii.基本实现逻辑：遍历data字典，字典value值为DataFrame, 该value值每一行可以处理出
   某支股票在某一天的数据，按照股票名称加入该股票的info成员中。(同时使用了pandas中
   isna()接口，过滤所有的缺失值)，最后每支股票的所有数据按照日期排序。

   dataframe的基本结构如下：

   ![数据处理_简单策略.jpg](https://i.loli.net/2021/12/01/538VPqKc4XnNljo.jpg)

### IOUtils类
IO接口，提供一些对数据集的操作

- `check_day_info` 检查某一天是否为交易日
- `get_info_by_day` 获取某一天的股票信息
- `find_largest_within(self, cur, k)`.
 - 找出最近k天涨幅最大的股票 [max(0, cur-k+1), cur]

 - 基本实现：遍历IOManager.__parse_data()返回的字典，调用calculate_profit接口得到
   该股票最近k的利润，维护利润的最大值以及对应最大值的股票名称即可。

### BackTest类

回测功能的实现
#### 成员变量
- `config`
- `test_info`
#### 成员函数

- `test()` 执行多次回测任务
- `test_single()` 根据开始结束日期执行回测任务
- `exceed_advice()` 执行策略建议
- `eval()` 评估回测结果
- `save_eval_result()` 保存回测结果
- `save_log()` 保存执行日志

### Strategy类

策略的实现，内部为静态函数，供外部调用，函数读入日期信息，股票信息和持仓情况给出策略建议

#### 方法

- `strategy_1()`: 策略1，卖出所有持仓，购买7天内涨幅最小（跌幅最大）的股票

- `strategy_2()`: 策略2，卖出所有持仓，购买7天内涨幅最大（跌幅最小）的股票

### Trade类

持仓状态类，保存持仓状态，对持仓股票进行操作

#### 成员变量

- `Postion` 字典，存储持仓状态，包含现金数量，持有股票的股数

#### 方法

- `buy_stock()` 购买某一只股票
- `sell_stock()` 出售某一只股票
- `selloffall()` 卖出所有股票
- `GetAccoutInfo()` 获取持仓信息
- `GetTotalAsset()` 计算某一天的持仓总资产

### BaseConfig类

回测的初始设置

#### 成员变量

- `n_sample`  回测一个策略的次数
- `is_random` 选择回测的日期是否随机
- `init_cash` 初始化手里有多少现金
- `stock_info` 开始持仓情况，存为字典
- `start_date` 允许最早交易时间
- `end_date` 允许交易最晚时间
- `strategy` 选择一个策略
- `const_sold_interval` 固定卖股票间隔，
- `is_good_strategy_ratio` 判断一只策略好坏的比例
- `logname` 日志名字，根据策略名和时间组成

### TestResult类

- 回测结果

#### 成员变量

- `strategy_name` 策略的名字
- `exchange_info`存储交易信息，结构为字典，字典的key为日期，values为字典，存储手里有的现金，股票，资产，状态

#### 方法

- `addInfo()` 添加一条exchange_info

- `size()` 返回exchange_info的长度，用于is_positve_margin()调用判断是否收益
- `is_positve_margin()` 根据exchange_info存储的资产判断是否收益，这里会有边界值判断，只有exchange_info中存储信息的时候才会判断



### EvalStrategy类

评价策略

#### 成员变量

- `config` 获取回测人员设置的参数，来源是BaseConfig类

#### 方法

- `is_positve_margin()` 计算我们的策略有收益的个数，这里还会有一个边界测试，只有size() > 0 的时候才是有效的数据，其次才能判断是否是有收益的。根据config里面 is_good_strategy_ratio来计算我们的策略到底是不是一个好的策略



### Log类

记录单一条日志

#### 成员变量

- `time`  记录日期
- `money` 现金
- `holdings` 持股的价值
- `value` 所有股票当前值多少钱以及现金
- `op` 这一轮的操作



### Logs类

#### 成员变量

- `logname` 日志名字
- `strategyname` 策略名字

#### 方法

- `add()` 添加一条log到logs
- `print()` 打印信息供debug //后面也没用
- `output()` 输出log，存储为csv文件，将回测过程中的信息，也就Log类的成员变量存储起来



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

7. ##### 日收益率曲线

​		在回测期内，策略每天的收益率情况。

​		同样是可交互的，可以看到悬停点是策略产生最大收益的一天，+4.5%

![7.png](https://i.loli.net/2021/11/30/WaR7OMI4K1zYjgX.png)

#### 错误与异常控制

1.可视化类本身自带规范化数据格式（让输入数据变为可以绘图的格式）的方法

2.异常控制，通过try except方法等，保证输入异常时，可以正确告知调用者可视化发生了异常。



注：其他限于时间没有展示or还没有完全完成的功能

​		持仓结构条形图，持仓结构—盈亏雷达图：同时展示当前持仓的比例与盈亏情况等等







