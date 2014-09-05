__author__ = 'mehdi'

import numpy as np
from Trades import Overal_neutral
import csv


class Calculations:
    def __init__(self, initial_money, read_price_data, read_employment_data, output_address):
        """

        :param initial_money:
        :param read_price_data:
        :param read_employment_data:
        """
        self.output_address = output_address
        self.number_of_countries = len(read_employment_data[1])
        self.cash = np.zeros(len(read_employment_data) + 1)
        self.initial_money = initial_money
        self.investment = np.zeros(len(read_employment_data) + 1)
        self.price_data = read_price_data
        self.employment_data = read_employment_data
        self.investment_status = np.zeros((len(read_employment_data), len(read_employment_data[1])), dtype=int)
        self.CLI_rise_status = np.zeros((len(read_employment_data), len(read_employment_data[1])), dtype=bool)
        self.CLI_largerthanhundred_status = np.zeros((len(read_employment_data), len(read_employment_data[1])), dtype=bool)

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
                    self.investment_status[count_row][longs[count_pos]] += 1
            for count_pos in xrange(0, short_positions):
                if shorts[count_pos] != 0:
                    self.investment_status[count_row][shorts[count_pos]] -= 1

    def investment_algor(self):
        # This is for the first datapoint in time (Problem with count_row-1 being smaller than 0)
        start_trading = Overal_neutral(len(self.cash), self.number_of_countries, self.initial_money, self.price_data)
        count_row = 0
        for count_col in xrange(0, len(self.investment_status[count_row])):
            if self.investment_status[count_row][count_col] > 0:
                start_trading.buy_long(count_row, count_col)
            elif self.investment_status[count_row][count_col] < 0:
                start_trading.buy_short(count_row, count_col)

        one_or_more_long = True
        while start_trading.cash[count_row] > 0 and one_or_more_long:
            one_or_more_long = False
            for count_col in xrange(0, len(self.investment_status[count_row])):
                if self.investment_status[count_row][count_col] > 0:
                    one_or_more_long = False
                    self.investment_status[count_row][count_col] += 1
                    start_trading.buy_long(count_row, count_col)

        if start_trading.cash[count_row] < 0:
            start_trading.initial_money += -1 * start_trading.cash[count_row]
            start_trading.cash[count_row] = 0

        start_trading.refresh_balance(count_row)

        # This is for the rest of the datapoints
        for count_row in xrange(1, len(self.investment_status)):
            for count_col in xrange(0, len(self.investment_status[count_row])):
                if self.investment_status[count_row][count_col] > 0:
                    if self.investment_status[count_row - 1][count_col] > 0:
                        for iter in xrange(0, self.investment_status[count_row - 1][count_col]):
                            start_trading.keep_long(count_row, count_col)
                    elif self.investment_status[count_row - 1][count_col] < 0:
                        for iter in xrange(0, -1 * self.investment_status[count_row - 1][count_col]):
                            start_trading.sell_short(count_row, count_col)
                        start_trading.buy_long(count_row, count_col)
                    else:
                        start_trading.buy_long(count_row, count_col)
                elif self.investment_status[count_row][count_col] < 0:
                    if self.investment_status[count_row - 1][count_col] < 0:
                        for iter in xrange(0, -1 * self.investment_status[count_row - 1][count_col]):
                            start_trading.keep_short(count_row, count_col)
                    elif self.investment_status[count_row - 1][count_col] > 0:
                        for iter in xrange(0, self.investment_status[count_row - 1][count_col]):
                            start_trading.sell_long(count_row, count_col)
                        start_trading.buy_short(count_row, count_col)
                    else:
                        start_trading.buy_short(count_row, count_col)
                else:
                    if self.price_data[count_row][count_col] > 0:
                        if self.investment_status[count_row - 1][count_col] < 0:
                            for iter in xrange(0, -1 * self.investment_status[count_row - 1][count_col]):
                                start_trading.sell_short(count_row, count_col)
                        elif self.investment_status[count_row - 1][count_col] > 0:
                            for iter in xrange(0, self.investment_status[count_row - 1][count_col]):
                                start_trading.sell_long(count_row, count_col)
                    else:
                        if self.investment_status[count_row - 1][count_col] < 0:
                            for iter in xrange(0, self.investment_status[count_row - 1][count_col]):
                                start_trading.sell_short_nodata(count_row, count_col)
                        elif self.investment_status[count_row - 1][count_col] > 0:
                            for iter in xrange(0, self.investment_status[count_row - 1][count_col]):
                                start_trading.sell_long_nodata(count_row, count_col)
            one_or_more_long = True
            while start_trading.cash[count_row] > 0 and one_or_more_long:
                one_or_more_long = False
                for count_col in xrange(0, len(self.investment_status[count_row])):
                    if self.investment_status[count_row][count_col] > 0:
                        one_or_more_long = True
                        self.investment_status[count_row][count_col] += 1
                        start_trading.buy_long(count_row, count_col)

            if start_trading.cash[count_row] < 0:
                start_trading.initial_money += -1 * start_trading.cash[count_row]
                start_trading.cash[count_row] = 0
            start_trading.refresh_balance(count_row)

        for count_col in xrange(0, self.number_of_countries):
            if self.investment_status[count_row][count_col] < 0:
                for iter in xrange(0, -1 * self.investment_status[count_row - 1][count_col]):
                            start_trading.sell_short(count_row, count_col)
            elif self.investment_status[count_row][count_col] > 0:
                for iter in xrange(0, self.investment_status[count_row - 1][count_col]):
                            start_trading.sell_long(count_row, count_col)
        start_trading.refresh_balance(count_row)

        start_trading.earning_percentage()
        IO.write(self.output_address+'_C.csv', start_trading.investment)
        IO.write(self.output_address+'_I.csv', start_trading.cash)
        IO.write(self.output_address+'_P.csv', start_trading.percentage_return)


    def CLI_intertemporal_investment(self):
        for count_row in xrange(0, ):
            for count_col in xrange(0,):
                if self.CLI_largerthanhundred_status[count_row][count_col]:
                    self.investment_status[count_row][count_col] += 1
                else:
                    if self.CLI_rise_status:
                        self.investment_status[count_row][count_col] += 1
                    else:
                        self.investment_status[count_row][count_col] -= 1

    def CLI_intertemporal(self):
        test_value = 100
        count_row = 0
        for count_col in xrange(0,):
            if self.employment_data[count_row][count_col] >= test_value:
                self.CLI_largerthanhundred_status[count_row][count_col] = True
            else:
                self.CLI_largerthanhundred_status[count_row][count_col] = False
        for count_row in xrange(1,):
            for count_col in xrange (0,):
                if self.employment_data[count_row][count_col] >= test_value:
                    self.CLI_largerthanhundred_status[count_row][count_col] = True
                else:
                    self.CLI_largerthanhundred_status[count_row][count_col] = False
                if self.employment_data[count_row][count_col] >= self.employment_data[count_row-1][count_col] and \
                                                            self.employment_data[count_row][count_col] > 0:
                    self.CLI_rise_status[count_row][count_col] = True
                else:
                    self.CLI_rise_status[count_row][count_col] = False


class IO:

    def __init__(self, file_address, isshareprice):

        try:
            self.text_data = np.loadtxt(file_address,
                                        delimiter=',',
                                        dtype='str')

        except Exception, e:
            print str(e)

        self.float_data = np.zeros((len(self.text_data)-1, len(self.text_data[1])-1))
        for count_row in xrange(1, len(self.text_data)):
            for count_col in xrange(1, len(self.text_data[count_row])):
                if self.text_data[count_row][count_col] == ':' or self.text_data[count_row][count_col] == "":
                    if isshareprice:
                        self.float_data[count_row-1][count_col-1] = 0
                    else:
                        self.float_data[count_row-1][count_col-1] = -1
                else:
                    self.float_data[count_row-1][count_col-1] = float(self.text_data[count_row][count_col])

    @staticmethod
    def write(output_address, parameter):
        np.savetxt(output_address, parameter, delimiter=",")

    @staticmethod
    def main():
        short_positions = 1
        long_positions = 1
        output_1 ='/home/mehdi/Desktop/results1'
        employment_data = IO('/home/mehdi/Desktop/CLI_Data1.csv', False)
        price_data = IO('/home/mehdi/Desktop/NS_M_CLI.csv', True)
        start_calculations = Calculations(1000, price_data.float_data, employment_data.float_data, output_1)
        #start_calculations.comparison(long_positions, short_positions)
        start_calculations.CLI_intertemporal()
        start_calculations.CLI_intertemporal_investment()
        start_calculations.investment_algor()

        short_positions = 3
        long_positions = 3
        output_2 = '/home/mehdi/Desktop/results2'
        start_calculations = Calculations(1000, price_data.float_data, employment_data.float_data, output_2)
        #start_calculations.comparison(long_positions, short_positions)
        start_calculations.CLI_intertemporal()
        start_calculations.CLI_intertemporal_investment()
        start_calculations.investment_algor()

        short_positions = 4
        long_positions = 4
        output_3 = '/home/mehdi/Desktop/results3'
        start_calculations = Calculations(1000, price_data.float_data, employment_data.float_data, output_3)
        #start_calculations.comparison(long_positions, short_positions)
        start_calculations.CLI_intertemporal()
        start_calculations.CLI_intertemporal_investment()
        start_calculations.investment_algor()


    @staticmethod
    def main1():
        employment_data = IO('/home/mehdi/Desktop/Employment_data.csv', '/home/mehdi/Desktop/CLI.csv', False)
        employment_data.clear_dataset()

class Clean_dataset:
    def __init__(self, file_address):
        self.clear_data = []
        try:
            self.text_data = np.loadtxt(file_address,
                                        delimiter=',',
                                        dtype='str')

        except Exception, e:
            print str(e)

    def clear_dataset(self):
        i = -1
        for count_row in xrange(0, len(self.text_data1)):
            if self.text_data1[count_row][3] != self.text_data1[count_row-1][3]:
                i += 1
                self.clear_data.append([])
            self.clear_data[i].append(self.text_data1[count_row][4])
        with open('/home/mehdi/Desktop/CLI_Out.csv', 'wb') as out_file:
            wr = csv.writer(out_file, quoting=csv.QUOTE_ALL)
            wr.writerows(map(list, map(None, *self.clear_data)))
            out_file.close()

IO.main()
