import documentDistances
import sys
sys.path.append('..')

from dataStructures import *

class Module_sum(documentDistances.Distance):
  def process(self, lmatrix):
    score = 0.
    for i in xrange(lmatrix._min) :
      score += lmatrix.get(self._context['pairs'][i],i)
    return score / lmatrix._min

