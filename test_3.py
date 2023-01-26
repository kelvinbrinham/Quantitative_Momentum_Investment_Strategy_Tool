'''
test 3
'''
import pandas as pd
import numpy as np
import json as js


list_of_tickers_supported_f = open(f'list_of_tickers_supported.json')
list_of_tickers_supported_js = js.load(list_of_tickers_supported_f)

API_symbol_lst = [x['symbol'] for x in list_of_tickers_supported_js]
