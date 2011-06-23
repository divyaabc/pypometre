#!/usr/bin/python
# -*- coding: utf-8 -*-


#import os, sys
#import pprint
from dataStructures import *

def lFiltre2list_i(lFiltre, width_tgt) :
  matrix = lFiltre.getMatrix()
  mid = lFiltre._width / 2
  l = []
  for y in xrange(lFiltre._height) :
    mod = (y - mid) * width_tgt
    for x in xrange(lFiltre._width) :
      val = matrix[y][x] 
      if val == 0. :
        continue
      ni = mod + x - mid
      l.append((ni,val))
  return l


def convolve_linedMatrix(lMatrix, lFiltre, method, fill) :
  list_coeff = lFiltre2list_i(lFiltre, lMatrix._width) 
  ndata = array('f',[0.0 for _ in xrange(lMatrix._len)])
  for i in xrange(lMatrix._len) :
    sum_val, sum_coeff = 0., 0.
    for ci,coeff in list_coeff :
      ni = i + ci
      if(0 <= ni < lMatrix._len) :
        sum_coeff += coeff
        sum_val += lMatrix.data[ni] * coeff
    ndata[i] = sum_val / sum_coeff
  lMatrix.data = ndata
  return lMatrix

def lFiltre2list_xy(lFiltre) :
  l = []
  s, nb = 0., 0
  mid = lFiltre._width / 2
  for i in xrange(lFiltre._len) :
    val = lFiltre.data[i]
    if(val != 0) :
      xy = lFiltre.i2xy(i)
      l.append(((xy[0]-mid,xy[1]-mid), val))
      s += val
      nb += 1
  return nb,s,l

def convolve_linedMatrix2(lMatrix, lFiltre, method, fill) :
  nb_cases,total_coeff,list_coeff = lFiltre2list_xy(lFiltre) 
  ndata = array('f',[0.0 for _ in xrange(lMatrix._len)])
#  print lMatrix._len, lMatrix._width, lMatrix._height
  for i in xrange(lMatrix._len) :
    ox,oy = lMatrix.i2xy(i)
    sum_val, sum_coeff = 0., 0.
    for (x,y),coeff in list_coeff :
      nx = ox + x
      ny = oy + y
      if(0 <= nx < lMatrix._width and 0 <= ny < lMatrix._height) :
        sum_coeff += coeff
        sum_val += lMatrix.get(nx,ny) * coeff
    ndata[i] = sum_val / sum_coeff
  lMatrix.data = ndata
  return lMatrix


def threshold_linedMatrix(lMatrix, thresh) :
  for i in xrange(lMatrix._len) :
    if lMatrix.data[i]< thresh[0] :
      lMatrix.data[i] = 0.
    elif lMatrix.data[i] > thresh[1] :
      lMatrix.data[i] = 1.
  return lMatrix

