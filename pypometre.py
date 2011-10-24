#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
sys.path.append('./tools/')

import pprint
from dataStructures import *
import tool_dataStructures as tds
from pypometre_optparser import opt_parser_pypometre
#from optparse import OptionParser
#import types


import time
import tool_numpy as tn
#from munkres import *
import random

# recupere le fichier mod_name dans le dossier typ et charge Module_name
def getClassOf(typ, name):
  fileName = "%s.mod_%s"%(typ, name)
  className = "Module_%s"%(name)
  mod = __import__(fileName, None, None, [className], -1)
  class_ = getattr(mod, className)
  return class_

# renvoi la matrice identite _n*_n normalise (matrice de convolution)
def getMatrixId(_n) :
  f = []
  val = 1. / _n
  for i in xrange(_n) :
    line = [val if(i==j) else 0 for j in xrange(_n)]
    f.append(line)
  return f

def getMatrixCenter(_n) :
  f = []
  val = 1. / (_n - 1)
  for i in xrange(_n) :
    line = [val if(i==j) else 0 for j in xrange(_n)]
    f.append(line)
  c = int(_n/2) + 1
  f[c][c] = 0
  return f

def main(args=sys.argv[1:]):
    path_log1 = "./log/documentDistances"
    path_log2 = "./log/documentDistanceFilters"

    parser = opt_parser_pypometre()
    
    (opt_options, opt_args) = parser.parse_args(args)
    opt_fileout = opt_options.fileout

    signature = str(opt_options)

    context = {}
    matrix_id = getMatrixId(5)
#    matrix_id = getMatrixCenter(5)
    lPatch = LinedMatrix(0,0)
    lPatch.convertDistMatrix(matrix_id)
    context["convolve"] = lPatch
    context["threshold"] = (0.0,0.7)

    if len(opt_options.segmenter) > 1 :
      context["segmenter_n"] = int(opt_options.segmenter[1])

#choix du documentSegmenter
    documentSegmenter = getClassOf("documentSegmenters", opt_options.segmenter[0])(context)
#choix du segmentDistance
    segmentDistance = getClassOf("segmentDistances", opt_options.segmentDistance)(context)
#choix du documentFilter
    filters =[getClassOf("documentFilters",x)(context) for x in opt_options.documentFilter]
#choix des documentDistancesFilters
    documentDistanceFilters = []
    for x in opt_options.documentDistanceFilter :
      documentDistanceFilters.append(getClassOf("documentDistancesFilters",x)(context))
#choix du documentDistance
    documentDistance = getClassOf("documentDistances", opt_options.documentDistance)(context)

    if(opt_options.verbose) :
      print '[ok] Creating corpus, filtering documents, building segments distances matrices'

    segmented_corpus = []
    list_auto_corres = []
    for fileName in opt_args :
      try:
        content = Document(fileName)
        for f in filters :
          content = f(content)
        content = documentSegmenter(content)
#        print content.ff
#        print content.content
#        auto = get_auto_corres(content)
#        print auto
#        1/0
        segLst1 = content.getSegmentation()
#        if(len(segLst1) > 0) :
        segmented_corpus.append(content)
      except Exception, e:
        pass
      list_auto_corres.append(tds.get_auto_corres(content))

    len_segmented_corpus = len(segmented_corpus)
    lmatrix_docDist = LinedMatrix(len_segmented_corpus, len_segmented_corpus)

#    for i, document1 in enumerate(segmented_corpus):
    for i in xrange(len_segmented_corpus):#enumerate(segmented_corpus):
      document1 = segmented_corpus[i]
      auto_corres1 = list_auto_corres[i]
      segLst1 = document1.getSegmentation()
      name_doc1 = os.path.split(str(document1))[1]
      for j in xrange(len_segmented_corpus):
        if j <= i:
          continue
        document2 = segmented_corpus[j]

        if(opt_options.verbose) :
          print "[go] distance(%s,%s)"%(document1, document2)

        segLst2 = document2.getSegmentation()
        auto_corres2 = list_auto_corres[j]
        name_doc2 = os.path.split(str(document2))[1]

#        matrix = DistMatrix(len(segLst1), len(segLst2))

        ll1 = len(auto_corres1)
        ll2 = len(auto_corres2)

        matrix = LinedMatrix(len(segLst1),len(segLst2))

        for x in xrange(ll1) :
          seg1 = segLst1[auto_corres1[x][0]]
          for y in xrange(ll2) :
            dist = segmentDistance(seg1, segLst2[auto_corres2[y][0]])
            for xx in auto_corres1[x] :
              for yy in auto_corres2[y] :
                ni = xx + yy*matrix._width
                matrix.data[ni] = dist

#        for x in xrange(l1):
#          seg1 = segLst1[x]
#          for y in xrange(l2):
#            ni = x + y*matrix._width
#            matrix.data[ni] = segmentDistance(seg1, segLst2[y])

#            matrix.set(x, y, distance)

        cpt = 0
        if(opt_options.verbose) :
          tn.matrix2image(tn.matrix2numpy(matrix.getMatrix()),"%s/%s_x_%s%i.png"%(path_log1,name_doc1,name_doc2,cpt))

        for f in documentDistanceFilters :
          cpt += 1
#          print f
          matrix = f(matrix)
          if(opt_options.verbose) :
            tn.matrix2image(tn.matrix2numpy(matrix.getMatrix()),"%s/%s_x_%s%i.png"%(path_log1,name_doc1,name_doc2,cpt))
#            tn.matrix2image(matrix,"%s/%s_x_%s%i.png"%(path_log2,name_doc1,name_doc2,nb))

        distance = documentDistance(matrix)
        
        if(opt_options.verbose) :
          print "[ok] distance(%s,%s) = %0.2f "%(document1, document2, distance)
        lmatrix_docDist.set(i,j,distance)
        lmatrix_docDist.set(j,i,distance)

    list_str_document = [str(doc) for doc in segmented_corpus]
    print_json = '''
{"signature" : "%s",\n 
 "filenames" : %s, \n 
 "corpus_scores" : %s \n
}'''%(signature,str(list_str_document),str(lmatrix_docDist))

    if(opt_options.verbose) :
      print "[out] writing :", opt_options.fileout

    file_out = open(opt_options.fileout,'w')
    file_out.write(print_json)
    file_out.close()
    return print_json

if __name__ == "__main__":
#    l = [[random.random() for _ in xrange(10)] for _ in xrange(10)]
#    m = Munkres()
#    res = m.compute(l)
#    start = time.clock()
    main()
    end = time.clock()
#    print "[time] %f"%(end-start)
