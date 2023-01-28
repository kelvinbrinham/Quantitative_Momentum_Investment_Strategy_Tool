'''
main_OOP 2
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
    #Access API Key
    API_key_file_path = r'/Users/kelvinbrinham/Documents/GitHub/Secret_Files/IEX_API_Key.txt'
    API_key = linecache.getline(API_key_file_path, 10).strip()

    #Create list of tickers supported by the API from file created in another script
    list_of_tickers_supported_f = open(f'list_of_tickers_supported.json')
    list_of_tickers_supported_js = js.load(list_of_tickers_supported_f)

    #Create list of accepted tickers
    API_symbol_lst = [x['symbol'] for x in list_of_tickers_supported_js]

    def __init__(self, investment: float, number_of_positions: int):

        #Validate initialisation arguements
        assert investment > 0, f'Investment {investment} is negative!'
        assert number_of_positions > 0, f'Number of positions {number_of_positions} is negative!'
        assert isinstance(number_of_positions, int), f'Number of positions must be a positive integer'
        assert isinstance(investment, float) or isinstance(investment, int), f'Initial investment must be a positive number'

        self.__investment = investment
        self.__number_of_positions = number_of_positions


    def __Ticker_strings_lst_(self, filename: str, ticker_tag: str):
        universe_df = pd.read_csv(filename)

        #Create List of stock tickers
        Ticker_list = list(universe_df[ticker_tag])
        Ticker_list_stripped = []

        #Strip the ticker symbols to the base tickers (ignore exchanges, blank spaces etc.)
        for Ticker in Ticker_list:
            Ticker_list_stripped.append(Ticker.split()[0])

        #CHANGE <><><><><><><><><><><><><><><><><><><><><><><><>
        #Shorten for testing to reduce API requests (slow and limited number of requests on free trial)
        # Ticker_list_stripped = Ticker_list_stripped[:10]
        #<><><><><><><><><><><><><><><><><><><><><><><><><><><><>

        #Create sub lists of tickers with length chunk_length so that each API batch request isn't too long
        chunk_length = 100
        Ticker_list_stripped_chunked = [Ticker_list_stripped[x:x+chunk_length] for x in range(0, len(Ticker_list_stripped), chunk_length)]

        #List of strings, each containing multiple comma separated tickers ('AAPL,FB,...')
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
            API_url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={Ticker_strings_lst[i]}&types=stats,quote,chart&token={Momentum_strategy.API_key}'
            #Request batch stock data
            Stock_data_js = rq.get(API_url).json()
            for ticker in Ticker_strings_lst[i].split(','):
                #Write individual data frame for each stock and add to data_df_lst
                if ticker in Momentum_strategy.API_symbol_lst:
                    #Work out 1 year average Momentum
                    no_data_points = len(Stock_data_js[ticker]['chart']) # no. trading days in ytd
                    avg_ytd_mom = 0 # Average 1 day momentum ytd
                    ytd_mom_hit_ratio = 0 # no. days with increased momentum

                    for j in range(no_data_points):
                        percent_chg_current = Stock_data_js[ticker]['chart'][j]['changePercent']
                        avg_ytd_mom += percent_chg_current / no_data_points
                        if percent_chg_current > 0:
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

    def __Create_output_spreadsheet(self, _filename, _dataframe):
        _dataframe = _dataframe[:self.__number_of_positions]

        #Size of each EQUAL position
        position_size = self.__investment / self.__number_of_positions

        #Add number of stocks to buy to the spreadsheet
        for i in range(len(_dataframe)):
            _dataframe.loc[i, 'Buy'] = mth.floor(position_size / _dataframe['Price'][i])

        #Drop unnecessary columns
        _dataframe.drop(columns = ['level_0', 'index'], inplace = True)


        #Formatting the Excel sheet
        Momentum_strategy_file_name = _filename
        _dataframe.to_excel(Momentum_strategy_file_name, sheet_name = 'Order_Sheet', startrow = 3, index = False)

        #Load excel book
        Momentum_strategy_wb = xl.load_workbook(Momentum_strategy_file_name)
        Momentum_strategy_ws = Momentum_strategy_wb.active

        #Format percentages
        percentage_columns = ['C', 'D']
        for letter in percentage_columns:
            for i in range(5, 5 + self.__number_of_positions):
                Momentum_strategy_ws[letter + str(i)].number_format = '0.00%'

        #Add date and title
        title_font = Font(name = 'Arial', size = 18, color = '000080', bold = True)
        date_font = Font(name = 'Arial', size = 15)

        Momentum_strategy_ws['A1'].font = title_font
        Momentum_strategy_ws['A1'] = 'Momentum Trading Strategy'

        Momentum_strategy_ws['A2'].font = date_font
        Momentum_strategy_ws['A2'] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #Adjust column width to show contents clearly
        for column_ in Momentum_strategy_ws.columns:
            column_letter_ = column_[0].column_letter
            width_ = max(len(cell.value) for cell in column_ if isinstance(cell.value, str))
            Momentum_strategy_ws.column_dimensions[column_letter_].width = width_ + 3

        #Save workbook
        Momentum_strategy_wb.save(Momentum_strategy_file_name)


    def Order_Sheet(self, Minimum_1d_momentum_hit_ratio, Index_filename__, ticker_tag_, Output_filename):
        Ticker_strings_lst_, Ticker_list_stripped_chunked = self.__Ticker_strings_lst_(Index_filename__, ticker_tag_)
        df = self.__batch_request(Ticker_strings_lst_, Ticker_list_stripped_chunked)
        df = self.__analyse_momentum(Minimum_1d_momentum_hit_ratio, df)
        self.__Create_output_spreadsheet(Output_filename, df)

        # if len(df) <
