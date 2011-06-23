import documentDistancesFilters
import copy

import tool_numpy as tn
from array import array

import sys
sys.path.append('..')

from dataStructures import LinedMatrix
import tool_numpy as tn
import tool_dataStructures as tds



##module Hungarian_clean
class Module_hc(documentDistancesFilters.DistanceFilter):
  def process(self,matrix):
    matrix = tn.matrix2numpy(matrix.getMatrix())
    hungarian_pairs = self._context["pairs"]
    minDim = min(len(matrix),len(matrix[0]))
    m = [array('f',[1.0 for _ in xrange(minDim)]) for _ in xrange(minDim)]

    clean_matrix = tn.matrix2numpy(m)
#    pairs = copy.copy(self._context["pairs"])
    pairs = self._context['pairs']
    l = pairs[0:minDim]
    l.sort()
    new_pairs = []

    for i,j in enumerate(self._context["pairs"]) :
      if i >= minDim :
        break
      new_j = l.index(j)
      clean_matrix[i][new_j] = matrix[i][j]
      new_pairs.append(new_j)
    self._context["pairs"] = new_pairs

    lClean_matrix = LinedMatrix(0,0)
    lClean_matrix.convertDistMatrix(clean_matrix)
    return lClean_matrix
