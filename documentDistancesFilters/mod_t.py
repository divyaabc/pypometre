import documentDistancesFilters
import sys
sys.path.append('..')

from dataStructures import *
import tool_dataStructures as tds
#import tool_numpy as tn

#module threshold
class Module_t(documentDistancesFilters.DistanceFilter):
  def process(self,lMatrix):
#    lMatrix = LinedMatrix(0,0)
#    lMatrix.convertDistMatrix(matrix)
    lMatrix = tds.threshold_linedMatrix(lMatrix,self._context["threshold"])

#    matrix = lMatrix.getMatrix()
#    matrix = tn.matrix2numpy(matrix) 

#    for i,line in enumerate(matrix) :
#      for j,val in enumerate(line) :
#        if val < self._context["threshold"][0] :
#          matrix[i][j]  = 0
#        elif val > self._context["threshold"][1] :
#          matrix[i][j]  = 1

    self._context["matrix"] = lMatrix
    return lMatrix
