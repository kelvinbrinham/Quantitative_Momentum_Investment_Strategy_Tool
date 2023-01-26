'''
test 2
'''

lst_ = ['AAPL', 'MMM', 'AOS', 'ABT']
lst_string = ''

for ticker in lst_:
    lst_string = lst_string + ',' + ticker
lst_string = lst_string[1:]



print(lst_string)
