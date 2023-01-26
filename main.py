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


# read fifth line


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
Ticker_list_stripped = Ticker_list_stripped[:3]
print(Ticker_list_stripped)

# ticker = Ticker_list_stripped[0]


#Creating a batch request from API, IEX uses comma seperated string of Tickers
#Creating a comma separated string of tickers from ticker list stripped


# Ticker_string
# API_url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={Ticker_string}&types=stats?token={API_key}'

'''
1:58
'''


'''
API_url = f'https://cloud.iexapis.com/stable/stock/{ticker}/stats?token={API_key}'


#Perform the batch API request
Stock_data_js = rq.get(API_url).json()
print(Stock_data_js)

month1ChangePercent = Stock_data_js['month1ChangePercent']
print(month1ChangePercent)
'''
