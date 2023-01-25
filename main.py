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


# read fifth line


# Importing API key from file as to keep it secret when i publish code
API_key = linecache.getline(r'/Users/kelvinbrinham/Documents/GitHub/Secret_Files/IEX_API_Key.txt', 10)



#1. Import list of stocks we are interested in from Universe spreadsheet
universe_df = pd.read_excel(r'/Users/kelvinbrinham/Desktop/Python_practice/Aperture_Task_1/Universe.xlsx')
print(universe_df)
