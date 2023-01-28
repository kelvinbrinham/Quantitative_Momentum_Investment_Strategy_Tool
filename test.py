'''
test
'''


from main_OOP_2 import Momentum_strategy

strategy = Momentum_strategy(10000, 80)

# strategy.Order_Sheet(0.5, 'S&P500_Stocks.csv', 'Symbol', 'Output.xlsx')
strategy.Order_Sheet(0.2, 'FTSE100_Stocks.csv', 'ticker', 'Output.xlsx')
