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



#1. Import list of stocks we are interested in from S&P 500

class Equity:
    universe = []
    def __init__(self, name: str, ticker: str, price: float, quantity = 0):

        #Validate initialisation arguements
        assert price >= 0, f'Price {price} is negative!'
        assert quantity >= 0, f'Quantity {quantity} is negative!'

        #Assign to self object
        self.__name = name
        self.__ticker = ticker
        self.__quantity = quantity
        self.__price = price

        #Append each equity (instances) to the universe
        Equities.all.append(self)
