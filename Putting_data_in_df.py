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

API_key_file_path = r'/Users/kelvinbrinham/Documents/GitHub/Secret_Files/IEX_API_Key.txt'
API_key = linecache.getline(API_key_file_path, 10).strip()

API_url = f'https://cloud.iexapis.com/beta/ref-data/symbols?token={API_key}'

tester = rq.get(API_url).json()
print(tester)

with open(f"list_of_tickers_supported.json", 'w') as f:
    js.dump(tester, f)
