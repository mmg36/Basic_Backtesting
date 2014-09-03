__author__ = 'mehdi'

import numpy as np
import csv
from Comparision import Calculations


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
        employment_data = IO('/home/mehdi/Desktop/Productivity.csv', False)
        price_data = IO('/home/mehdi/Desktop/NS_M_CLI.csv', True)
        start_calculations = Calculations(0, price_data.float_data, employment_data.float_data)
        start_calculations.comparison(long_positions, short_positions)
        start_calculations.investment_algor()
        IO.write('/home/mehdi/Desktop/results1_C.csv', start_calculations.investment)
        IO.write('/home/mehdi/Desktop/results1_I.csv', start_calculations.cash)

        short_positions = 3
        long_positions = 3
        start_calculations = Calculations(0, price_data.float_data, employment_data.float_data)
        start_calculations.comparison(long_positions, short_positions)
        start_calculations.investment_algor()
        IO.write('/home/mehdi/Desktop/results2_C.csv', start_calculations.investment)
        IO.write('/home/mehdi/Desktop/results2_I.csv', start_calculations.cash)

        short_positions = 5
        long_positions = 5
        start_calculations = Calculations(0, price_data.float_data, employment_data.float_data)
        start_calculations.comparison(long_positions, short_positions)
        start_calculations.investment_algor()
        IO.write('/home/mehdi/Desktop/results3_C.csv', start_calculations.investment)
        IO.write('/home/mehdi/Desktop/results3_I.csv', start_calculations.cash)


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
