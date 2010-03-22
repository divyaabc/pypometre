import documentDistances
import hungarian
import numpy

class Module_hungarian(documentDistances.Distance):

    def process(self, matrixOrig):
        minDimension = min(len(matrixOrig), len(matrixOrig[0]))
        matrix = squarize(matrixOrig)
        a = numpy.array(matrix)
        pairs = hungarian.lap(a)[0]
        score = 0.0
        for i, j in enumerate(pairs):
            if i >= minDimension:
                break;
            score += matrix[i][j]
        result = score / minDimension
        print result
        return result

def squarize(matrix):
    if len(matrix) > len(matrix[0]):
        matrix2 = zip(*matrix)
    else: 
        matrix2 = matrix
    diff = len(matrix2[0]) - len(matrix2)
    for _ in xrange(diff):
        matrix2.append([1.0 for _ in xrange(len(matrix2[0]))])
    return matrix2

