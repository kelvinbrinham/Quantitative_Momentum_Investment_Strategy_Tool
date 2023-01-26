'''
test 2
'''

import numpy as np
import pandas as pd
import math as mth
import requests as rq
import linecache
from scipy import stats
import json as js
import datetime as dt

Stock_data_js_lst = open('Stock_data.json')
Stock_data_js_lst = js.load(Stock_data_js_lst)

#Put stock data into a df before analysis
my_columns = ['Ticker', 'Price'] #ADD MORE COLUMNS LATER

Stock_df = pd.DataFrame(columns=my_columns)

#Creating df for each stock
for i in range()


print(Stock_data_js_lst)

print(Stock_df)
