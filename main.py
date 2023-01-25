'''
main
'''

#1. Import list of stocks we are interested in

class Equities:
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

        #Append each equities (instances) to the universe
        Equities.all.append(self)
