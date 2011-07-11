import documentDistancesFilters
import hungarian
#import munk
import sys
sys.path.append('..')
from array import array

from dataStructures import LinedMatrix
import tool_dataStructures as tds

class Module_h(documentDistancesFilters.DistanceFilter):
  def process(self, matrixOrig):
    lDim = sorted([matrixOrig._height, matrixOrig._width])
    matrixOrig = tds.squarify(matrixOrig,1.)
    matrix = matrixOrig.getMatrix()
    nMatrix = [[1.-val for val in line] for line in matrix]
    pairs = hungarian.lap(matrix)[0]
#    res = munk.maxWeightMatching(nMatrix)
#    pairs = [res[0][i] for i in res[0].keys()]

    lA_void = LinedMatrix(lDim[1],lDim[0],1.)

    for i in xrange(lDim[0]) :
#      j = pairs[i]
      ni = pairs[i]+i*lA_void._width
      lA_void.data[ni] = matrix[i][pairs[i]]
#      lA_void.set(j,i,matrix[i][j])

    self._context["pairs"] = pairs
    return lA_void
