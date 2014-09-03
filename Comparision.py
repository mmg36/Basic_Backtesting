__author__ = 'mehdi'

import numpy as np
from Trades import Overal_neutral

class Calculations:
    def __init__(self, initial_money, read_price_data, read_employment_data):
        """

        :param initial_money:
        :param read_price_data:
        :param read_employment_data:
        """
        self.number_of_countries = len(read_employment_data[1])
        self.cash = np.zeros(len(read_employment_data) + 1)
        self.initial_money = initial_money
        self.investment = np.zeros(len(read_employment_data) + 1)
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
                    if self.price_data[count_row][count_col] > 0 and \
                                    self.employment_data[count_row][count_col] >= big_dummy and \
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
                    if self.price_data[count_row][count_col] > 0 and \
                                    self.employment_data[count_row][count_col] <= small_dummy and \
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
                    self.long_investment_status[count_row][longs[count_pos]] = True
            for count_pos in xrange(0, short_positions):
                if shorts[count_pos] != 0:
                    self.short_investment_status[count_row][shorts[count_pos]] = True

    def investment_algor(self):
        # This is for the first datapoint in time (Problem with count_row-1 being smaller than 0)
        start_trading = Overal_neutral(len(self.cash), len(self.read_employment_data[1]), self.initial_money)
        count_row = 0
        for count_col in xrange(0, len(self.long_investment_status[count_row])):
            if self.long_investment_status[count_row][count_col]:
                start_trading.buy_long(count_row, count_col)
            elif self.short_investment_status[count_row][count_col]:
                start_trading.buy_short(count_row, count_col)
        # This is for the rest of the datapoints
        for count_row in xrange(1, len(self.long_investment_status)):
            for count_col in xrange(0, len(self.long_investment_status[count_row])):
                if self.long_investment_status[count_row][count_col]:
                    if self.long_investment_status[count_row - 1][count_col]:
                        start_trading.keep_long(count_row, count_col)
                    elif self.short_investment_status[count_row - 1][count_col]:
                        start_trading.sell_short(count_row, count_col)
                        start_trading.buy_long(count_row, count_col)
                    else:
                        start_trading.buy_long(count_row, count_col)
                elif self.short_investment_status[count_row][count_col]:
                    if self.short_investment_status[count_row - 1][count_col]:
                        start_trading.keep_short(count_row, count_col)
                    elif self.long_investment_status[count_row - 1][count_col]:
                        start_trading.sell_long(count_row, count_col)
                        start_trading.buy_short(count_row, count_col)
                    else:
                        start_trading.buy_short(count_row, count_col)
                else:
                    if self.price_data[count_row][count_col] > 0:
                        if self.short_investment_status[count_row - 1][count_col]:
                            start_trading.sell_short(count_row, count_col)
                        elif self.long_investment_status[count_row - 1][count_col]:
                            start_trading.sell_long(count_row, count_col)
                    else:
                        if self.short_investment_status[count_row - 1][count_col]:
                            start_trading.sell_short_nodata(count_row, count_col)
                        elif self.long_investment_status[count_row - 1][count_col]:
                            start_trading.sell_long_nodata(count_row, count_col)

            start_trading.refresh_balance(count_row)

        for count_col in xrange(0, len(self.number_of_countries)):
            if self.short_investment_status[count_row][count_col]:
                            start_trading.sell_short(count_row, count_col)
            elif self.long_investment_status[count_row][count_col]:
                            start_trading.sell_long(count_row, count_col)

        start_trading.earning_percentage()
