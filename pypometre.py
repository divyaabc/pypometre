#!/usr/bin/python
import os, sys
from dataStructures import *

def getClassOf(typ, name):
    fileName = "%s.mod_%s"%(typ, name)
    #capitalizedTyp = typ[0].upper() + typ[1:]
    className = "Module_%s"%(name)
    #mod = __import__(fileName)
    mod = __import__(fileName, None, None, [className], -1)
    #print [x for x in mod.__dict__ if x.startswith("Doc")]
    #print mod.DocumentFilters_t
    class_ = getattr(mod, className)
    print fileName, 
    print class_
    return class_

def main():
    context = {}
    documentFilter = getClassOf("documentFilters", "t")(context)
    #documentSegmenter = getClassOf("documentSegmenters", "newline")(context)
    documentSegmenter = getClassOf("documentSegmenters", "nline")(3)
    #documentSegmenter = getClassOf("documentSegmenters", "nchar")(5)
    #segmentDistance = getClassOf("segmentDistances", "jaro")(context)
    #segmentDistance = getClassOf("segmentDistances", "jaro_winkler")(context)
    segmentDistance = getClassOf("segmentDistances", "levenshtein")(context)
    #segmentDistance = getClassOf("segmentDistances", "equals")(context)
    documentDistance = getClassOf("documentDistances", "hungarian")(context)
    resultsPresenter = getClassOf("resultsPresenters", "coloredAndSortedMatrix")(context)

 
    document_names = sys.argv[1:]

    print "Creating corpus..."
    initial_corpus = []
    for fileName in document_names:
        content = Document(fileName)
        initial_corpus.append(content)

    print "Filtering documents..."
    filtered_corpus = []
    for document in initial_corpus:
        filtered_document = documentFilter(document)
        filtered_corpus.append(filtered_document)

    print "Segmentation..."
    segmented_corpus = []
    for document in filtered_corpus:
        segmented_document = documentSegmenter(document)
        segmented_corpus.append(segmented_document)

#     for document in segmented_corpus :
#       print document.str_verbose()    
#     return 0


    print "Building segments distances matrices"
    documents_distances = DistMatrix(len(segmented_corpus), len(segmented_corpus))
    for i, document1 in enumerate(segmented_corpus):
        segLst1 = document1.getSegmentation()
        for j, document2 in enumerate(segmented_corpus):
            if j <= i:
                continue
            print " * matrix :", document1, document2  
            segLst2 = document2.getSegmentation()
            print "   * distance matrix"
            matrix = DistMatrix(len(segLst1), len(segLst2))
            for x, seg1 in enumerate(segLst1):
                for y, seg2 in enumerate(segLst2):
                    distance = segmentDistance(seg1, seg2)
                    matrix.set(x, y, distance)
            print "   * document distance"
            distance = documentDistance(matrix)
            documents_distances.set(i, j, distance)
            documents_distances.set(j, i, distance)

    print_json = '{"filenames" : \n  '
    list_str_document = []
    for document in segmented_corpus :
      list_str_document.append(str(document)) 
    print_json += str(list_str_document)
    print_json += ',\n "corpus_scores" : \n  '+str(documents_distances) + '\n}'

    out = './out.js'
    file_out = open(out,'w')
    file_out.write(print_json)
    file_out.close()

#    print 
#    resultsPresenter(document_names, documents_distances)

main()
