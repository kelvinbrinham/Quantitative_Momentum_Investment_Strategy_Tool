'''
test 2
'''
from main import Ticker_list_stripped

print(Ticker_list_stripped)

Ticker_list_stripped_chunked = [Ticker_list_stripped[x:x+3] for x in range(0, len(Ticker_list_stripped), 3)]

for i in range(len(Ticker_list_stripped_chunked)):
    print(Ticker_list_stripped_chunked[i])
    print(len(Ticker_list_stripped_chunked[i]))

print(i)
