'''
main
'''

import numpy as np
import pandas as pd
import math as mth
import requests as rq
import linecache
from scipy import stats
import json as js
import datetime as dt
import openpyxl as xl
from openpyxl.styles import Font, Color


pd.set_option('display.max_columns', None)

# Importing API key from file as to keep it secret when i publish code
API_key_file_path = r'/Users/kelvinbrinham/Documents/GitHub/Secret_Files/IEX_API_Key.txt'
API_key = linecache.getline(API_key_file_path, 10).strip()

#Import list of S&P500 stocks from csv file i found online
universe_df = pd.read_csv(r'S&P500_Stocks.csv')

#Create List of stock tickers
Ticker_list = list(universe_df['Symbol'])
Ticker_list_stripped = []

#Strip the ticker symbols to the base tickers (ignore exchanges, blank spaces etc.)
for Ticker in Ticker_list:
    Ticker_list_stripped.append(Ticker.split()[0])

#Shorten for testing to reduce API requests (slow and limited number of requests on free trial)
Ticker_list_stripped = Ticker_list_stripped[:10]

#Create sub lists of tickers with length chunk_length so that each API batch request isn't too long
chunk_length = 100
Ticker_list_stripped_chunked = [Ticker_list_stripped[x:x+chunk_length] for x in range(0, len(Ticker_list_stripped), chunk_length)]

#List of strings, each containing multiple comma separated tickers ('AAPL,FB,...')
Ticker_strings_lst = []
for i in range(len(Ticker_list_stripped_chunked)):
    Ticker_strings_lst.append(','.join(Ticker_list_stripped_chunked[i]))

#Open file containing list of tickers supported by the API
list_of_tickers_supported_f = open(f'list_of_tickers_supported.json')
list_of_tickers_supported_js = js.load(list_of_tickers_supported_f)

#Create list of accepted tickers
API_symbol_lst = [x['symbol'] for x in list_of_tickers_supported_js]


#Perform batch requests from API to retrieve data
#Create list of dataframes (one for each stock)
data_df_lst = []
#Define the columns of my data frame
my_columns = ['Ticker', 'Price', 'YTD Average 1-Day Percentage Momentum', 'YTD 1-Day Momentum Hit Ratio', 'Buy']

#Loop over each ticker string
for i in range(len(Ticker_list_stripped_chunked)):
    API_url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={Ticker_strings_lst[i]}&types=stats,quote,chart&token={API_key}'
    #Request batch stock data
    Stock_data_js = rq.get(API_url).json()
    for ticker in Ticker_strings_lst[i].split(','):
        #Write individual data frame for each stock and add to data_df_lst
        if ticker in API_symbol_lst:
            #Work out 1 year average Momentum
            no_data_points = len(Stock_data_js[ticker]['chart']) # no. trading days in ytd
            avg_ytd_mom = 0 # Average 1 day momentum ytd
            ytd_mom_hit_ratio = 0 # no. days with increased momentum

            for j in range(no_data_points):
                percent_chg_current = Stock_data_js[ticker]['chart'][j]['changePercent']
                avg_ytd_mom += percent_chg_current / no_data_points
                if percent_chg_current > 0:
                    ytd_mom_hit_ratio += 1 / no_data_points

            Stock_df = pd.DataFrame([[ticker, Stock_data_js[ticker]['quote']['latestPrice'],
                                    avg_ytd_mom, ytd_mom_hit_ratio, 'N/A']], columns=my_columns)

        else: #If ticker is not supported by the API
            Stock_df = pd.DataFrame(columns=my_columns)
        data_df_lst.append(Stock_df)

#Create 1 overall dataframe containing all relevant data for each stock
#(I create multiple data frames and then use concat because append() is soon to be removed from pandas)
data_df = pd.concat(data_df_lst, axis = 0, ignore_index = True).dropna(inplace = True).reset_index(inplace = True)

#Removing Stocks with 1-Day momentum hit-ratios worse than:
Minimum_1d_momentum_hit_ratio = 0.1
data_df.drop(data_df[data_df['YTD 1-Day Momentum Hit Ratio'] < Minimum_1d_momentum_hit_ratio].index, inplace = True)

#Sort the remaining stocks by YTD average 1-Day percentage momentum
data_df.sort_values('YTD Average 1-Day Percentage Momentum', ascending = False, inplace = True)


cash = 10000
portfolio_length = 20

data_df.reset_index(inplace = True)

data_df = data_df[:portfolio_length]


position_size = cash / portfolio_length

for i in range(len(data_df)):
    data_df.loc[i, 'Buy'] = mth.floor(position_size / data_df['Price'][i])

data_df.drop(columns = ['level_0', 'index'], inplace = True)


#Formatting the Excel sheet
Momentum_strategy_file_name = 'OUTPUT/Momentum_strategy.xlsx'
data_df.to_excel(Momentum_strategy_file_name, sheet_name = 'Order_Sheet', startrow = 3, index = False)

Momentum_strategy_wb = xl.load_workbook(Momentum_strategy_file_name)
Momentum_strategy_ws = Momentum_strategy_wb.active

percentage_columns = ['C', 'D']

for letter in percentage_columns:
    for i in range(4, 4 + portfolio_length):
        Momentum_strategy_ws[letter + str(i)].number_format = '0.00%'

title_font = Font(name = 'Arial', size = 18, color = '000080', bold = True)
date_font = Font(name = 'Arial', size = 15)

Momentum_strategy_ws['A1'].font = title_font
Momentum_strategy_ws['A1'] = 'Momentum Trading Strategy'

Momentum_strategy_ws['A2'].font = date_font
Momentum_strategy_ws['A2'] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


for column_ in Momentum_strategy_ws.columns:
    column_letter_ = column_[0].column_letter
    width_ = max(len(cell.value) for cell in column_ if isinstance(cell.value, str))
    Momentum_strategy_ws.column_dimensions[column_letter_].width = width_ + 3

Momentum_strategy_wb.save(Momentum_strategy_file_name)
