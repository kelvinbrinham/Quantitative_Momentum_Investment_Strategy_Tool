'''
test
'''


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


    def total_investment_value(self):
        return self.__price * self.__quantity


    def total_value(self):
        


    def __repr__(self):
    #Representing instance nicely
        return f"{self.__class__.__name__}('{self.__ticker}', {self.__price}, {self.__quantity})"


Apple = Equity('AAPL', 66, 1)


print(Apple)
