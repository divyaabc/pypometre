import documentDistances
import hungarian
import numpy
import pprint

class Module_hungarian(documentDistances.Distance):

    def process(self, matrixOrig):
        minDimension = min(len(matrixOrig), len(matrixOrig[0]))
      
        matrix = squarize(matrixOrig)
        a = numpy.array(matrix)
#        a.astype(None)
#        print a.dtype.name
        pprint.pprint(a)
        pairs = hungarian.lap(a)[0]
#        print "2"
        score = 0.0
        for i, j in enumerate(pairs):
            if i >= minDimension:
                break;
            score += matrix[i][j]
#        print "3"
        result = score / minDimension
        print result
        return result

def squarize(matrix):
    if len(matrix) > len(matrix[0]):
        matrix2 = zip(*matrix)
    else: 
        matrix2 = matrix
    len_line = len(matrix2[0])
    diff = len_line - len(matrix2)
    for _ in xrange(diff):
        matrix2.append([1.0 for _ in xrange(len_line)])
    matrix2 = modMatrix(matrix2)
    return matrix2

def modMatrix(_matrix) :
  matrix2 = []
  for line in _matrix :
    matrix2.append(list(line))
  return matrix2
    
