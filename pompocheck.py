# -*- coding:utf-8 -*-
#!/usr/bin/python
from optparse import OptionParser

def main(option):

  if(option.verbose) :
    print " - read file : " + str(option.filename)
  
  dict_check = eval(file(option.filename).read())
  list_filenames,fraud_pairs = dict_check["filenames"],dict_check["fraud_pairs"]
  length = len(list_filenames)

  corpus_scores=[[1. for i in xrange(length)] for j in xrange(length)]
  for i in xrange(length) :
    corpus_scores[i][i] = 0.

  list_index_fraud = []
  for fraud in fraud_pairs :
    print fraud
    f1,f2 = list_filenames.index(fraud[0]),list_filenames.index(fraud[1])
    corpus_scores[f1][f2] = 0.
    corpus_scores[f2][f1] = 0.

  spl = option.filename.split(".")
  if len(spl) == 1 :
    fileout = spl[0] + ".check.js"
  else :
    fileout = ".".join(spl[0:-1]) + ".check.js"
  data="{\"signature\":'ideal', \"filenames\": "+str(list_filenames) + ", \"corpus_scores\": " + str(corpus_scores)+"}"

  if(option.verbose) :
    print " - print in : " + str(fileout)

  output = open(fileout,"w") 
  output.write(str(data))

import sys, os

parser = OptionParser()
parser.add_option("-f", "--files", dest="filename", default="out.js",
                  help = "use the file FILE to create the .js used for pompodiff.py",
                  metavar = "FILE")

parser.add_option("-q", "--quiet",
                   action="store_false", dest="verbose", default=True,
                   help="don't print status messages to stdout")

(opt_options, opt_args) = parser.parse_args()
if(len(opt_args) > 0) :
  opt_options.filename = opt_args[0]


main(opt_options)
