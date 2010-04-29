import documentDistancesFilters
import hungarian
import numpy
import pprint
import sys

class Module_hungarian(documentDistancesFilters.DistanceFilter):

    def process(self, matrixOrig):
        minDim = min(len(matrixOrig), len(matrixOrig[0]))
        maxDim = max(len(matrixOrig), len(matrixOrig[0]))

        matrix = squarify(matrixOrig,1.)
        a = numpy.array(matrix)
        pairs = hungarian.lap(a)[0]

        a_void = numpy.resize(a, (minDim,maxDim))
        a_void.fill(1.0)

        for i, j in enumerate(pairs):
            if i >= minDim:
                break;
            a_void[i][j] = matrix[i][j]

#        self._context["matrix"] = a_void
        self._context["pairs"] = pairs
        return a_void


def squarify(_matrix, _val_fill):
    if len(_matrix) > len(_matrix[0]):
      matrix2 = zip(*_matrix)
    else: 
      matrix2 = zip(*_matrix)
      matrix2 = zip(*matrix2)
    len_line = len(matrix2[0])
    diff = len_line - len(matrix2)
    for _ in xrange(diff):
      matrix2.append([_val_fill for _ in xrange(len_line)])
    return matrix2
