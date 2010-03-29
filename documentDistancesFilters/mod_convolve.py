import documentDistancesFilters
import numpy
import pprint
import scipy.signal
import sys

class Module_convolve(documentDistancesFilters.DistanceFilter):

    def process(self,matrix):
        filter = numpy.array(self._context["convolve"])
        a_convolved = scipy.signal.convolve2d(matrix, filter, mode="same")
        self._context["matrix"] = a_convolved
        return self._context["matrix"]

