# -*- coding:utf-8 -*-
#!/usr/bin/python
from optparse import OptionParser
def vararg_callback(option, opt_str, value, parser):
     assert value is None
     value = []

     def floatable(str):
         try:
             float(str)
             return True
         except ValueError:
             return False

     for arg in parser.rargs:
         # stop on --foo like options
         if arg[:2] == "--" and len(arg) > 2:
             break
         # stop on -a, but not on -3 or -3.0
         if arg[:1] == "-" and len(arg) > 1 and not floatable(arg):
             break
         value.append(arg)

     del parser.rargs[:len(value)]
     setattr(parser.values, option.dest, value)

def listList_to_matrix(lstLst):
    matrix = {}
    for i, lst in enumerate(lstLst):
        for j, v in enumerate(lst):
            matrix[(i, j)] = v
    return matrix

def compareChains(c1, c2):
    matrix1 = listList_to_matrix(c1["corpus_scores"])
    matrix2 = listList_to_matrix(c2["corpus_scores"])
    sum=0
    for i,file1 in enumerate(c1["filenames"]):
        i2 = c2["filenames"].index(file1)
        for j,file2 in enumerate(c1["filenames"]):
            j2 = c2["filenames"].index(file2)
            sum += abs(matrix1[(i,j)]-matrix2[(i2,j2)])
    return sum

def main(option):
    chains = []

    if(option.verbose) :
      print " - read files : " + str(option.files)

    length,filenames = len(option.files),option.files
    corpus_scores = [[0 for i in xrange(length)] for j in xrange(length)]
    for i,c in enumerate(option.files):
        chains.append(eval(file(c).read()))
    
    for i,c1 in enumerate(chains):
        for j,c2 in enumerate(chains):
            corpus_scores[i][j] = compareChains(c1,c2)
    signatures = [filenames[c]+"|"+i["signature"] for c,i in enumerate(chains)]
    signature = ";".join(signatures)
    data = "{\"signature\":\""+signature+"\", \"filenames\": "+str(filenames) + ", \"corpus_scores\": " + str(corpus_scores)+"}"

    if(option.verbose) :
      print " - print in : " + str(option.output)

    output = open(option.output,"w") 
    output.write(str(data))

import sys, os
parser = OptionParser()

parser.add_option("-f", "--files", dest="files",
                  help = "compare the files FILES, each FILE being a pypometre.py output done with the same corpora but different parameters",
                  metavar = "FILES", action="callback", callback=vararg_callback)

parser.add_option("-q", "--quiet",
                   action="store_false", dest="verbose", default=True,
                   help="don't print status messages to stdout")

parser.add_option("-o", "--output", dest="output", default="report_pompodiff.js")

(opt_options, opt_args) = parser.parse_args()

if(len(opt_args) > 1) :
  opt_options.files = opt_args

main(opt_options)
