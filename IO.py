__author__ = 'mehdi'

import numpy as np
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
        employment_data = IO('/home/mehdi/Desktop/Employment_data.csv', False)
        price_data = IO('/home/mehdi/Desktop/NS_M1.csv', True)
        start_calculations = Calculations(2000, price_data.float_data, employment_data.float_data)
        start_calculations.comparison(3, 3)
        start_calculations.investment_algor()
        IO.write('/home/mehdi/Desktop/results1.csv', start_calculations.long_investment_status)
        IO.write('/home/mehdi/Desktop/results2.csv', start_calculations.short_investment_status)

        # IO.write('/home/mehdi/Desktop/results1.csv', start_calculations.investment)
        # IO.write('/home/mehdi/Desktop/results2.csv', start_calculations.cash)

IO.main()
