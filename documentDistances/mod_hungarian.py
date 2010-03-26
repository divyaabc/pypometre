import documentDistances
import hungarian
import numpy
import pprint
import scipy.signal
import sys
import Image


def matrix2image(_matrix,_path):
  a_print = _matrix.copy()
  a_print = (1. - a_print) * 255
  a_print = a_print.astype(numpy.uint8)
  Image.fromarray(a_print).save(_path)

class Module_hungarian(documentDistances.Distance):

    def process(self, matrixOrig):
        minDim = min(len(matrixOrig), len(matrixOrig[0]))
        maxDim = max(len(matrixOrig), len(matrixOrig[0]))
      
        matrix = squarize(matrixOrig)
        a = numpy.array(matrix)

#        path  = "./log/documentDistances/"
#        path += "./distance_" + str(minDim) + "_" + str(maxDim) + ".png"
#        matrix2image(a,path)

        pairs = hungarian.lap(a)[0]
        a_void = numpy.resize(a, (minDim,maxDim))
        a_void.fill(1)

        for i, j in enumerate(pairs):
            if i >= minDim:
                break;
            a_void[i][j] = matrix[i][j]

        filter = numpy.array(self._context["convolve"])

        a_convolved = scipy.signal.convolve2d(a_void, filter, mode="same")
#        path  = "./log/documentDistances/"
#        path += "convolved_" + str(minDim) + "_" + str(maxDim) + ".png"
#        matrix2image(a_convolved,path)

        a_seuil = a_convolved.copy()
        a_seuil.fill(1)

        score = 0.0
        for i, j in enumerate(pairs):
          if i >= minDim:
            break;
          if a_convolved[i][j] < self._context["threshold"][0] :
            a_convolved[i][j] = 0
          elif a_convolved[i][j] > self._context["threshold"][1] :
            a_convolved[i][j] = 1
          score += a_convolved[i][j]
          a_seuil[i][j] = a_convolved[i][j]

#        path  = "./log/documentDistances/"
#        path += "seuil_" + str(minDim) + "_" + str(maxDim) + ".png"
#        matrix2image(a_seuil,path)

        result = score / minDim

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
      matrix2.append([1 for _ in xrange(len_line)])
#     matrix2.append([float(sys.maxint) for _ in xrange(len_line)])
    matrix2 = modMatrix(matrix2)
    return matrix2

def modMatrix(_matrix) :
  matrix2 = []
  for line in _matrix :
    matrix2.append(list(line))
  return matrix2
    
