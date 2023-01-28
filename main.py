'''
test
'''


from Momentum_Strategy_class import Momentum_strategy
import config

API_key = config.API_key

my_strategy = Momentum_strategy(10000, 30, API_key)
my_strategy.Order_sheet(0.5, 'S&P500_Stocks.csv', 'Symbol', 'OUTPUT/Order_sheet.xlsx', False)
