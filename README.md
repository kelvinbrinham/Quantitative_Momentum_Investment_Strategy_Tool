# Quantitative_Momentum_Investment_Strategy_Machine

Summary: This tool takes investment inputs and analysis stocks to find the ones with the most high-quality momentum. The code then produces an output order spreadsheet outlining which and how many stocks to purchase.

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

Scripts:

main.py - Here we import the Momentum_strategy class and use the tool

Momentum_strategy_class.py - Contains the class which performs the analysis and function of the tool.

Accessory_scripts/Checking_API_Accepted_Tickers.py - Checks which tickers (stocks) are supported by the IEX API and saves them to a JSON file list_of_tickers_supported.json. This script needn’t be used but I included it for completeness so you can see where list_of_tickers_supported.json came from.

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

Files:

S&P500_Stocks.csv - Contains the stock tickers in the S&P500 index. I found this online and included it as an example input.

FTSE100_Stocks.csv - Contains the stock tickers in the FTSE100 index. I found this online and included it as an example input.

list_of_tickers_supported.json - Contains the stock tickers which are supported by the IEX API I use.

OUTPUT/Order_sheet_EXAMPLE.xlsx - Example output order sheet that the tool produces.

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

IMPORTANT:
The API key I use is private. It is stored in a config.py file on my local machine and loaded in main.py. YOU MUST input your API_key as outlined below. You may also choose to create a config.py file containing your API key which you import so as to keep it secret. I have left a commented import example on line 9 in main.py.

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

Description of analysis:
The tool analysis two characteristics of stocks. The mean 1-Day momentum (the daily percentage change in stock price) for the year to date (YTD); and, ‘Momentum Hit Ratio (MHR)’. I define MHR as the fraction of days within the YTD in which the share increased in price. This introduces a measure of the quality of momentum. The tool cuts off stocks with an MHR below a user-defined value and then picks the stocks with the highest mean 1-Day momentum. The tool then buys equal size positions in the stocks with the most high quality momentum. 

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

Instructions for use (please read Description of analysis first):
Note: All currency is USD

1. Input your personal API_key in a config.py file
2. Initialise the Momentum_strategy class with the amount you want to invest and the number of shares you wish to buy. E.g. my_strategy = Momentum_strategy(CASH_TO_INVEST, NUMBER_SHARES_TO_BUY, API_KEY)
3. Utilise the Order_Sheet() class function like so:

my_strategy.Order_sheet(MOMENTUM_HIT_RATIO: float, INDEX_FILE: str, TICKER_TAG: str, OUTPUT_FILE_PATH: str, FRACTIONAL_SHARES: bool)

MOMENTUM_HIT_RATIO = The minimum MHR needed for a stock to be ordered
INDEX_FILE = The file path for the .csv file containing the stocks in the desired index
TICKER_TAG = The tag for the ticker column in the INDEX_FILE. E.g. it is ’Symbol’ in the included S&P500_Stocks.csv file and ‘ticker’ in the included FTSE100_Stocks.csv file
OUTPUT_FILE_PATH (default: OUTPUT/Order_sheet.xlsx) = File path for output order spreadsheet
FRACTIONAL_SHARES (default: False) = Set True to allow the order of fractional shares, False otherwise. 


Example Input:
my_strategy = Momentum_strategy(10000, 20, API_KEY)
my_strategy.Order_sheet(0.5, S&P500_Stocks.csv, 'Symbol', OUTPUT/Order_sheet_1.xlsx, False)

The above code will find the 20 stocks in the S&P500 with the highest YTD mean 1-Day momentum which also has a MHR above 0.5. The code works out how many shares to buy in each stock such that each stock position has an equal share of the 10,000 USD invested. I inputted False, therefore the code only calculates the order of whole shares by rounding positions down, meaning the final positions won't all be equal in size. The example spreadsheet i included is produced form this code.

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

Future:
There are many improvements I can envisage, here are just a few:
- Increase the complexity of analysis with extra metrics
- A portfolio system using OOP which keeps track of stocks purchased and their returns etc. (although there are many apps for this of course)
- Add extra user choice (such as 1-Month momentum etc.)




