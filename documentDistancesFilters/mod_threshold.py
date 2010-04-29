import documentDistancesFilters
import hungarian
import numpy
import pprint
import scipy.signal
import sys

class Module_threshold(documentDistancesFilters.DistanceFilter):

    def process(self,matrix):
        a_seuil = matrix.copy()
        for i,line in enumerate(matrix) :
          for j,val in enumerate(line) :
            if val < self._context["threshold"][0] :
              a_seuil[i][j]  = 0
            elif val > self._context["threshold"][1] :
              a_seuil[i][j]  = 1
            else :
#              print "=", val, self._context["threshold"]
              a_seuil[i][j] = val

        self._context["matrix"] = a_seuil
        return a_seuil

    
