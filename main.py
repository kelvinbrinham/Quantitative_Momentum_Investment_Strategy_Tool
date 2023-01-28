'''
test
'''


from Momentum_Strategy_class import Momentum_strategy

strategy = Momentum_strategy(10000, 80)

strategy.Order_Sheet(0.7, 'S&P500_Stocks.csv', 'Symbol', 'Output.xlsx')
# strategy.Order_Sheet(0.1, 'FTSE100_Stocks.csv', 'ticker', 'Output.xlsx')
