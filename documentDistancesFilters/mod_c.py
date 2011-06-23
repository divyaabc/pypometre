import documentDistancesFilters
import sys
sys.path.append('..')
from dataStructures import *
import tool_dataStructures as tds
import tool_numpy as tn

class Module_c(documentDistancesFilters.DistanceFilter):
  def process(self,lMatrix):
    lPatch = LinedMatrix(0,0)
    lPatch.convertDistMatrix(self._context['convolve'])
    lMatrix = tds.convolve_linedMatrix(lMatrix, lPatch, "m", 1.0)
#    f = tn.matrix2numpy(self._context['convolve'])
#    a_convolved = tn.matrix2matrix_convolved(matrix, f)
    self._context["matrix"] = lMatrix
    return lMatrix

