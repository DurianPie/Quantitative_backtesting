class Trade:
    def __init__(self, Position={'cash':100000}) -> None:
        # Position 存储当前仓位，cash为现金值 如{'600150.XSHG': 20, 'cash': 1000}
        self.Position = Position
    
    def selloffall(self, data):
        """
        清空当前持仓
        Arguments
        ---------
        data: 每日各股票信息dict 
        
        Returns
        -------
        
        """
        for stock in self.Position.keys():
            if stock != 'cash':
                stock_price = data[stock][0]
                self.Position['cash'] += self.Position[stock] * stock_price
                del self.Position[stock]
                