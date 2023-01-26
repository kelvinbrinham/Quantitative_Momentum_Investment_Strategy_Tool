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

#Mess with first dict of length 3 as in the API batch request list we will
#Perform the following manipulation to add this to a dataframe using concat
#By creating a df for each stock and then concat at the end
Stock_data_js_lst = Stock_data_js_lst[0]

#Put stock data into a df before analysis
my_columns = ['Ticker', 'Price'] #ADD MORE COLUMNS LATER

Stock_df = pd.DataFrame(columns=my_columns)
