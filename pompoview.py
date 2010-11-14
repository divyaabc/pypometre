#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
from functools import partial
from optparse import OptionParser
from pypometre_optparser import opt_parser_pompoview

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

def boris_classifier(matrix, threshold):
    nbColumns = math.sqrt(len(matrix))
    N = (len(matrix)-nbColumns) / 2.0
    ACC = (sum(1.0-x for x in matrix.itervalues() ) / (2.0*N) )
    SG = threshold
    SI = ACC + ((1.0-ACC) * SG)
    steps = [1.0-SI]
    return steps

def print_matrix_as_html(f, names, matrix, nodes, separators, classifier, coloration, option_projection, signature):
    steps = classifier(matrix)
    colors = coloration(0, 1., steps, get_color_html)

    if option_projection :
      total = [0 for _ in xrange(len(nodes))]
      cpt = len(total) - 1

    print >>f, '<table style="collapse:collapse;" cellspacing="0">'
    for i, n in enumerate(nodes):
        print >>f,  '<tr>'
        for j in xrange(len(nodes)):
          if option_projection and (i != j) :
            total[j] += matrix[(i,j)]
          sepTxt = "border-right: 0px solid black; border-bottom: 0px solid black;"
          cls, color = get_color(matrix[(i, j)], steps, colors)
          print >>f, '<td style="font-size:13px; padding:4px;%sbackground-color:%s;">%6.3f</td>'%(sepTxt, color, matrix[(i, j)])
        print >>f, '<td style="font-size : 12px;">%s</td></tr>'%names[n]
    print >>f, "<tr>"

    if option_projection :
      print >>f, "<tr>"
      line_str = ""
      for val in total :
        true_val = float(val) / cpt
        cls, color = get_color(true_val, steps, colors)
        sepTxt = "border: 1px solid black;"
        line_str += '<td style="font-size : 12px; padding:4px;%sbackground-color:%s;">%6.2f</td>'%(sepTxt, color, true_val)
      print >>f, "%s</tr>"%(line_str) 

    for n in nodes:
        print >>f, '<td valign="top" style="font-size:12px; padding:0px;">%s</td> '% "<br/>".join(names[n])
    print >>f, "<td></td></tr></table>"

    print_signature = ""

    for l1 in signature.split(";") :
        l2 = l1.split('|')
        print_signature += "<dl><dt>"+l2[0]+"</dt>"
        for l3 in l2[1:] :
            l4 = l3.split(',')
            print_signature += "<dd><strong>" + l4[0] + "</strong> " + str(l4[1:]) + "</dd>"
        print_signature += "</dl>"

    print >>f, "%s"%(print_signature)

def print_matrix_as_doc(f, names, matrix, nodes, separators, classifier, coloration, option_projection):
  print >>f, "\documentclass[a4paper]{article}"
  print >>f, "\usepackage[utf8]{inputenc}"
  print >>f, "\usepackage[T1]{fontenc}" 
  print >>f, "\usepackage[francais]{babel}"
  print >>f, "\usepackage[counterclockwise]{rotating}"
  print >>f, "\usepackage[table]{xcolor}"
  print >>f, '\\begin{document}'

  print_matrix_as_tex(f, names, matrix, nodes, separators, classifier, option_projection)

  print >>f, "\end{document}"


def print_matrix_as_tex(f, names, matrix, nodes, separators, classifier, coloration, option_projection):
    steps = classifier(matrix)
    colors = coloration(0., 1., steps)
    descript_col = "|r|"
    first_line = "  &"

    for i,val in enumerate(nodes):
      descript_col += 'c'
      first_line += ' \\rotatebox{90}{'+str(names[val])+'} &'
    first_line = '\hline\n' + first_line[:len(first_line)-2] + '\\\\'

    print >>f, '\\begin{tabular}{' + descript_col + '|}'
    print >>f,  first_line

    if option_projection :
      total = []
      cpt=0
      for i,val in enumerate(nodes):
        total.append(0)
        descript_col += 'c'

    print >>f,  '\hline'
    
    for i, n in enumerate(nodes):
        line = "%s & " % (names[n])
        for j in xrange(len(nodes)):
            cls, color = get_color(matrix[(i, j)], steps, colors)
            if(option_projection and i != j) :
              total[j] += matrix[(i,j)]
              cpt += 1
            line += '%s %.2f & ' % (color,matrix[(i,j)])
        line = line[:len(line)-2] + '\\\\' 
        print >>f, "%s\cline{1-1}" % (line)
    print >>f, '\hline'


    if option_projection :
      print >>f, 'total & '
      line_total = ""
      for val in total :
        true_val = float(val) / (cpt-1)
        cls, color = get_color(true_val, steps, colors)
        line_total += '%s %0.2f & ' % (color, float(val) / (cpt-1))
      line_total = line_total[:len(line_total)-2] + '\\\\' 
      print >>f, "%s" % (line_total)
    print >>f, '\hline\end{tabular}'

def print_matrix_as_png(f, names, matrix, nodes, separators, classifier, coloration, option_projection, signature):
  import Image, ImageColor
  zoom = 2
  steps = classifier(matrix)
  colors = coloration(0, 1., steps, get_color_html)
  h = len(nodes) * zoom
  m = [[[] for _ in xrange(h)] for _ in xrange(h)]

  image = Image.new("RGBA", (h, h))
  for i, n in enumerate(nodes):
    for j in xrange(len(nodes)):
      cls, c = get_color(matrix[(i, j)], steps, colors)
      for k1 in range(zoom) :
        for k2 in range(zoom) :
          rgba = ImageColor.getcolor(c, "RGBA")
          image.putpixel((i*zoom+k1, j*zoom+k2), rgba) 
  image.save(f,"png")


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

    if options.fileout == "default" :
      outFile = os.path.splitext(inFile)[0] + "." + options.mode
    elif options.mode == "doc" :
      outFile = os.path.splitext(options.fileout)[0] + ".doc.tex"
    else :
      outFile = os.path.splitext(options.fileout)[0] + "." + options.mode
    f = open(outFile, "w")

    data = eval(file(inFile).read())
    names, input, signature = data["filenames"], data["corpus_scores"], data["signature"]
    matrix = listList_to_matrix(input)

    couples = linkage(matrix, dist_max)
    tree = couples_to_tree(couples)
    sortedNodes, separators = sort_tree(tree, couples, sort_by_diameter(matrix))
    matrix = permute_matrix(matrix, sortedNodes)

########################################
#   OPTION : normalisation -n
########################################
#    normedMatrix = normalize_matrix(sortedMatrix,sortedNodes)
    if options.normalize : matrix = normalize_matrix(matrix,sortedNodes)

########################################
#   OPTION : verbose -q
########################################

########################################
#   OPTION : output mode -m
########################################
    #classifier, coloration = (lambda m: boris_classifier(m, .85)), get_hsl 
    classifier, coloration = (lambda m: matrix_half_entangled_mean(m,options.nb_class)), get_half_hsl
    #classifier, coloration = (lambda m: matrix_entangled_mean(m,options.nb_class)), get_hsl
#    print separators
    if options.mode == "html" :
      printer = print_matrix_as_html
    elif options.mode == "tex" :
      printer = print_matrix_as_tex
    elif options.mode == "doc" :
      printer = print_matrix_as_doc
    elif options.mode == "png" :
      printer = print_matrix_as_png

    printer(f, names, matrix, sortedNodes, separators, classifier, coloration, options.projection, signature)

########################################
#   OPTION : verbose -q
########################################
    if(options.verbose) :
      print " - " + "file://" + os.path.join(os.path.abspath("."), outFile)

import sys, os
parser = opt_parser_pompoview()
(opt_options, opt_args) = parser.parse_args()
if(len(opt_args) > 0) :
  opt_options.filename = opt_args[0]

main(opt_options)
