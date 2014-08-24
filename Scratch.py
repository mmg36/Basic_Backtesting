__author__ = 'mehdi'
import numpy as np

def rand1():

    def1 = 0
    arr1 = [1, 2, 3, 4]
    for count in xrange(1, 10):
        def1 += 1
        arr1.append( def1)

    print arr1
    print "Hello"

rand1()