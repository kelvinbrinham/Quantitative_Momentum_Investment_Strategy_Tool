'''
test
'''


from Momentum_Strategy_class import Momentum_strategy

strategy = Momentum_strategy(100000000, 30)

# strategy.Order_Sheet(0, 'S&P500_Stocks.csv', 'Symbol', 'OUTPUT/Order_sheet.xlsx', False)
strategy.Order_Sheet(0, 'S&P500_Stocks.csv', 'Symbol')
# strategy.Order_Sheet(0.1, 'FTSE100_Stocks.csv', 'ticker', 'Output.xlsx')
