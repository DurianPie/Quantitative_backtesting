from src.IOUtils import *
from src.Trade import Trade

class Strategy:
    def strategy_1(date, data, Trade):
        
        Trade.selloffall()
        return