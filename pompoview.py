#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
from functools import partial
from optparse import OptionParser
from pypometre_optparser import opt_parser_pompoview

def avg(l): 
  l = list(l)
  return float(sum(l))/len(l)

#def median(matrix):
#    lst = sorted(matrix.values())
#    return lst[len(lst)/2]

def listList_to_matrix(ll):
  matrix = {}
  for i, l in enumerate(ll):
    for j, v in enumerate(l):
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
  result = []
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
  result = []
  while lst:
    inf,sup,n = lst.pop()
    m = matrix_mean_split(matrix, inf, sup)
    result.append(m)
    if n == 1.:
      continue
    lst.append((inf,m,n-1))
    #lst.append((m,sup,n-1))
  result.sort()
  return result


def get_hsl(vmin, vmax, steps, null):
  colors = []
  for s in xrange(len(steps)):
    colors.append(get_color_html(((vmax-vmin)*s)/len(steps) + vmin))
  colors.append(get_color_html(1.0))
  return colors

def get_half_hsl(min, max, steps, color_printer):
  colors = []
  for s in xrange(len(steps)):
    colors.append(color_printer(1./(2**s)))
  colors.append(color_printer(0.0))
  colors.reverse()
  return colors

def get_hsb(min, max, steps):
    colors = []
    for s in xrange(len(steps)):
        colors.append(get_color_tex(((max-min)*s)/len(steps) + min))
    return colors

def get_color_tex(r) :
    return "\cellcolor[hsb]{%0.2f, %0.2f, %0.2f}"%(float(120*r)/360, .7, .9)#int(r*100), 70)

def get_color_html(r):
    return "hsl(%d, %d%%, %d%%)"%(int(120*r), 100, 50)#int(r*100), 70)

def get_color(v, steps, colors):
    for i, (s, c) in enumerate(zip(steps, colors)):
        if v<=s: 
            return i, c
    return i+1, colors[-1]

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

def boris_classifier(matrix, threshold):
    nbColumns = math.sqrt(len(matrix))
    N = (len(matrix)-nbColumns) / 2.0
    ACC = (sum(1.0-x for x in matrix.itervalues() ) / (2.0*N) )
    SG = threshold
    SI = ACC + ((1.0-ACC) * SG)
    steps = [1.0-SI]
    return steps


def plist(f, names, matrix, nodes, classifier, coloration, signature, outFileName, opt):
  steps = classifier(matrix)
  print steps
  1/0
  pass

def phtml(f, names, matrix, nodes, classifier, coloration, signature, outFileName, opt):
    steps = classifier(matrix)
    colors = coloration(0, 1., steps, get_color_html)
    style_td = ['font-size:11px;','padding:2px;']

    if opt.projection :
      total = [0 for _ in xrange(len(nodes))]
      cpt = len(total) - 1.

    print >>f, '<table style="collapse:collapse;" cellspacing="0">'
    for i, n in enumerate(nodes):
        print >>f, '<tr>'
        for j in xrange(len(nodes)):
          if opt.projection and (i != j) :
            total[j] += matrix[(i,j)] / cpt
          score = matrix[(i,j)]
          _, color = get_color(score, steps, colors)
          styles = style_td + ['background-color:%s;'%(color)]
          print >>f, '<td style="%s">%6.2f</td>'%("".join(styles), score)
        print >>f, '<td style="%s">%s</td></tr>'%(style_td[0],names[n])
    print >>f, "<tr>"

    if opt.projection :
      print >>f, "<tr>"
      line_str = ""
      for true_val in total :
        cls, color = get_color(true_val, steps, colors)
        styles = style_td + ['background-color:%s;'%(color),'border: 1px solid black;']
        line_str += '<td style="%s;">%.2f</td>'%("".join(styles), true_val)
      print >>f, "%s</tr>"%(line_str) 

    for n in nodes:
      print >>f, '<td valign="top" style="%s">%s</td> '%(style_td[0],"<br/>".join(names[n]))
    print >>f, "<td/></tr></table>"

    try :
      signature = eval(signature)
      print_signature = ""
      for k,v in signature.iteritems() :
        print_signature += '<li><strong>%s</strong> : %s</li>'%(str(k),str(v))
    except :
      print_signature = '<p>%s</p>'%(signature)

    print >>f, "%s"%(print_signature)

def pdoc(f, names, matrix, nodes, classifier, coloration, signature, outFileName, opt):
  print >>f, "\documentclass[a4paper]{article}"
  print >>f, "\usepackage[utf8]{inputenc}"
  print >>f, "\usepackage[T1]{fontenc}" 
  print >>f, "\usepackage[francais]{babel}"
  print >>f, "\usepackage[counterclockwise]{rotating}"
  print >>f, "\usepackage[table]{xcolor}"
  print >>f, '\\begin{document}'

  ptex(f, names, matrix, nodes, classifier, coloration, signature, outFileName, opt)

  print >>f, "\end{document}"


def ptex(f, names, matrix, nodes, classifier, coloration, signature, outFileName, opt):
    steps = classifier(matrix)
    colors = coloration(0., 1., steps, get_color_tex)
    descript_col = "|r|"
    first_line = "  &"

    for i,val in enumerate(nodes):
      descript_col += 'c'
      v = names[val].split('/')[-1]
      first_line += '%s & '%(v)
      #first_line += ' \\rotatebox{90}{'+str(names[val])+'} &'
    first_line = '\hline\n' + first_line[:len(first_line)-2] + '\\\\'

    print >>f, '\\begin{tabular}{' + descript_col + '|}'
    print >>f,  first_line

    if opt.projection :
      total = []
      cpt=0
      for i,val in enumerate(nodes):
        total.append(0)
        descript_col += 'c'

    print >>f,  '\hline'
    
    for i, n in enumerate(nodes):
        v = names[n].split('/')[-1]
        line = "%s & " % (v)
        #line = "%s & " % (names[n])
        for j in xrange(len(nodes)):
            cls, color = get_color(matrix[(i, j)], steps, colors)
            if(opt.projection and i != j) :
              total[j] += matrix[(i,j)]
              cpt += 1
            line += '%s %.2f & ' % (color,matrix[(i,j)])
        line = line[:len(line)-2] + '\\\\' 
        print >>f, "%s\cline{1-1}" % (line)
    print >>f, '\hline'


    if opt.projection :
      print >>f, 'total & '
      line_total = ""
      for val in total :
        true_val = float(val) / (cpt-1)
        cls, color = get_color(true_val, steps, colors)
        line_total += '%s %0.2f & ' % (color, float(val) / (cpt-1))
      line_total = line_total[:len(line_total)-2] + '\\\\' 
      print >>f, "%s" % (line_total)
    print >>f, '\hline\end{tabular}'

def ppng(f, names, matrix, nodes, classifier, coloration, signature, outFileName, opt):
  import Image, ImageColor
  zoom = 2
  steps = classifier(matrix)
  colors = coloration(0, 1., steps, get_color_html)
  l = len(nodes)
  h = l * zoom

  image = Image.new("RGBA", (h, h))
  for i, n in enumerate(nodes):
    for j in xrange(l):
      cls, c = get_color(matrix[(i, j)], steps, colors)
      for k1 in xrange(zoom) :
        for k2 in xrange(zoom) :
          rgba = ImageColor.getcolor(c, "RGBA")
          image.putpixel((i*zoom+k1, j*zoom+k2), rgba) 
  image.save(f,"png")

def pjson(f, names, matrix, nodes, classifier, coloration, signature, outFileName, opt):
  pngName = getFileName(outFileName, "png")
  f2 = open(pngName, 'w')
  ppng(f2, names, matrix, nodes, classifier, coloration, signature, pngName, opt)
  
  steps = classifier(matrix)
  colors = coloration(0, 1., steps, get_color_html)
    
  fileNames = []
  for val in nodes:
      fileNames.append(names[val])
     
  m = []
  col = []
  for i, n in enumerate(nodes):
    l = []
    col_l = []
    for j in xrange(len(nodes)):
      cls, c = get_color(matrix[(i, j)], steps, colors)
      l.append(matrix[(i, j)])
      col_l.append(c)
    m.append(l)
    col.append(col_l)
  f.write("{'fileNames':%s, 'matrix': %s, 'colors': %s}"%(fileNames, m, col));


def init_groupes(matrix):
  groupes = [[i] for i, j in matrix if j == 0]
  groupes.sort()
  return groupes


def iteration_linkage2(matrix, groupes, dist):
  min_dist = min((dist(matrix, g1, g2), i1, i2) 
                      for i1, g1 in enumerate(groupes)
                      for i2, g2 in enumerate(groupes)
                      if i1 != i2
                )
  return min_dist

def iteration_linkage(matrix, groupes, dist) :
  res = []
  for i1, g1 in enumerate(groupes) :
    for i2, g2 in enumerate(groupes) :
      if i2 > i1:
        d = dist(matrix,g1,g2)
        res.append((d, i1, i2))
 #       res.append((d, i2, i1))
  return min(res)

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

def dmin(matrix, g1, g2):
  return min(matrix[(i, j)] for i in g1 for j in g2)
            
def dmax(matrix, g1, g2):
  return max(matrix[(i, j)] for i in g1 for j in g2)

def davg(matrix, g1, g2):
  return avg(matrix[(i, j)] for i in g1 for j in g2)

def getFileName(inFile, mode, outFile='default') :
  if outFile == "default" :
    return '%s.%s'%(os.path.splitext(inFile)[0],mode)
  return '%s.%s'%(os.path.splitext(outFile)[0],mode)

def main(options):
    #raise SystemExit(0)
################################
#   OPTION : filename -f
################################
    inFile = options.filename

################################
#   OPTION : fileout -o
#   OPTION : mode -m
################################
    outFile = getFileName(inFile, options.mode, options.fileout)

    f = open(outFile, "w")

    data = eval(file(inFile).read())
    names, signature = data["filenames"], data["signature"]
    matrix = listList_to_matrix(data["corpus_scores"])

################################
#   OPTION : dist -d
################################
    fname = 'd%s'%(options.dist)
    distance_cluster = eval(fname)

    couples = linkage(matrix, distance_cluster)
    tree = couples_to_tree(couples)
    sortedNodes, separators = sort_tree(tree, couples, sort_by_diameter(matrix))
    matrix = permute_matrix(matrix, sortedNodes)

###############################
#   OPTION : normalisation -n
###############################
    if options.normalize : 
      matrix = normalize_matrix(matrix,sortedNodes)

###############################
#   OPTION : output mode -m
###############################
    #classifier, coloration = (lambda m: boris_classifier(m, .85)), get_hsl 
    #classifier, coloration = (lambda m: matrix_half_entangled_mean(m,options.nb_class)), get_half_hsl
    classifier, coloration = (lambda m: matrix_entangled_mean(m,options.nb_class)), get_hsl

    fname = "p%s"%(options.mode)
    printer = eval(fname)
    printer(f, names, matrix, sortedNodes, classifier, coloration, signature, outFile, options)

################################
#   OPTION : verbose -q
################################
    if(options.verbose) :
      print " - " + "file://" + os.path.join(os.path.abspath("."), outFile)

import sys, os
parser = opt_parser_pompoview()
(opt_options, opt_args) = parser.parse_args()
if(len(opt_args) > 0) :
  opt_options.filename = opt_args[0]

main(opt_options)
