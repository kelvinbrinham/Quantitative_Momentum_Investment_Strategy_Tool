'''
test
'''


from main_OOP_2 import Momentum_strategy

strategy = Momentum_strategy(10000, 30)

strategy.Order_Sheet(0.5, 'S&P500_Stocks.csv', 'Output.xlsx')
