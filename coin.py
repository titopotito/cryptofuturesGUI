from ftxdata import getftxdata

class Coin():
    def __init__(self, ticker):
        self.__data = getftxdata('https://ftx.com/api/futures/' + ticker)
        self.__ticker = ticker
        self.__price = self.__data['mark']
        self.__percent = str(round(self.__data['change24h']*100, 2)) + '%'

    def get(self, attribute):
        if attribute == 'ticker':
            return self.__ticker
        elif attribute == 'price':
            return self.__price
        elif attribute == '%':
            return self.__percent
        else:
            return self.__data