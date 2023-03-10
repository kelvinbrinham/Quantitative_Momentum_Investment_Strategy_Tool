'''
Momentum Strategy Class

This script contains the class which analyses selected stocks based on high quality Momentum
and produces an order spreadsheet.
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


class Momentum_strategy:

    #Create list of tickers supported by the API from file created in another script
    list_of_tickers_supported_f = open(f'list_of_tickers_supported.json')
    list_of_tickers_supported_js = js.load(list_of_tickers_supported_f)

    #Create list of accepted tickers
    API_symbol_lst = [x['symbol'] for x in list_of_tickers_supported_js]

    def __init__(self, investment: float, number_of_positions: int, API_key: str):

        #Validate initialisation arguements
        assert investment > 0, f'Investment {investment} is negative!'
        assert number_of_positions > 0, f'Number of positions {number_of_positions} is negative!'
        assert isinstance(number_of_positions, int), f'Number of positions must be a positive integer'
        assert isinstance(investment, float) or isinstance(investment, int), f'Initial investment must be a positive number'

        self.__investment = investment
        self.__number_of_positions = number_of_positions
        self.__API_key = API_key


    def __Ticker_strings_lst_(self, filename: str, ticker_tag: str):
        universe_df = pd.read_csv(filename)

        if ticker_tag not in universe_df:
            raise Exception(f'Wrong Ticker tag, please check the tag in the file {filename}')
        #Create List of stock tickers
        Ticker_list = list(universe_df[ticker_tag])
        Ticker_list_stripped = []

        #Strip the ticker symbols to the base tickers (ignore exchanges, blank spaces etc.)
        for Ticker in Ticker_list:
            Ticker_list_stripped.append(Ticker.split()[0])

        #TESTING <><><><><><><><><><><><><><><><><><><><><><><><>
        #Shorten ticker list for testing to reduce API requests (slow and limited number of requests on free trial)
        # Ticker_list_stripped = Ticker_list_stripped[:10]
        #<><><><><><><><><><><><><><><><><><><><><><><><><><><><>

        #Create sub lists of tickers with length chunk_length so that each API batch request isn't too long
        chunk_length = 100
        Ticker_list_stripped_chunked = [Ticker_list_stripped[x:x+chunk_length] for x in range(0, len(Ticker_list_stripped), chunk_length)]

        #List of strings, each containing multiple comma separated tickers ('AAPL,FB,...') for the batch API request
        Ticker_strings_lst = []
        for i in range(len(Ticker_list_stripped_chunked)):
            Ticker_strings_lst.append(','.join(Ticker_list_stripped_chunked[i]))

        return Ticker_strings_lst, Ticker_list_stripped_chunked

    def __batch_request(self, Ticker_strings_lst, Ticker_list_stripped_chunked):
        #Perform batch requests from API to retrieve data
        #Create list of dataframes (one for each stock)
        data_df_lst = []
        #Define the columns of my data frame
        my_columns = ['Ticker', 'Price', 'YTD Average 1-Day Percentage Momentum', 'YTD 1-Day Momentum Hit Ratio', 'Buy']

        #Loop over each ticker string
        for i in range(len(Ticker_list_stripped_chunked)):
            API_url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={Ticker_strings_lst[i]}&types=stats,quote,chart&token={self.__API_key}'
            #Request batch stock data
            Stock_data_js = rq.get(API_url).json()
            #Loop over each stock
            for ticker in Ticker_strings_lst[i].split(','):
                #Write individual data frame for each stock and add to data_df_lst
                #Check if ticker is supported by the API
                if ticker in Momentum_strategy.API_symbol_lst:
                    #Work out 1 year average Momentum
                    no_data_points = len(Stock_data_js[ticker]['chart']) # no. trading days in ytd
                    avg_ytd_mom = 0 # Average 1 day momentum ytd
                    ytd_mom_hit_ratio = 0 # no. days with increased momentum

                    for j in range(no_data_points):
                        percent_chg_current = Stock_data_js[ticker]['chart'][j]['changePercent']
                        avg_ytd_mom += percent_chg_current / no_data_points
                        if percent_chg_current > 0: #I define hit ratio as number of days the stock increased in price
                            ytd_mom_hit_ratio += 1 / no_data_points

                    Stock_df = pd.DataFrame([[ticker, Stock_data_js[ticker]['quote']['latestPrice'],
                                            avg_ytd_mom, ytd_mom_hit_ratio, 'N/A']], columns=my_columns)

                else: #If ticker is not supported by the API
                    Stock_df = pd.DataFrame(columns=my_columns)
                data_df_lst.append(Stock_df)

        #Create 1 overall dataframe containing all relevant data for each stock
        #(I create multiple data frames and then use concat because append() is soon to be removed from pandas)
        data_df = pd.concat(data_df_lst, axis = 0, ignore_index = True)
        data_df.dropna(inplace = True)
        data_df.reset_index(inplace = True)

        return data_df

    def __analyse_momentum(self, Minimum_1d_momentum_hit_ratio, dataframe):
        dataframe.drop(dataframe[dataframe['YTD 1-Day Momentum Hit Ratio'] < Minimum_1d_momentum_hit_ratio].index, inplace = True)

        #Sort the remaining stocks by YTD average 1-Day percentage momentum
        dataframe.sort_values('YTD Average 1-Day Percentage Momentum', ascending = False, inplace = True)
        dataframe.reset_index(inplace = True)

        return dataframe

    def __Create_output_spreadsheet(self, _filename, _dataframe, __Index_filename, fractional_shares):
        #Cut dataframe to number of positions the user chooses to open
        _dataframe = _dataframe[:self.__number_of_positions]
        __number_of_positions_remaining = len(_dataframe)
        
        if not __number_of_positions_remaining:
            raise Exception('No stocks meet the momentum criteria you requested. Try lowering the 1-Day momentum hit ratio criterion.')
        
        #Retrive name of stock index from the index file name
        index_name = __Index_filename.split('_')[0]
        
        #Size of each EQUAL position
        position_size = self.__investment / __number_of_positions_remaining

        #Add number of stocks to buy to the spreadsheet
        for i in range(len(_dataframe)):
            if not fractional_shares:
                _dataframe.loc[i, 'Buy'] = mth.floor(position_size / _dataframe['Price'][i])
            else:
                _dataframe.loc[i, 'Buy'] = position_size / _dataframe['Price'][i]

        #Drop unnecessary columns
        _dataframe.drop(columns = ['level_0', 'index'], inplace = True)


        #Formatting the Excel sheet
        Momentum_strategy_file_name = _filename
        _dataframe.to_excel(Momentum_strategy_file_name, sheet_name = 'Order_Sheet', startrow = 5, index = False)

        #Load excel book
        Momentum_strategy_wb = xl.load_workbook(Momentum_strategy_file_name)
        Momentum_strategy_ws = Momentum_strategy_wb.active

        #Format percentages
        percentage_columns = ['C', 'D']
        for letter in percentage_columns:
            for i in range(7, 7 + __number_of_positions_remaining):
                Momentum_strategy_ws[letter + str(i)].number_format = '0.00%'

        #Add date and title
        title_font = Font(name = 'Arial', size = 18, color = '000080', bold = True)
        date_font = Font(name = 'Arial', size = 15)

        Momentum_strategy_ws['A1'].font = title_font
        Momentum_strategy_ws['A1'] = 'Momentum Trading Strategy (' + index_name + ')'

        Momentum_strategy_ws['A2'].font = date_font
        Momentum_strategy_ws['A2'] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #Adjust column width to show contents clearly
        for column_ in Momentum_strategy_ws.columns:
            column_letter_ = column_[0].column_letter
            width_ = max(len(cell.value) for cell in column_ if isinstance(cell.value, str))
            Momentum_strategy_ws.column_dimensions[column_letter_].width = width_ + 3

        #Save workbook
        Momentum_strategy_wb.save(Momentum_strategy_file_name)

    def __Add_summary_to_output_spreadsheet(self, __Output_filename, __Buy_list_length, __Capital_invested, __Capital_invested_percent):
        __Momentum_strategy_wb = xl.load_workbook(__Output_filename)
        __Momentum_strategy_ws = __Momentum_strategy_wb.active

        __Momentum_strategy_ws['A3'] = f'Positions to open: {__Buy_list_length}.'
        __Momentum_strategy_ws['A4'] = f'Capital invested: {"${:.2f}".format(__Capital_invested)}; {__Capital_invested_percent} of available capital.'

        __Momentum_strategy_wb.save(__Output_filename)
    
    #NOT hidden function for user to call
    def Order_sheet(self, Minimum_1d_momentum_hit_ratio: float, Index_filename__: str, ticker_tag_: str, Output_filename = 'OUTPUT/Order_sheet.xlsx', fractional_shares = False):

        assert isinstance(Minimum_1d_momentum_hit_ratio, float) or isinstance(Minimum_1d_momentum_hit_ratio, int), f'Momentum hit ratio, {Minimum_1d_momentum_hit_ratio}, must be a number between 0 and 1'
        assert Minimum_1d_momentum_hit_ratio >= 0 and Minimum_1d_momentum_hit_ratio < 1, f'Momentum hit ratio, {Minimum_1d_momentum_hit_ratio}, must be a number between 0 and 1'
        assert isinstance(Index_filename__, str), f'Input stock ticker list file name must be a string'
        assert isinstance(ticker_tag_, str), f'Input stock list file ticker tag must be a string'
        assert isinstance(Output_filename, str), f'Output order sheet filename must be a string'
        assert isinstance(fractional_shares, bool), f'The fractional shares option must be "True" or "False" for ordering fractional shares or not respectively'

        Ticker_strings_lst_, Ticker_list_stripped_chunked = self.__Ticker_strings_lst_(Index_filename__, ticker_tag_)
        df = self.__batch_request(Ticker_strings_lst_, Ticker_list_stripped_chunked)
        df = self.__analyse_momentum(Minimum_1d_momentum_hit_ratio, df)
        self.__Create_output_spreadsheet(Output_filename, df, Index_filename__, fractional_shares)

        
        price_list_ = list(df['Price'])
        Buy_list_ = list(df['Buy'])
        Buy_list_length = len([x for x in Buy_list_ if not isinstance(x, str) and x > 0])
        Capital_invested = sum([price_list_[i] * Buy_list_[i] for i in range(len(Buy_list_)) if not isinstance(Buy_list_[i], str)])
        Capital_invested_percent = "{0:.0%}".format(Capital_invested / self.__investment)
        minimum_investment_ = min(price_list_) * self.__number_of_positions

        self.__Add_summary_to_output_spreadsheet(Output_filename, Buy_list_length, Capital_invested, Capital_invested_percent)

        print('-----')

        if Buy_list_length == 0:
            print(f'Not enough capital to open a position, please invest a minimum of ${minimum_investment_}')

        else:
            if Buy_list_length < self.__number_of_positions:
                if Buy_list_length == 1:
                    print(f'Note: Number of positions smaller than desired because only {Buy_list_length} stock met the minimum momentum hit ratio criterion.')
                else:
                    print(f'Note: Number of positions smaller than desired because only {Buy_list_length} stocks met the minimum momentum hit ratio criterion.')

            print('-----')
            print(f'Order Sheet Summary:')
            print(f'Index: {Index_filename__.split("_")[0]}')
            print(f'Positions to open: {Buy_list_length}.')
            print(f'Capital invested: {"${:.2f}".format(Capital_invested)}; {Capital_invested_percent} of available capital.')
