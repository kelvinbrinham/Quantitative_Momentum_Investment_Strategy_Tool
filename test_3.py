'''
test 3
'''
import numpy as np
import pandas as pd
import math as mth
import requests as rq
import linecache
from scipy import stats
import json as js
import datetime as dt

today = dt.datetime.now()
ticker = 'AAPl'

API_key_file_path = r'/Users/kelvinbrinham/Documents/GitHub/Secret_Files/IEX_API_Key.txt'
API_key = linecache.getline(API_key_file_path, 10).strip()

ticker_string = 'AAPL,FB'
API_url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={ticker_string}&types=stats,quote,chart&range=1y&token={API_key}'
Stock_data_js = rq.get(API_url).json()

no_data_points = len(Stock_data_js['AAPL']['chart'])
# avg_1y_mom = 0
# for i in range(no_data_points):
#     avg_1y_mom += Stock_data_js['AAPL']['chart'][0]['close']
#
# print(avg_1y_mom)



# print(Stock_data_js)
# print(len(Stock_data_js))
#
# print(Stock_data_js['AAPL'])
# print(len(Stock_data_js['AAPL']))
#
print(Stock_data_js['AAPL']['chart'][0]['close'])
print(Stock_data_js['AAPL']['chart'][1]['close'])
# print(len(Stock_data_js['AAPL']['chart']))
