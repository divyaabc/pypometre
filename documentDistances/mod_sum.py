import documentDistances
import sys
sys.path.append('..')

from dataStructures import *

class Module_sum(documentDistances.Distance):
  def process(self, lmatrix):
    minDim = min(lmatrix._width, lmatrix._height)
    pairs =  self._context['pairs']
    score = 0.
    for i in xrange(minDim) :
      score += lmatrix.get(pairs[i],i)
    return score / minDim

