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

#TRIM TICKER LIST TO 1 STOCK FOR TESTING PURPOSES
# Ticker_list_stripped = Ticker_list_stripped[:3]

# ticker = Ticker_list_stripped[0]


#Creating a batch request from API, IEX uses comma seperated string of Tickers
#Creating a comma separated string of tickers from ticker list stripped

#Create list of sub lists each 100 length so as not to create a batch request that is too long.
chunk_length = 3
Ticker_list_stripped_chunked = [Ticker_list_stripped[x:x+chunk_length] for x in range(0, len(Ticker_list_stripped), chunk_length)]

Ticker_strings_lst = []
for i in range(len(Ticker_list_stripped_chunked)):
    Ticker_strings_lst.append(','.join(Ticker_list_stripped_chunked[i]))

#Perform batch requests from API to retrieve data
Stock_data_js_lst = []
#Work with length 3 for now
for i in range(2):
    API_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={Ticker_strings_lst[i]}&token={API_key}'
    Stock_data_js = rq.get(API_url).json()
    Stock_data_js_lst.append(Stock_data_js)


for i in range(len(Stock_data_js_lst)):
    print(Stock_data_js_lst[i])

#Save Stock_data_js_lst to file to avoid excessive API requests as i mess with putting it in a dataframe

with open('Stock_data.json', 'w') as f:
    js.dump(Stock_data_js_lst, f)



'''
#Perform the batch API request
print(Stock_data_js)
print(Stock_data_js['MMM']['stats'])

month1ChangePercent = Stock_data_js['MMM']['month1ChangePercent']
print(month1ChangePercent)
'''
