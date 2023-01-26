'''
Storage
'''


API_url = f'https://cloud.iexapis.com/stable/stock/{ticker}/stats?token={API_key}'


#Perform the batch API request
Stock_data_js = rq.get(API_url).json()
print(Stock_data_js)

month1ChangePercent = Stock_data_js['month1ChangePercent']
print(month1ChangePercent)
