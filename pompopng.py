#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from functools import partial
from optparse import OptionParser
import Image
import ImageColor
import numpy
import colorsys

def avg(l): 
    l = list(l)
    return float(sum(l))/len(l)

def median(matrix):
    lst = sorted(matrix.values())
    return lst[len(lst)/2]

def listList_to_matrix(lstLst):
    matrix = {}
    for i, lst in enumerate(lstLst):
        for j, v in enumerate(lst):
            matrix[(i, j)] = v
    return matrix

def matrix_mean(matrix):
    return sum(matrix.values()) / len(matrix)

def matrix_mean_split(matrix, inf, sup):
    return matrix_mean(dict((k, v) for k, v in matrix.iteritems() if inf <= v <=sup))

def matrix_entangled_mean(matrix, n):
    val_max = max(matrix.values())
    val_min = min(matrix.values())
    lst = [(val_min,val_max,n)]
    result = [val_max+1]
    while lst:
        inf,sup,n = lst.pop()
        m = matrix_mean_split(matrix, inf, sup)
        result.append(m)
        if n == 1:
            continue
        lst.append((inf,m,n-1))
        lst.append((m,sup,n-1))
    result.sort()
    return result

def matrix_half_entangled_mean(matrix, n):
    val_max = max(matrix.values())
    val_min = min(matrix.values())
    lst = [(val_min,val_max,n)]
    result = [val_max+1]
    while lst:
        inf,sup,n = lst.pop()
        m = matrix_mean_split(matrix, inf, sup)
        result.append(m)
        if n == 1:
            continue
        lst.append((inf,m,n-1))
        #lst.append((m,sup,n-1))
    result.sort()
    return result


def get_hsl(min, max, steps):
    colors = []
    for s in xrange(len(steps)):
        colors.append(get_color_html(((max-min)*s)/len(steps) + min))
    return colors


def get_half_hsl(min, max, steps):
    colors = []
    for s in xrange(len(steps)):
      colors.append(get_color_html(1./(2**s)))
    colors.reverse()
    return colors

def get_hsb(min, max, steps):
    colors = []
    for s in xrange(len(steps)):
        colors.append(get_color_tex(((max-min)*s)/len(steps) + min))
    return colors

def get_color_tex(r) :
    return "\cellcolor[hsb]{%0.2f, %0.2f, %0.2f}"%(float(120*r)/360, .7, .9)#int(r*100), 70)

def get_color_html(r) :
    return "hsl(%d, %d%%, %d%%)"%(int(120*r), 100, 50)#int(r*100), 70)

def get_color_rgb(v) :
  color = ImageColor.getrgb("hsl(%d,%d%%,%d%%)" % (int(120*v), 100, 50))
  return color

def get_half_grey(min, max, steps) :
    colors = []
    for s in xrange(len(steps)):
      colors.append(get_color_grey(1./(2**s)))
    colors.reverse()
    return colors

def get_half_rgb(min, max, steps) :
    colors = []
    for s in xrange(len(steps)):
      colors.append(get_color_rgb(1./(2**s)))
    colors.reverse()
    return colors

def get_color(v, steps, colors):
    for i, (s, c) in enumerate(zip(steps, colors)):
        if v<s: 
            return i, c
    return 0, "white"

def normalize_matrix(matrix, nodes) :
  mx = 0
  mn = 1
  matrix_normalized = {}
  for i,n in enumerate(nodes) :
    for j in xrange(len(nodes)):
      mx = max(mx,matrix[(i,j)])
      if (i != j) :
        mn = min(mn,matrix[(i,j)])

  inter = mx - mn

  for i,n in enumerate(nodes) :
    for j in xrange(len(nodes)):
      val = matrix[(i,j)]
      if val == 0 : 
        matrix_normalized[(i,j)] = val
      else :
        matrix_normalized[(i,j)] = (val - mn) / inter

  return matrix_normalized

def init_groupes(matrix):
    groupes = [[i] for i, j in matrix if j == 0]
    groupes.sort()
    return groupes

def dist_min(matrix, g1, g2):
    return min(matrix[(i, j)] for i in g1 for j in g2)
            
def dist_max(matrix, g1, g2):
    return max(matrix[(i, j)] for i in g1 for j in g2)

def dist_avg(matrix, g1, g2):
    return avg(matrix[(i, j)] for i in g1 for j in g2)

def iteration_linkage(matrix, groupes, dist):
    min_dist = min((dist(matrix, g1, g2), i1, i2) 
                        for i1, g1 in enumerate(groupes)
                        for i2, g2 in enumerate(groupes)
                        if i1 != i2
                  )
    return min_dist

def linkage(matrix, dist):
    groupes = init_groupes(matrix)
    couples = []
     
    while len(groupes) > 1:
        d, i1, i2 = iteration_linkage(matrix, groupes, dist)
        g = sorted(groupes[i1] + groupes[i2])
        couples.append((d, groupes[i1], groupes[i2], g))
        groupes[i1] = g 
        del(groupes[i2])
        groupes.sort()
    return couples

def get_height(tree, node):
    if len(node) == 1: 
        return 1
    content, root = tree
    return max(get_height(tree, n) for n in content[node]) + 1

def sort_by_height(tree):
    def _(lstNodes):
        return sorted(lstNodes, key=partial(get_height, tree)) 
    return _

def sort_by_diameter(matrix):
    def _(lstNodes):
        return sorted(lstNodes, key=partial(tree_diameter, matrix), reverse=True)
    return _

def tree_diameter(matrix, node):
    if len(node) == 1:
        return 2
    return max(matrix[(i, j)] for i in node for j in node if i != j)

def couples_to_tree(couples):
    children = {}
    for dist, i1, i2, total in couples:
        children[tuple(total)] = (tuple(i1), tuple(i2))
    return (children, tuple(couples[-1][-1]))

def sort_tree(tree, couples, sort_fct): 
    children, root = tree
    maxHeight = 0
    todo = [(root, 0, 0)]
    separators = [0]*len(root)
    result = []
    distNode = dict((tuple(g), d) for d, _, _, g in couples)
    while todo:
        node, height, pos = todo.pop()
        if children.get(node) is not None:
            sorted_children = sort_fct(children[node])
            for i, child in enumerate(sorted_children):
                todo.append((child, height, pos))
                pos += len(child)
                if i + 1 != len(sorted_children):
                    separators[pos] = distNode[node]
        else:
            result.append(node[0])
            #print "--- "*height,  node[0]
    return result, list(reversed(separators))

def permute_matrix(matrix, lstNodes):
    m = {}
    for i1, i2 in enumerate(lstNodes):
        for j1, j2 in enumerate(lstNodes):
            m[(i1, j1)] = matrix[(i2, j2)]
    return m

def filter_matrix(matrix, line):
    l = max(i for (i, j) in matrix)+1
    for i in xrange(l):
        for j in xrange(l):
            if (line == i) and (line == j):
                matrix[(i, j)] = 0.0
            elif (line == i) or (line == j):
                matrix[(i, j)] = 0.9999999

def print_matrix_as_png(names, matrix, nodes, nbCls,outFile):
    zoom = 2
    steps = matrix_half_entangled_mean(matrix,nbCls)
    colors = get_half_rgb(0, 1., steps)
    h = len(nodes) * zoom
    m = numpy.zeros((h,h,4),numpy.uint8)

    for i, n in enumerate(nodes):
        for j in xrange(len(nodes)):
          cls, c = get_color(matrix[(i, j)], steps, colors)
          for k1 in range(zoom) :
            for k2 in range(zoom) :
              m[(i*zoom)+k1][(j*zoom)+k2] = [c[0],c[1],c[2],1000]
    pilImage = Image.fromarray(m, 'RGBA')
    pilImage.save(outFile,"png")

def main(options):
    #raise SystemExit(0)
########################################
#   OPTION : filename -f
########################################
    inFile = options.filename

########################################
#   OPTION : fileout -o
#   OPTION : mode -m
########################################

    outFile = os.path.splitext(inFile)[0] + ".png"

    if(options.verbose) :
      print " - read file"
    data = eval(file(inFile).read())
    names, input, signature = data["filenames"], data["corpus_scores"], data["signature"]
    matrix = listList_to_matrix(input)

    if(options.verbose) :
      print " - sort document values"

    couples = linkage(matrix, dist_max)
    tree = couples_to_tree(couples)
    sortedNodes, separators = sort_tree(tree, couples, sort_by_diameter(matrix))
    matrix = permute_matrix(matrix, sortedNodes)

########################################
#   OPTION : normalisation -n
########################################
#    normedMatrix = normalize_matrix(sortedMatrix,sortedNodes)
    
    if options.normalize :
      if(options.verbose) :
        print " - normalize each document score"
      matrix = normalize_matrix(matrix,sortedNodes)

########################################
#   OPTION : verbose -q
########################################
    if(options.verbose) :
      print " - draw matrix"

########################################
#   OPTION : output mode -m
########################################
#    print separators
#    print_matrix_as_html(f, names, matrix, sortedNodes, separators, options.nb_class, options.projection, signature)
    print_matrix_as_png(names, matrix, sortedNodes, options.nb_class,outFile)

########################################
#   OPTION : verbose -q
########################################
    if(options.verbose) :
      print " - " + "file://" + os.path.join(os.path.abspath("."), outFile)

import sys, os
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", default = "out.js",
                   help="Write report from FILE", metavar="FILE")

parser.add_option("-o", "--output_file", dest="fileout", default = "default",
                   help="Write report to FILEOUT (default)", metavar="FILEOUT")

parser.add_option("-q", "--quiet",
                   action="store_false", dest="verbose", default=True,
                   help="don't print status messages to stdout")

parser.add_option("-n", "--normalize",
                   action="store_true", dest="normalize", default=False,
                   help="Normalize each values of the matrix between [minVal,maxVal] (default = False)")

parser.add_option("-p", "--projection",
                   action="store_true", dest="projection", default=False,
                   help="Project the values of the matrix on the x-axis : (default = False)")

parser.add_option("-c", "--nb_class", dest="nb_class", default = "4", type = "int",
                   help="Use a coloration in NBCLASS classes (default = 4)", metavar="NBCLASS")

(opt_options, opt_args) = parser.parse_args()
if(len(opt_args) > 0) :
  opt_options.filename = opt_args[0]

main(opt_options)
