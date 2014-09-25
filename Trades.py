__author__ = 'mehdi'
import numpy as np


class Trades():

    def __init__(self, investment_period, number_of_countries, initial_money, price_data):
        self.investment_period = investment_period  # time period in which investment is taking place.
        self.number_of_countries = number_of_countries # number of countries that you are investing in. This is useful
        # when you want to invest in multiple countries at one go.
        self.cash = np.zeros(investment_period + 1) # Initial cash invested
        self.percentage_return = np.zeros(investment_period+1) # Percentage return on the initial investment
        self.cash[0] = initial_money # initial money which is basically the initial cash that you invest.
        self.initial_money = initial_money # Initial money invested
        self.investment = np.zeros(investment_period + 1)
       # self.cash_short_margin = np.zeros(investment_period, number_of_countries)
        self.price_data = price_data
        # Price of the stocks or any that type of assets that you would like to invest in.

    def earning_percentage(self):
        self.percentage_return[0] = 1
        for count_row in xrange(1, self.investment_period+1):
            self.percentage_return[count_row] = (self.investment[count_row]+self.cash[count_row]-self.investment[count_row - 1] - self.cash[count_row - 1])/ \
                                                (self.investment[count_row - 1] + self.cash[count_row - 1]) + \
                                                self.percentage_return[count_row - 1]

class Overal_neutral (Trades):
    def __init__(self, investment_period, number_of_countries, initial_money, price_data):
        Trades.__init__(self, investment_period, number_of_countries, initial_money, price_data)

    def buy_long(self, count_row, count_col):
        self.cash[count_row] -= self.price_data[count_row][count_col]
        ss1 = self.price_data[count_row][count_col]
        self.investment[count_row] += self.price_data[count_row][count_col]

    def sell_long(self, count_row, count_col):
        self.cash[count_row] += self.price_data[count_row][count_col]
        self.investment[count_row] -= self.price_data[count_row - 1][count_col]

    def buy_short(self, count_row, count_col):
        self.investment[count_row] -= self.price_data[count_row][count_col]
        self.cash[count_row] += self.price_data[count_row][count_col]

    def sell_short(self, count_row, count_col):
        self.cash[count_row] -= self.price_data[count_row][count_col]
        self.investment[count_row] += self.price_data[count_row - 1][count_col]

    def keep_long(self, count_row, count_col):
        self.investment[count_row] += (self.price_data[count_row][count_col] - \
                                            self.price_data[count_row - 1][count_col])

    def keep_short(self, count_row, count_col):
        self.investment[count_row] -= (self.price_data[count_row][count_col] - \
                                            self.price_data[count_row - 1][count_col])

    # At the moment keep long and keep short are not very important other than making sure that balance is kept constant
    # but the main intention of writing these methods were for the trading costs if they want to be implemented later.

    def sell_short_nodata(self, count_row, count_col):
        self.investment[count_row] += self.price_data[count_row - 1][count_col]
        self.cash[count_row] -= self.price_data[count_row - 1][count_col]
    # Liquidates all of the short positions when there is data missing for that positions in that particular time.

    def sell_long_nodata(self, count_row, count_col):
        self.investment[count_row] -= self.price_data[count_row - 1][count_col]
        self.cash[count_row] += self.price_data[count_row - 1][count_col]
    # Liquidates all of the long positions when there is data missing for that position in that particular time.

    def refresh_balance(self, count_row):
        self.cash[count_row + 1] = self.cash[count_row]
        self.investment[count_row + 1] = self.investment[count_row]
    #if analysing more than one country, then total balance is moved from one point in time to next
    # (e.g one month to next)