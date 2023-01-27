'''
test
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

class Equity:
    #List of equity objects in Portfolio
    universe = []
    def __init__(self, ticker: str, price: float, quantity = 0):

        #Validate initialisation arguements
        assert price >= 0, f'Price {price} is negative!'
        assert quantity >= 0, f'Quantity {quantity} is negative!'

        #Assign to self object
        self.__ticker = ticker
        self.__quantity = quantity
        self.__price = price

        #Append each equity (instances) to the universe
        Equity.universe.append(self)

        #-----------------------------
        #ADD INSTANTIATE FROM CSV HERE!!!
        #-----------------------------

    def ticker_name(self):
        return self.__ticker

    @classmethod
    def display(cls):
        print(Equity.universe)


    def total_invested_value(self):
        return self.__price * self.__quantity


    def current_stock_price(self):
        API_url = f'https://cloud.iexapis.com/stable/stock/{self.__ticker}/quote/latestPrice?token={API_key}'
        current_price_ = rq.get(API_url).json()
        return current_price_


    def stock_total_value(self):
        API_url = f'https://cloud.iexapis.com/stable/stock/{self.__ticker}/quote/latestPrice?token={API_key}'
        current_price_ = rq.get(API_url).json()
        return current_price_ * self.__quantity

    # def portfolio_value(self):
    #     API_url = f'https://cloud.iexapis.com/stable/stock/{self.__ticker}/quote/latestPrice?token={API_key}'
    #     current_price_ = rq.get(API_url).json()
    #     return current_price_ * self.__quantity


    def __repr__(self):
    #Representing instance nicely
        return f"{self.__class__.__name__}('{self.__ticker}', {self.__price}, {self.__quantity})"


Apple = Equity('AAPL', 140, 2)


print(Apple)
print(Apple.current_stock_price())
print(Apple.stock_total_value())
print(Apple.total_invested_value())
