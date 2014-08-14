__author__ = 'mehdi'

import numpy as np


class Calculations:
    def __init__(self, initial_money, read_price_data, read_employment_data):
        """

        :param initial_money:
        :param read_price_data:
        :param read_employment_data:
        """
        self.cash = np.zeros(len(read_employment_data) + 2)
        self.cash[0] = initial_money
        self.investment = np.zeros(len(read_employment_data) + 2)
        self.investment[0] = 0
        self.price_data = read_price_data
        self.employment_data = read_employment_data
        self.long_investment_status = np.zeros((len(read_employment_data), len(read_employment_data[1])), dtype=bool)
        self.short_investment_status = np.zeros((len(read_employment_data), len(read_employment_data[1])), dtype=bool)

    def comparison(self, long_positions, short_positions):

        longs = np.zeros(long_positions)
        shorts = np.zeros(short_positions)
        big_dummy = 0
        small_dummy = 110
        big_dummy_loc = -1
        small_dummy_loc = -1
        isnot_repetitive = True

        for count_row in xrange(0, len(self.employment_data)):
            for count_pos in xrange(0, long_positions):
                for count_col in xrange(0, len(self.employment_data[count_row])):
                    if self.employment_data[count_row][count_col] >= big_dummy and \
                                    self.employment_data[count_row][count_col] != -1:
                        if count_pos != -1:
                            for i in xrange(0, count_pos):
                                if count_col == longs[i]:
                                    isnot_repetitive = False and isnot_repetitive
                        if isnot_repetitive:
                            big_dummy = self.employment_data[count_row][count_col]
                            big_dummy_loc = count_col
                        isnot_repetitive = True
                    if big_dummy_loc != -1:
                        longs[count_pos] = big_dummy_loc
                        big_dummy_loc = -1
                big_dummy = 0
            for count_pos in xrange(0, short_positions):
                for count_col in xrange(0, len(self.employment_data[count_row])):
                    if self.employment_data[count_row][count_col] <= small_dummy and \
                                    self.employment_data[count_row][count_col] != -1:
                        if count_pos != 0:
                            for i in xrange(0, count_pos):
                                if count_col == shorts[i]:
                                    isnot_repetitive = False and isnot_repetitive
                        if isnot_repetitive:
                            small_dummy = self.employment_data[count_row][count_col]
                            small_dummy_loc = count_col
                        isnot_repetitive = True
                    if small_dummy_loc != -1:
                        shorts[count_pos] = small_dummy_loc
                        small_dummy_loc = -1
                small_dummy = 110

            for count_pos in xrange(0, long_positions):
                if longs[count_pos] != 0:
                    self.long_investment_status[longs[count_pos]] = True
            for count_pos in xrange(0, short_positions):
                if shorts[count_pos] != 0:
                    self.short_investment_status[shorts[count_pos]] = True

    def investment_algor(self):
        for count_row in xrange(0, len(self.long_investment_status)):
            for count_col in xrange(0, len(self.long_investment_status[count_row])):
                if self.long_investment_status[count_row][count_col]:
                    if self.long_investment_status[count_row - 1][count_col]:
                        self.investment[count_row + 1] += (self.price_data[count_row][count_col] - \
                                                           self.price_data[count_row - 1][count_col])
                    elif self.short_investment_status[count_row - 1][count_col]:
                        self.investment[count_row + 1] += -(self.price_data[count_row][count_col] + \
                                                            self.price_data[count_row - 1][count_col]) + \
                                                            self.price_data[count_row][count_col]
                        # First line for selling the shorted stock and second for Buying the long stock
                        self.cash[count_row + 1] += - self.price_data[count_row][count_col] + \
                                                    - self.price_data[count_row][count_col]
                        # One for shorting and the other for going long
                    else:
                        self.cash[count_row + 1] += -self.price_data[count_row][count_col]
                        self.investment[count_row + 1] += self.price_data[count_row][count_col]
                elif self.short_investment_status[count_row][count_col]:
                    if self.short_investment_status[count_row - 1][count_col]:
                        self.investment[count_row + 1] += self.price_data[count_row - 1][count_col]
                        self.cash[count_row + 1] -= self.price_data[count_row - 1][count_col]
                    elif self.long_investment_status[count_row - 1][count_col]:
                        self.investment[count_row + 1] += -self.price_data[count_row-1][count_col] \
                                                                      +self.price_data[count_row][count_col]
                        self.cash[count_row + 1] += -self.price_data[count_row][count_col] \
                                                                +self.price_data[count_row][count_col]
                    else:
                        self.investment[count_row + 1] += self.price_data[count_row][count_col]
                        self.cash[count_row + 1] -= self.price_data[count_row][count_col]
                else:
                    if self.short_investment_status[count_row - 1][count_col]:
                        self.investment[count_row + 1] += self.price_data[count_row][count_col]
                        self.cash[count_row + 1] -= self.price_data[count_row][count_col]
                    elif self.long_investment_status[count_row - 1][count_col]:
                        self.investment[count_row + 1] += self.price_data[count_row-1][count_col]
                        self.cash[count_row + 1] += -self.price_data[count_row][count_col]
            self.cash[count_row + 2] = self.cash[count_row + 1]
            self.investment[count_row + 2] = self.investment[count_row + 1]