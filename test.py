'''
test
'''


class Equity:
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

        #Append each equity (instances) to the universe
        Equity.universe.append(self)

        #-----------------------------
        #ADD INSTANTIATE FROM CSV HERE!!!
        #-----------------------------

    def __repr__(self):
    #Representing instance nicely
        return f"{self.__class__.__name__}('{self.__name}', '{self.__ticker}', {self.__price}, {self.__quantity})"


Apple = Equity('Apple', 'AAPL', 66, 1)
Orange = Equity('Orange', 'O', 56, 2)
