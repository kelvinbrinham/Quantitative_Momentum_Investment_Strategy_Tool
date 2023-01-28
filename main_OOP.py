'''
main_OOP
'''

import numpy as np
import pandas as pd
import math as mth
import requests as rq
import linecache
from scipy import stats
import json as js
import datetime as dt
import openpyxl as xl
from openpyxl.styles import Font, Color

API_key_file_path = r'/Users/kelvinbrinham/Documents/GitHub/Secret_Files/IEX_API_Key.txt'
API_key = linecache.getline(API_key_file_path, 10).strip()


class Equity:
    #List of equity objects in Portfolio
    universe = []

    list_of_tickers_supported_f = open(f'list_of_tickers_supported.json')
    list_of_tickers_supported_js = js.load(list_of_tickers_supported_f)

    #Create list of accepted tickers
    API_symbol_lst = [x['symbol'] for x in list_of_tickers_supported_js]

    def __init__(self, ticker: str, quantity = 0):

        #Validate initialisation arguements
        assert quantity >= 0, f'Quantity {quantity} is negative!'
        assert ticker in Equity.API_symbol_lst, f'This stock is not supported, please try another.'

        #Assign to self object
        self.__ticker = ticker
        self.__quantity = quantity

        API_url = f'https://cloud.iexapis.com/stable/stock/{self.__ticker}/quote/latestPrice?token={API_key}'
        current_price_ = rq.get(API_url).json()

        self.__purchase_price = current_price_

        #Append each equity (instances) to the universe
        Equity.universe.append(self)

        #-----------------------------
        #ADD INSTANTIATE FROM CSV HERE!!!
        #-----------------------------

    #Initial properties
    def ticker_name(self):
        return self.__ticker

    def purchase_price(self):
        return self.__purchase_price

    def initial_position_size(self):
        return self.__purchase_price * self.__quantity

    #Current properties
    def current_price(self):
        API_url = f'https://cloud.iexapis.com/stable/stock/{self.__ticker}/quote/latestPrice?token={API_key}'
        current_price_ = rq.get(API_url).json()
        return current_price_

    def position_size(self):
        API_url = f'https://cloud.iexapis.com/stable/stock/{self.__ticker}/quote/latestPrice?token={API_key}'
        current_price_ = rq.get(API_url).json()
        return current_price_ * self.__quantity

    def return_percentage(self):
        API_url = f'https://cloud.iexapis.com/stable/stock/{self.__ticker}/quote/latestPrice?token={API_key}'
        current_price_ = rq.get(API_url).json()
        current_position_size = current_price_ * self.__quantity
        initial_position_size = self.__purchase_price * self.__quantity
        return_percentage_ = (current_position_size - initial_position_size) / initial_position_size
        return "{0:.0%}".format(return_percentage_)
