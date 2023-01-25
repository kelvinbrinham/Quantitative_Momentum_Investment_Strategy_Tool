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
API_key = linecache.getline(r'/Users/kelvinbrinham/Documents/GitHub/Secret_Files/IEX_API_Key.txt', 10)

#1. Import list of stocks we are interested in from s and p 500 csv file
# i found online
'''
universe_df = pd.read_csv(r'S&P500_Stocks.csv')

#List of Tickers from spreadsheet
Ticker_list = list(universe_df['Symbol'])
Ticker_list_stripped = []

#Strip the ticker symbols to the base tickers
for Ticker in Ticker_list:
    Ticker_list_stripped.append(Ticker.split()[0])

#TRIM TICKER LIST TO 1 STOCK FOR TESTING PURPOSES
Ticker_list_stripped = Ticker_list_stripped[:1]

print(Ticker_list_stripped)

ticker = Ticker_list_stripped[0]
'''
ticker = 'AAPL'


# API_url = f'https://cloud.iexapis.com/stable/stock/{ticker}/stats?token={API_key}'
API_url = f'https://cloud.iexapis.com/stable/stock/{ticker}/stats?token={API_key}'

print(API_url)
Stock_data = rq.get(API_url)
print(Stock_data)
