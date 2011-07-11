import documentDistancesFilters
import sys
sys.path.append('..')

from dataStructures import *
import tool_dataStructures as tds
#import tool_numpy as tn

#module threshold
class Module_t(documentDistancesFilters.DistanceFilter):
  def process(self,lMatrix):
    lMatrix = tds.threshold_linedMatrix(lMatrix,self._context["threshold"])

    self._context["matrix"] = lMatrix
    return lMatrix
