'''
Creating a file containing the accepted tickers for the IEX API
'''

import requests as rq
import linecache
import json as js


API_key_file_path = r'/Users/kelvinbrinham/Documents/GitHub/Secret_Files/IEX_API_Key.txt'
API_key = linecache.getline(API_key_file_path, 10).strip()

API_url = f'https://cloud.iexapis.com/beta/ref-data/symbols?token={API_key}'

tester = rq.get(API_url).json()
print(tester)

with open(f"list_of_tickers_supported.json", 'w') as f:
    js.dump(tester, f)
