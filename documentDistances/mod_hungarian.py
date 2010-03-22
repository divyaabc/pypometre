import documentDistances
import hungarian
import numpy

class Module_hungarian(documentDistances.Distance):

    def process(self, matrix):
        matrix = squarize(matrix)
        a = numpy.array(matrix)
        pairs = hungarian.lap(a)[0]
        score = 0.0
        for i, j in enumerate(pairs):
            score += matrix[i][j]
        minDimension = min(len(matrix), len(matrix[0]))
        return score / minDimension

def squarize(matrix):
    if len(matrix) > len(matrix[0]):
        matrix2 = zip(*matrix)
    else: 
        matrix2 = matrix
    diff = len(matrix2[0]) - len(matrix2)
    for _ in xrange(diff):
        matrix2.append([0 for _ in xrange(len(matrix2[0]))])
    return matrix2

