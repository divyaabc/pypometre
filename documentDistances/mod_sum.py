import documentDistances
import sys
sys.path.append('..')

from dataStructures import *

class Module_sum(documentDistances.Distance):
  def process(self, lmatrix):
    pairs =  self._context['pairs']
    score = 0.
    for i in xrange(lmatrix._min) :
      score += lmatrix.get(pairs[i],i)
    return score / lmatrix._min

