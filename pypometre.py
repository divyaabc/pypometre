#!/usr/bin/python
import os, sys
import pprint
from dataStructures import *
import Image
import numpy
from optparse import OptionParser

#prend une matrice de distance entre segment et l'ecrit au format png dans le fichier _path
def matrix2image(_matrix,_path):
  a_print = _matrix.copy()
  a_print = (1. - a_print) * 255
  a_print = a_print.astype(numpy.uint8)
  Image.fromarray(a_print).save(_path)

# recupere le fichier mod_name dans le dossier typ et charge Module_name
def getClassOf(typ, name):
    fileName = "%s.mod_%s"%(typ, name)
    className = "Module_%s"%(name)
    mod = __import__(fileName, None, None, [className], -1)
    class_ = getattr(mod, className)
    print fileName, 
    print class_
    return class_

# renvoi la matrice identite _n*_n normalise (matrice de convolution)
def getMatrixId(_n) :
  filter = []
  val = 1. / _n
  for i in xrange(_n) :
    line = []
    for j in xrange(_n) :
      if i == j :
        line.append(val)
      else :
        line.append(0)
    filter.append(line)
  return filter

#parse des option separee par des ","
def read_list_arg1(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(','))

#parse des option separee par des ":"
def read_list_arg2(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(':'))

#fonction main
def main():
    parser = OptionParser()
    parser.add_option("-o", "--file", dest="fileout", default = "out.js",
                       help="write report to FILEOUT", metavar="FILEOUT")
    parser.add_option("-q", "--quiet",
                       action="store_false", dest="verbose", default=True,
                       help="don't print status messages to stdout")


    parser.add_option("-t", "--filter", dest="documentFilter", default = ["t"],
                       type = "string", action = "callback", callback = read_list_arg1,
                       help="FILTER applied on each document (-t f1,f2,f1 will apply f1 then f2 and f1)", metavar="FILTER")

    parser.add_option("-c", "--segmenter", dest="segmenter", default = ["l","1"],
                       type = "string", action = "callback", callback = read_list_arg2,
                       help="use de segmenter SEG", metavar="SEG")

    parser.add_option("-s", "--segmentDistance", dest="segmentDistance", default = "levenshtein",
                       help="use de distance between segments SEGDIST (lv: levenshtein, ie: inner entropy, j: jaro, jw: jaro winkler, eq: equals)", metavar="SEGDIST")

    parser.add_option("-l", "--documentDistanceFilter", dest="documentDistanceFilter",
                       default = ["h"],
                       type = "string", action = "callback", callback = read_list_arg1,
                       help="DOCDISTFILTER applied on the segment matrix (-l f1,f2,f1 will apply f1 then f2 and f1)", metavar="DOCDISTFILTER")


    parser.add_option("-d", "--documentDistance", dest="documentDistance", default = "sum",
                       help="compute the distance DOCDIST on the segment matrix", metavar="DOCDIST")


    (opt_options, opt_args) = parser.parse_args()
    opt_fileout = opt_options.fileout



    context = {}
    context["convolve"] = getMatrixId(5)
    context["threshold"] = (0.3,0.7)
    context["segmenter_n"] = int(opt_options.segmenter[1])
#choix du documentFilter

    filters=[ getClassOf("documentFilters",x)(context) for x in opt_options.documentFilter]

#     documentFilter = getClassOf("documentFilters", "t")(context)
#     documentFilter = getClassOf("documentFilters", "s")(context)

#choix du documentSegmenter

    segmenterMap = {"l":"nline","c":"nchar"}
    if segmenterMap.has_key(opt_options.segmenter[0]):
      documentSegmenter = getClassOf("documentSegmenters", segmenterMap[opt_options.segmenter[0]])(context)
    else:
      documentSegmenter = getClassOf("documentSegmenters", opt_options.segmenter[0])(context)

    #documentSegmenter = getClassOf("documentSegmenters", "nline")(1)
    #documentSegmenter = getClassOf("documentSegmenters", "newline")(context)
    #documentSegmenter = getClassOf("documentSegmenters", "nchar")(1)

#choix du segmentDistance

    segDistMap = {"lv":"levenshtein","ie":"innerEntropy","j":"jaro","jw":"jaro_winkler","eq":"equals"}
    if segDistMap.has_key(opt_options.segmentDistance):
      segmentDistance = getClassOf("segmentDistances", segDistMap[opt_options.segmentDistance])(context)
    else:
      segmentDistance = getClassOf("segmentDistances", opt_options.segmentDistance)(context)

    #segmentDistance = getClassOf("segmentDistances", "innerEntropy")(context)
    #segmentDistance = getClassOf("segmentDistances", "levenshtein")(context)
    #segmentDistance = getClassOf("segmentDistances", "jaro")(context)
    #segmentDistance = getClassOf("segmentDistances", "jaro_winkler")(context)
    #segmentDistance = getClassOf("segmentDistances", "equals")(context)

#choix des documentDistancesFilters
    documentDistanceFilterH = getClassOf("documentDistancesFilters", "hungarian")({})
    documentDistanceFilterC = getClassOf("documentDistancesFilters", "convolve")(context)
    documentDistanceFilterT = getClassOf("documentDistancesFilters", "threshold")(context)

#choix du documentDistance
    documentDistance = getClassOf("documentDistances", "sum")({})

#    resultsPresenter = getClassOf("resultsPresenters", "coloredAndSortedMatrix")(context)

    print "Creating corpus..."
    initial_corpus = []
    for fileName in opt_args:
        content = Document(fileName)
        initial_corpus.append(content)

    print "Filtering documents..."
    filtered_corpus = []
    for document in initial_corpus:
      filtered_document = document
      for f in filters:
        filtered_document = f(filtered_document)
      filtered_corpus.append(filtered_document)

    print "Segmentation..."
    segmented_corpus = []
    for document in filtered_corpus:
      segmented_document = documentSegmenter(document)
      segmented_corpus.append(segmented_document)

#    for document in segmented_corpus :
#      print document.str_verbose()    
#    return 0

    print "Building segments distances matrices"
    documents_distances = DistMatrix(len(segmented_corpus), len(segmented_corpus))
    for i, document1 in enumerate(segmented_corpus):
        segLst1 = document1.getSegmentation()
        name_doc1 = os.path.split(str(document1))[1]
        for j, document2 in enumerate(segmented_corpus):
            if j <= i:
                continue
            print " * matrix :", document1, document2  
            segLst2 = document2.getSegmentation()
            name_doc2 = os.path.split(str(document2))[1]
            print "   * distance matrix"
            matrix = DistMatrix(len(segLst1), len(segLst2))
            for x, seg1 in enumerate(segLst1):
                for y, seg2 in enumerate(segLst2):
                    distance = segmentDistance(seg1, seg2)
                    matrix.set(x, y, distance)
            print "   * document distance filter"

            matrix = matrix.convert2numpy()

            matrix_hungarian = documentDistanceFilterH(matrix)
            context_hungarian = documentDistanceFilterH._context
            pairs_hungarian = context_hungarian["pairs"]

            matrix_convolve = documentDistanceFilterC(matrix_hungarian)
            matrix_threshold = documentDistanceFilterT(matrix_convolve)

#            path  = "./log/documentDistances/"
#            path += "./distance_" + name_doc1 + "_" + name_doc2 + ".png"
#            matrix2image(matrix_threshold,path)

            print "   * document distance"
            documentDistance._context["pairs"] = pairs_hungarian
            distance = documentDistance(matrix_threshold)
            print distance

            documents_distances.set(i, j, distance)
            documents_distances.set(j, i, distance)

    print_json = '{"filenames" : \n  '
    list_str_document = []
    for document in segmented_corpus :
      list_str_document.append(str(document)) 
    print_json += str(list_str_document)
    print_json += ',\n "corpus_scores" : \n  '+str(documents_distances) + '\n}'

    print
    print "---> " + opt_options.fileout

    file_out = open(opt_options.fileout,'w')
    file_out.write(print_json)
    file_out.close()

main()
