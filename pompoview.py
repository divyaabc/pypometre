#!/usr/bin/python
import math
from functools import partial

def avg(l): 
    l = list(l)
    return float(sum(l))/len(l)

def median(matrix):
    lst = sorted(matrix.values())
    return lst[len(lst)/2]

def get_pts():
    pts = [
      (5,3),
      (4,5),
      (6,1),
      (7,3),
      (8,2),
      (10,10),
      (9,9),
      (6,5),
      (3,10),
    ]
    return pts

def print_pts(pts):
    print pts
    l = int(max(max(x, y) for x, y in pts))
    m = int(min(min(x, y) for x, y in pts)) 
    if l-m > 100:
        print "ERROR: l-m=%d is too much"%(l-m)
        return 
    r = ""
    for i in xrange(m-1, l+1):
        for j in xrange(m-1, l+1):
            for n, (x, y) in enumerate(pts):
                if ((i, j) == (int(x)+m, int(y)+m)):
                    r += "%2d"%n
                    break 
            else:
                r += " -"
        r += "\n"
    print r

def get_matrix(pts):
    matrix = {}
    for i, (xi, yi) in enumerate(pts):
        for j, (xj, yj) in enumerate(pts):
            matrix[(i, j)] = math.hypot(xj-xi, yj-yi) / math.hypot(10, 10) 
    return matrix  

def listList_to_matrix(lstLst):
    matrix = {}
    for i, lst in enumerate(lstLst):
        for j, v in enumerate(lst):
            matrix[(i, j)] = v
    return matrix

def print_matrix(matrix):
    l = max(i for (i, j) in matrix)
    print " "*6, 
    for i in xrange(l):
        print "%5d "%i,
    print
    for i in xrange(l):
        print "%2d : "%i,
        for j in xrange(l):
            print "%6.2f"%matrix[(i, j)],
        print

def print_matrix_with_titles(matrix, nodes):
    print " "*6, 
    for n in nodes:
        print "%5d "%n,
    print
    for i, n in enumerate(nodes):
        print "%2d : "%n,
        for j in xrange(len(nodes)):
            print "%6.2f"%matrix[(i, j)],
        print

def matrix_mean(matrix):
    return sum(matrix.values()) / len(matrix)

def matrix_mean_split(matrix, inf, sup):
    return matrix_mean(dict((k, v) for k, v in matrix.iteritems() if inf <= v <=sup))

def matrix_entangled_mean(matrix, n):
    val_max = max(matrix.values())
    val_min = min(matrix.values())
    lst = [(val_min,val_max,n)]
    result = [2]
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

def matrix_median(matrix):
    return list(sorted(matrix.values()))[len(matrix)/2]

def get_hsl(min, max, steps):
    colors = []
    for s in xrange(len(steps)):
        colors.append(get_color_html(((max-min)*s)/len(steps) + min))
    return colors

def get_hsb(min, max, steps):
    colors = []
    for s in xrange(len(steps)):
        colors.append(get_color_tex(((max-min)*s)/len(steps) + min))
    return colors

def get_color_tex(r) :
    return "\cellcolor[hsb]{%0.2f, %0.2f, %0.2f}"%(float(120*r)/360, .7, .9)#int(r*100), 70)

def get_color_html(r):
    #return "hsl(%d, %d%%, %d%%)"%(int(120*r), 100-int(r*5)*10, 50-int(r*5)*10)#int(r*100), 70)
    return "hsl(%d, %d%%, %d%%)"%(int(120*r), 100, 50)#int(r*100), 70)
    #return "#%02x%02x%02x"%(int(r*255), int(g*255), int(b*255))

def get_color(v, steps, colors):
    for i, (s, c) in enumerate(zip(steps, colors)):
        if v<s: 
            return i, c
    return 0, "white"

def print_matrix_as_html(f, names, matrix, nodes, separators, nbCls):
    #names = [os.path.split(n)[1] for n in names]
    steps = matrix_entangled_mean(matrix,nbCls)
    colors = get_hsl(0., 1., steps)
    print >>f, '<table style="collapse:collapse;" cellspacing="0">'
    for i, n in enumerate(nodes):
        print >>f,  '<tr>'
        for j in xrange(len(nodes)):
            sepCol = 0#(int(separators[j]*4)) 
            sepRow = 0#(int(separators[i]*4)) 
            sepTxt = "border-right: %dpx solid black;"%sepCol
            sepTxt+= "border-bottom: %dpx solid black;"%sepRow
            cls, color = get_color(matrix[(i, j)], steps, colors)
            print >>f, '<td style="padding:4px;%sbackground-color:%s;">%6.2f</td>'%(sepTxt, color, matrix[(i, j)])
        print >>f, '<td>%s</td>'%names[n]
        print >>f, "</tr>"
    print >>f, "<tr>"
    for n in nodes:
        print >>f, '<td valign="top" style="padding:0px;">%s</td> '% "<br/>".join(names[n])
    print >>f, "<td></td></tr>"
    print >>f, "</table>"

def print_matrix_as_tex(f, names, matrix, nodes, separators, nbCls):
    names = [os.path.split(n)[1] for n in names]
    steps = matrix_entangled_mean(matrix,nbCls)
    colors = get_hsb(0., 1., steps)
    descript_col = "|r|"
    first_line = "  &"
    for i,val in enumerate(nodes):
      descript_col += 'c'
      first_line += ' '+str(names[val])+' &'
    first_line = '\hline\n' + first_line[:len(first_line)-2] + '\\\\'

    print >>f, '\\begin{tabular}{' + descript_col + '|}'
    print >>f,  first_line
    print >>f,  '\hline'
    
    for i, n in enumerate(nodes):
        line = "%s & " % (names[n])
        for j in xrange(len(nodes)):
            cls, color = get_color(matrix[(i, j)], steps, colors)
            line += '%s %.2f & ' % (color,matrix[(i,j)])
        line = line[:len(line)-2] + '\\\\' 
        print >>f, "%s" % (line)
        print >>f, '\cline{1-1}'
    print >>f, '\hline'
    print >>f, '\end{tabular}'

def print_matrix_as_tex2(f, names, matrix, nodes, separators, nbCls):
    names = [os.path.split(n)[1] for n in names]
    steps = matrix_entangled_mean(matrix,nbCls)
    colors = get_hsb(0., 1., steps)
    descript_col = "|r|"
    first_line = "  &"
    total = []
    cpt=0
    for i,val in enumerate(nodes):
      total.append(0)
      descript_col += 'c'
      first_line += ' '+str(names[val])+' &'
#      first_line += ' \\rotatebox{45}{'+str(names[val])+'} &'
    first_line = '\hline\n' + first_line[:len(first_line)-2] + '\\\\'

    print >>f, '\\begin{tabular}{' + descript_col + '|}'
    print >>f,  first_line
    print >>f,  '\hline'
    
    for i, n in enumerate(nodes):
        cpt += 1
        line = "%s & " % (names[n])
        for j in xrange(len(nodes)):
            cls, color = get_color(matrix[(i, j)], steps, colors)
            if(i != j) :
              total[j] += matrix[(i,j)]
            line += '%s %.2f & ' % (color,matrix[(i,j)])
        line = line[:len(line)-2] + '\\\\' 
        print >>f, "%s" % (line)
        print >>f, '\cline{1-1}'
    print >>f, '\hline'
    print >>f, 'total & '

    line_total = ""
    for val in total :
      true_val = float(val) / (cpt-1)
      cls, color = get_color(true_val, steps, colors)
      line_total += '%s %0.2f & ' % (color, float(val) / (cpt-1))
    line_total = line_total[:len(line_total)-2] + '\\\\' 
    print >>f, "%s" % (line_total)
    print >>f, '\hline'

    print >>f, '\end{tabular}'


def matrix_get_line(matrix, line): 
    return dict((k, v) for (k, v) in matrix.iteritems() if k[0] == line)

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

def energie_groupe(g, matrix):
    e = 0.0
    for i in g:
        for j in g:
            if i > j:
                continue
            e += matrix[(i, j)]
    conn = (len(g)*(len(g)-1)) / 2.0
    if conn < 0.001:
        return 0
    e /= conn
    return e 

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

def takeByTwo(l):
    it = iter(l)
    n = it.next()
    for m in it:
        yield n, m
        n = m

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

def print_couples(couples, matrix):
    for dist, g1, g2, total in couples:
        e1 = energie_groupe(g1, matrix)
        e2 = energie_groupe(g2, matrix)
        et = energie_groupe(total, matrix)
        print "%6.2f %6.2f %6.2f %6.2f %20s - %-20s"%(dist, e1, e2, et, g1, g2)


def print_tensor(matrix):
    import random
    max_matrix = max(max(x, y) for x, y in matrix)
    pts = [(random.random(), random.random()) for _ in xrange(max_matrix)]
    energy = 100.0
    while energy > 1.0:
        dx, dy = 0.0, 0.0
        newPts = pts[:]
        for i, (x1, y1) in enumerate(pts):
            for j in xrange(i+1, len(pts)):
                x2, y2 = pts[j]
                d = matrix[(i, j)]*20
                e = math.hypot(x2-x1,y2-y1) 
                angle = math.atan2(y2-y1, x2-x1)
                
                f = (d-e)*0.02 
                dx += math.cos(angle)*(f)
                dy += math.sin(angle)*(f) 
            if math.hypot(dx, dy) <= energy:
                dx, dy = 0.0, 0.0
            newPts[i] = (x1 + dx, y1 + dy)
        pts = newPts
        energy -= 1.0
    print_pts(pts)

def main(inFile, outFile):
    data = eval(file(inFile).read())
    names, input = data["filenames"], data["corpus_scores"]
    #raise SystemExit(0)
    matrix = listList_to_matrix(input)
    couples = linkage(matrix, dist_max)
    #print_couples(couples, matrix)
    tree = couples_to_tree(couples)
    sortedNodes, separators = sort_tree(tree, couples, sort_by_diameter(matrix))
    sortedMatrix = permute_matrix(matrix, sortedNodes)
    #print_matrix_with_titles(sortedMatrix, sortedNodes)
    f = open(outFile, "w")
    print_matrix_as_html(f, names, sortedMatrix, sortedNodes, separators, 3)
    #print_matrix_as_tex2(f, names, sortedMatrix, sortedNodes, separators, 3)
    #print_matrix_as_tex(f, names, sortedMatrix, sortedNodes, separators, 3)

import sys, os
producedFiles = []
for fileName in sys.argv[1:]:
  data = eval(file(fileName).read())
  names, input = data["filenames"], data["corpus_scores"]
#  raise SystemExit(0)
#  outFileName = os.path.splitext(fileName)[0] + ".tex"
  outFileName = os.path.splitext(fileName)[0] + ".html"
  producedFiles.append(outFileName)
  main(fileName, outFileName)
print "Produced files: "
for fileName in producedFiles:
    print " - " + "file://" + os.path.join(os.path.abspath("."), fileName)


