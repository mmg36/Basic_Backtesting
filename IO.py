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

    def write_to_csv(self, output_address, investment, cash):
        for count in xrange(0, len(investment)):
            self.savetxt(output_address,
                         (output_address,investment),
                         delimiter=',')

    @staticmethod
    def main():
        employment_data = IO('/home/mehdi/Desktop/Employment_data1.csv', False)
        price_data = IO('/home/mehdi/Desktop/NS_M1.csv', True)
        start_calculations = Calculations(2000, price_data.float_data, employment_data.float_data)
        start_calculations.comparison(5, 5)
        start_calculations.investment()

IO.main()

