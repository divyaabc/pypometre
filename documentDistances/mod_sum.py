import documentDistances
import numpy
import pprint

class Module_sum(documentDistances.Distance):

    def process(self, matrix):
        minDim = min(len(matrix), len(matrix[0]))
        pairs =  self._context["pairs"]
        score = 0.0
        for i, j in enumerate(pairs):
          if i >= minDim :
            break
          score += matrix[i][j]

        return score / minDim
