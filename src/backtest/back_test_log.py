"""
Author: nijing
date: 20211125
"""

class BlockChangeInfo:
    """
    股票交易信息
    """
    def __init__(self, change_num=0, change_price=0) -> None:
        self.change_num = change_num
        self.change_price = change_price
    
    def to_str(self):
        return " change_num:" + str(self.change_num) + ", change_price:" + str(self.change_price)

change_type = {"buy", "sell"}


class ChangeInfo:
    """
    针对一次交易所发生的信息
    """
    def __init__(self, change_occ_time) -> None:
        self.change_occ_time = change_occ_time
        self.change_info = {}

    def buyBlock(self, BlockChangeInfo):
        self.change_info["buy"] = BlockChangeInfo
    
    def sellBlock(self, BlockChangeInfo):
        self.change_info["sell"] = BlockChangeInfo

    def to_str(self):
        detail = "record: occ at " + str(self.change_occ_time)
        for key, value in self.change_info:
            detail += " " + key + " " + value.to_str()
        return detail


class StockInfo:
    """
    描述一只股票的持有情况
    """
    def __init__(self, count, price) -> None:
        self.cout = count
        self.price = price
        self.value = self.count * self.price 

class OneDayLog:
    """
    记录特定一天的交易信息及账户情况
    """
    def __init__(self, date) -> None:
        self.date = date
        self.change_infos = []
        self.cash = 0
        self.stock_info = {}
        self.margin = 0

    def add_change(self, ChangeInfo):
        self.change_infos.append(ChangeInfo)


class BackTestLog:
    """
    针对交易信息记录设计的对象
    """
    def __init__(self, init_cost, init_block_info) -> None:
        pass
        self.date_info_map = {}
        self.init_cost = init_cost
        self.init_block_info = init_block_info

    def add_one_day_log(self, date, one_day_log):
        self.date_info_map[date] = one_day_log

    def get_margin(self):
        if (len(self.init_block_info) == 0):
            return 0

        else:
            return self.init_block_info[-1].margin
