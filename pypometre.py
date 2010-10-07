#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import pprint
from dataStructures import *
import Image
import numpy
from pypometre_optparser import opt_parser
#from optparse import OptionParser
#import types


#prend une matrice de distance entre segment et l'ecrit au format png dans le fichier _path
def matrix2image(_matrix,_path):
  a_print = _matrix.copy()
  a_print = (1. - a_print) * 255
  a_print = a_print.astype(numpy.uint8)
  Image.fromarray(a_print).save(_path)

# recupere le fichier mod_name dans le dossier typ et charge Module_name
def getClassOf(typ, name):
    if isinstance(name, list):
        name = name[0]
    fileName = "%s.mod_%s"%(typ, name)
    className = "Module_%s"%(name)
    mod = __import__(fileName, None, None, [className], -1)
    class_ = getattr(mod, className)
#    print fileName, 
#    print class_
    return class_

# renvoi la matrice identite _n*_n normalise (matrice de convolution)
def getMatrixId(_n) :
  f = []
  val = 1. / _n
  for i in xrange(_n) :
    line = []
    for j in xrange(_n) :
      if i == j :
        line.append(val)
      else :
        line.append(0.)
    f.append(line)
  return f


def getMatrixCenter(_n) :
  f = []
  val = 1. / (_n - 1)
  for i in xrange(_n) :
    line = []
    for j in xrange(_n) :
      if i == j :
        line.append(val)
      else :
        line.append(0.)
    f.append(line)
  c = int(_n/2) + 1
  f[c][c] = 0
  return f

def get_signature(option, mapAlias) :
  dict_option = eval(str(option))
  list_keys = dict_option.keys()
  list_keys.sort()
  sign = ""
  for module in list_keys :
    if module != "fileout" and module != "verbose":
      sign += str(module) 
      if isinstance(dict_option[module],list): #type(dict_option[module]) == types.ListType :
        for v in dict_option[module] :
          if mapAlias.has_key(module) :
            if mapAlias[module].has_key(v[0]) :
              v =mapAlias[module][v[0]]
          sign += "," + v[0] 
      else :
        if mapAlias.has_key(module) :
          if mapAlias[module].has_key(dict_option[module]) :
            sign += "," + mapAlias[module][dict_option[module]]
        else :
          sign += "," + dict_option[module]
      sign += "|"
  sign = sign[:-1]
  return sign

def get_cmdLine(option, mapAlias) :
  dict_option = eval(str(option))
  list_keys = dict_option.keys()
  list_keys.sort()
  sign = ""
  for module in list_keys :
    if module != "fileout" and module != "verbose":
      sign += str(module) 
      if isinstance(dict_option[module],list): #type(dict_option[module]) == types.ListType :
        for v in dict_option[module] :
          if mapAlias.has_key(module) :
            if mapAlias[module].has_key(v[0]) :
              v = mapAlias[module][v[0]]
          sign += "," + ':'.join(v)
      else :
        if mapAlias.has_key(module) :
          if mapAlias[module].has_key(dict_option[module]) :
            sign += "," + mapAlias[module][dict_option[module]]
        else :
          sign += "," + dict_option[module]
      sign += " "
  sign = sign[:-1]
  return sign


def main(args=sys.argv[1:]):
    parser = opt_parser()
    
    (opt_options, opt_args) = parser.parse_args(args)
    opt_fileout = opt_options.fileout

    mapAlias = {
      "segmenter" : {
        "l":"nline", "c":"nchar", "a" : "all"
      },

      "segmentDistance" : {
        "lv":"levenshtein", "ie":"innerEntropy", "j":"jaro",
        "jw":"jaro_winkler", "eq":"equals", "inf":"information"
      },
    
      "documentDistanceFilter" : {
        "h":"hungarian", "c":"convolve", "t":"threshold",
        "hc":"hungarian_clean", "jv":"lapjv"
      }
    }

    signature = get_signature(opt_options, mapAlias)

    context = {}
    matrix_id = getMatrixId(5)
#    matrix_id = getMatrixCenter(5)
    context["convolve"] = matrix_id
    context["threshold"] = (0.0,0.7)

    if len(opt_options.segmenter) > 1 :
      context["segmenter_n"] = int(opt_options.segmenter[1])

#choix du documentFilter
    filters=[ getClassOf("documentFilters",x)(context) for x in opt_options.documentFilter]
#     documentFilter = getClassOf("documentFilters", "t")(context)
#     documentFilter = getClassOf("documentFilters", "s")(context)

#choix du documentSegmenter
    segmenterMap = mapAlias['segmenter']
    if segmenterMap.has_key(opt_options.segmenter[0][0]):
      documentSegmenter = getClassOf("documentSegmenters", segmenterMap[opt_options.segmenter[0][0]])(context)
    else:
      documentSegmenter = getClassOf("documentSegmenters", opt_options.segmenter[0][0])(context)

#choix du segmentDistance
    segDistMap = mapAlias['segmentDistance']
    if segDistMap.has_key(opt_options.segmentDistance):
      segmentDistance = getClassOf("segmentDistances", segDistMap[opt_options.segmentDistance])(context)
    else:
      segmentDistance = getClassOf("segmentDistances", opt_options.segmentDistance)(context)

#choix des documentDistancesFilters
    docDistFiltMap = mapAlias['documentDistanceFilter']
    documentDistanceFilters = []
    for x in opt_options.documentDistanceFilter :
      if docDistFiltMap.has_key(x) :
        documentDistanceFilters.append(getClassOf("documentDistancesFilters",docDistFiltMap[x])(context))
      else :
        documentDistanceFilters.append(getClassOf("documentDistancesFilters",x)(context))

#choix du documentDistance
    documentDistance = getClassOf("documentDistances", opt_options.documentDistance)(context)

#    resultsPresenter = getClassOf("resultsPresenters", "coloredAndSortedMatrix")(context)

    if(opt_options.verbose) :
      print "Creating corpus..."
    initial_corpus = []
    for fileName in opt_args:
      try:
        content = Document(fileName)
        initial_corpus.append(content)
      except Exception, e:
        print e

    if(opt_options.verbose) :
      print "Filtering documents..."
    filtered_corpus = []
    for document in initial_corpus:
      filtered_document = document
      for f in filters:
        filtered_document = f(filtered_document)
      filtered_corpus.append(filtered_document)

    if(opt_options.verbose) :
      print "Segmentation..."
    segmented_corpus = []
    for document in filtered_corpus:
      segmented_document = documentSegmenter(document)
      segmented_corpus.append(segmented_document)

#    for document in segmented_corpus :
#      print document.str_verbose()    
#    return 0

    if(opt_options.verbose) :
      print "Building segments distances matrices"
    documents_distances = DistMatrix(len(segmented_corpus), len(segmented_corpus))
    for i, document1 in enumerate(segmented_corpus):
        segLst1 = document1.getSegmentation()
        name_doc1 = os.path.split(str(document1))[1]
        for j, document2 in enumerate(segmented_corpus):
            if j <= i:
                continue
            if(opt_options.verbose) :
              print " * matrix :", document1, document2  
            segLst2 = document2.getSegmentation()
            name_doc2 = os.path.split(str(document2))[1]
            if(opt_options.verbose) :
              print "   * distance matrix"
            matrix = DistMatrix(len(segLst1), len(segLst2))
            for x, seg1 in enumerate(segLst1):
                for y, seg2 in enumerate(segLst2):
                    distance = segmentDistance(seg1, seg2)
                    matrix.set(x, y, distance)
            if(opt_options.verbose) :
              print "   * document distance filter"

            matrix = matrix.convert2numpy()

            if(opt_options.verbose) :
              matrix2image(matrix,"./log/documentDistances/"+name_doc1+"_x_"+name_doc2+".png")

            for nb,filter in enumerate(documentDistanceFilters) :
              matrix = filter(matrix)
              if(opt_options.verbose) :
                matrix2image(matrix,"./log/documentDistanceFilters/"+name_doc1+"_x_"+name_doc2+"_"+str(nb)+".png")


            if(opt_options.verbose) :
              print "   * document distance"

            distance = documentDistance(matrix)

            if(opt_options.verbose) :
              print "   * distance = " + str(distance)
#            else :
#              print " * ", document1, document2, " : ", distance

            documents_distances.set(i, j, distance)
            documents_distances.set(j, i, distance)

    print_json = '{"signature" : \'' + signature + '\',\n "filenames" : \n  '
    list_str_document = []
    for document in segmented_corpus :
      list_str_document.append(str(document)) 
    print_json += str(list_str_document)
    print_json += ',\n "corpus_scores" : \n  '+str(documents_distances) + '\n}'

    if(opt_options.verbose) :
        print
        print "   * writing : " + opt_options.fileout


    file_out = open(opt_options.fileout,'w')
    file_out.write(print_json)
    file_out.close()
    return print_json

if __name__ == "__main__":
    main()
