import documentDistancesFilters
import numpy
import pprint
import scipy.signal
import sys

class Module_convolve(documentDistancesFilters.DistanceFilter):

    def process(self,matrix):
#        print matrix
#        1/0
        filter = numpy.array(self._context["convolve"])
        a_convolved = scipy.signal.convolve2d(matrix, filter, mode="same")
        self._context["matrix"] = a_convolved
        return a_convolved

