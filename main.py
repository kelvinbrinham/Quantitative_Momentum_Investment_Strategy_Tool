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

pd.set_option('display.max_columns', None)


# Importing API key from file as to keep it secret when i publish code
API_key_file_path = r'/Users/kelvinbrinham/Documents/GitHub/Secret_Files/IEX_API_Key.txt'
API_key = linecache.getline(API_key_file_path, 10).strip()
#1. Import list of stocks we are interested in from s and p 500 csv file
# i found online

universe_df = pd.read_csv(r'S&P500_Stocks.csv')

#List of Tickers from spreadsheet
Ticker_list = list(universe_df['Symbol'])
Ticker_list_stripped = []

#Strip the ticker symbols to the base tickers
for Ticker in Ticker_list:
    Ticker_list_stripped.append(Ticker.split()[0])



#Creating a batch request from API, IEX uses comma seperated string of Tickers
#Creating a comma separated string of tickers from ticker list stripped

#Create list of sub lists each 100 length so as not to create a batch request that is too long.
chunk_length = 100
Ticker_list_stripped_chunked = [Ticker_list_stripped[x:x+chunk_length] for x in range(0, len(Ticker_list_stripped), chunk_length)]

Ticker_strings_lst = []
for i in range(len(Ticker_list_stripped_chunked)):
    Ticker_strings_lst.append(','.join(Ticker_list_stripped_chunked[i]))


list_of_tickers_supported_f = open(f'list_of_tickers_supported.json')
list_of_tickers_supported_js = js.load(list_of_tickers_supported_f)

API_symbol_lst = [x['symbol'] for x in list_of_tickers_supported_js]


#Perform batch requests from API to retrieve data
#Creating a high quality momentum strategy
data_df_lst = []
my_columns = ['Ticker', 'Price',
                'One-Year Price Return',
                'One-Year Return Percentile',
                'Six-Month Price Return',
                'Six-Month Return Percentile',
                'Three-Month Price Return',
                'Three-Month Return Percentile',
                'One-Month Price Return',
                'One-Month Return Percentile',
                'HQM Score']


for i in range(len(Ticker_list_stripped_chunked)):
    API_url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={Ticker_strings_lst[i]}&types=stats,quote&token={API_key}'
    Stock_data_js = rq.get(API_url).json()
    for ticker in Ticker_strings_lst[i].split(','):
        if ticker in API_symbol_lst:
            Stock_df = pd.DataFrame([[ticker, Stock_data_js[ticker]['quote']['latestPrice'],
                                Stock_data_js[ticker]['stats']['year1ChangePercent'],
                                'N/A',
                                Stock_data_js[ticker]['stats']['month6ChangePercent'],
                                'N/A',
                                Stock_data_js[ticker]['stats']['month3ChangePercent'],
                                'N/A',
                                Stock_data_js[ticker]['stats']['month1ChangePercent'],
                                'N/A',
                                'N/A']], columns=my_columns)

        else:
            Stock_df = pd.DataFrame(columns=my_columns)
        data_df_lst.append(Stock_df)

data_df = pd.concat(data_df_lst, axis = 0, ignore_index = True)
data_df.dropna(inplace = True)
data_df.reset_index(inplace = True)

print(data_df)


# data_df.to_excel('OUTPUT.xlsx')
