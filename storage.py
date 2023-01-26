'''
Storage
'''


#FLatten list

lst_ = [{'symbol': 'AAPL'}, {'symbol': 'TSLA'}]

lst2 = [x['symbol'] for x in lst_]

print(lst2)
