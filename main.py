'''
test
'''


from Momentum_Strategy_class import Momentum_strategy

from config import API_key


my_strategy = Momentum_strategy(10000, 30, API_key)
my_strategy.Order_sheet(0.5, 'S&P500_Stocks.csv', 'Symbol', '/Users/kelvinbrinham/Downloads/Quantitative_Momentum_Investment_Strategy_Tool-main/OUTPUT/bla.xlsx', False)
