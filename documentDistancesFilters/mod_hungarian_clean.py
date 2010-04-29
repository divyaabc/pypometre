import documentDistancesFilters
import numpy
import pprint
import scipy.signal
import sys
import copy

class Module_hungarian_clean(documentDistancesFilters.DistanceFilter):

    def process(self,matrix):
        hungarian_pairs = self._context["pairs"]
        minDim = min(len(matrix),len(matrix[0]))
        m = [[1.0 for i in xrange(minDim)] for i in xrange(minDim)]
        clean_matrix = numpy.array(m)
        pairs = copy.copy(self._context["pairs"])
        l = list(pairs[0:minDim])
        l.sort()
        new_pairs = []
        
        for i,j in enumerate(self._context["pairs"]) :
          if i >= minDim :
            break
          new_j = l.index(j)
          clean_matrix[i][new_j] = matrix[i][j]
          new_pairs.append(new_j)

        self._context["pairs"] = new_pairs
        print clean_matrix
#        1/0
#        self._context["matrix"] = clean_matrix
        return clean_matrix

