__author__ = 'mehdi'
import numpy as np

class Trades:
    def __init__(self, investment_period, number_of_countries, initial_money, price_data):
        self.investment_period = investment_period
        self.number_of_countries = number_of_countries
        self.cash = np.zeros(investment_period + 1)
        self.percentage_return = np.zeros(investment_period+1)
        self.cash[0] = initial_money
        self.investment = np.zeros(investment_period + 1)
        self.cash_short_margin = np.zeros(investment_period, number_of_countries)
        self.price_data = price_data

    def earning_percentage(self):
        for count_row in xrange(0, self.investment_period+1):
            self.percentage_return[count_row] = (self.investment[count_row]+self.cash[count_row])/self.cash[0]

class Overal_neutral (Trades):
    def __init__(self, investment_period, number_of_countries, initial_money):
        Trades.__init__(self, investment_period, number_of_countries, initial_money)

    def buy_long(self, count_row, count_col):
        self.cash[count_row] -= self.price_data[count_row][count_col]
        self.investment[count_row] += self.price_data[count_row][count_col]

    def sell_long(self, count_row, count_col):
        self.cash[count_row][count_col] += self.price_data[count_row][count_col]
        self.investment[count_row][count_col] -= self.price_data[count_row - 1][count_col]

    def buy_short(self, count_row, count_col):
        self.investment[count_row] -= self.price_data[count_row][count_col]
        self.cash[count_row] += self.price_data[count_row][count_col]

    def sell_short(self, count_row, count_col):
        self.cash[count_row][count_col] -= self.price_data[count_row][count_col]
        self.investment[count_row][count_col] += self.price_data[count_row - 1][count_col]

    def keep_long(self, count_row, count_col):
        self.investment[count_row] += (self.price_data[count_row][count_col] - \
                                            self.price_data[count_row - 1][count_col])

    def keep_short(self, count_row, count_col):
        self.investment[count_row] -= (self.price_data[count_row][count_col] - \
                                            self.price_data[count_row - 1][count_col])

    def sell_short_nodata(self, count_row, count_col):
        self.investment[count_row] += self.price_data[count_row - 1][count_col]
        self.cash[count_row] -= self.price_data[count_row - 1][count_col]

    def sell_long_nodata(self, count_row, count_col):
        self.investment[count_row] -= self.price_data[count_row - 1][count_col]
        self.cash[count_row] += self.price_data[count_row - 1][count_col]

    def refresh_balance(self, count_row):
        self.cash[count_row + 1] = self.cash[count_row]
        self.investment[count_row + 1] = self.investment[count_row]