#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import Image
import scipy.signal

def squarify(matrix, val_fill) :
  if len(matrix) > len(matrix[0]):
    matrix2 = zip(*matrix)
  else:
    matrix2 = list(matrix)
  len_line = len(matrix2[0])
  diff = len_line - len(matrix2)
  for _ in xrange(diff):
    matrix2.append([val_fill for _ in xrange(len_line)])
  return matrix2

def numpy_resize(matrix, couple_dim) :
  return numpy.resize(matrix, couple_dim)

def matrix2numpy(matrix) :
  return numpy.array(matrix,"float32")

def distMatrix2numpy(distMatrix) :
  return numpy.array(distMatrix.data,"float32")

def matrix2image(matrix, path) :
  a_print = (1. - matrix) * 255
  a_print = a_print.astype(numpy.uint8)
  Image.fromarray(a_print).save(path)

def matrix2matrix_convolved(matrix,filt) :
  return scipy.signal.convolve2d(matrix, filt, mode="same", fillvalue=1.)

