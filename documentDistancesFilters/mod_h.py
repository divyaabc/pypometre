import documentDistancesFilters
import hungarian
import sys
sys.path.append('..')

from dataStructures import LinedMatrix
import tool_numpy as tn
import tool_dataStructures as tds

class Module_h(documentDistancesFilters.DistanceFilter):
  def process(self, matrixOrig):
    matrixOrig = tn.matrix2numpy(matrixOrig.getMatrix())
    lDim = sorted([len(matrixOrig), len(matrixOrig[0])])

    matrix = tn.squarify(matrixOrig,1.)
    a = tn.matrix2numpy(matrix)
    pairs = list(hungarian.lap(a)[0])

    a_void = tn.numpy_resize(a, lDim)
    a_void.fill(1.0)

    for i in xrange(lDim[0]) :
      j = pairs[i]
      a_void[i][j] = matrix[i][j]

#    for i, j in enumerate(pairs):
#      if i >= lDim[0] :
#        break
#      a_void[i][j] = matrix[i][j]

    self._context["pairs"] = pairs

    lA_void = LinedMatrix(0,0)
    lA_void.convertDistMatrix(a_void)

    return lA_void
