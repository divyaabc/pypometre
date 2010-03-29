import documentDistances
import numpy
import pprint

class Module_sum(documentDistances.Distance):

    def process(self, matrix):
        a_convolved = matrix
        minDim = min(len(a_convolved), len(a_convolved[0]))
        pairs =  self._context["pairs"]
        score = 0.0
        
        for i, j in enumerate(pairs):
          if i >= minDim :
            break
          score += a_convolved[i][j]

        result = score / minDim

        return result
