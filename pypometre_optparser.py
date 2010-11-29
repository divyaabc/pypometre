from optparse import OptionParser

#parse des options separees par des ","
def read_list_arg(option, opt, value, parser):
  print value
  lst = [m.split(':') for m in value.split(',')]
  print lst
  setattr(parser.values, option.dest, lst)

def read_list_arg1(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(','))

#parse des options separees par des ":"
def read_list_arg2(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(':'))

def opt_parser_pompoview():
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
                     help="Normalize each values of the matrix between [minVal,maxVal] [default : False]")
  parser.add_option("-m", "--mode",
                     dest="mode", default="html",
                     help="Output mode : png, html, tex (prepared for input), doc (prepared for pdflatex), json (prepared for pompozoom)")
  parser.add_option("-p", "--projection",
                     action="store_true", dest="projection", default=False,
                     help="Project the values of the matrix on the x-axis : (default = False)")
  parser.add_option("-c", "--nb_class", dest="nb_class", default = "4", type = "int",
                     help="Use a coloration in NBCLASS classes [default : 4]", metavar="NBCLASS")
  parser.add_option("-d", "--dist", dest="dist", default = "max",
                     help="Use the distance DIST to compute similarities between clusters of documents [default : -d max] values : {max,min,avg}", metavar="DIST")
  return parser

def opt_parser_pypometre():
#fonction main
    parser = OptionParser()

    parser.add_option("-o", "--fileout", dest="fileout", default = "out.js",
                      help="write report to the json file FILEOUT [default -o out.js]", metavar="FILEOUT")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout" )
    parser.add_option("-t", "--filter", dest= "documentFilter", default = ["t"],
                      type = "string", action = "callback", callback = read_list_arg1,
                      help="FILTER applied on each document [default : -t t] (-t f1,f2,f1 will apply f1 then f2 and f1) "+
                      "Values : {t, s, id}", metavar="FILTER")
    parser.add_option("-c", "--segmenter", dest="segmenter", default = ["l","1"],
                      type = "string", action = "callback", callback = read_list_arg2,
                      help="use de segmenter SEG [default : -c l:1] Values : {c:[0-9], l:[0-9], a}",
                      metavar="SEG")
    parser.add_option(
      "-s", "--segmentDistance", dest="segmentDistance", default = "levenshtein",
      help='use de distance between segments SEGDIST [default : -s lv] ' +
           'Values : {lv|levenshtein, ie|innerEntropy, j|jaro, jw|jaro_winkler, eq|equals}',
      metavar="SEGDIST")
    parser.add_option(
      "-l", "--documentDistanceFilter", dest="documentDistanceFilter", default = ["c","t","h","c","t"],
      type = "string", action = "callback", callback = read_list_arg1,
      help="DOCDISTFILTER applied on the segment matrix [default : -l c,t,h,c,t] (-l f1,f2,f1 will apply f1 then f2 and f1) "+
           "Values : {h|hungarian, t|threshold, c|convolute, jv|lapjv}", metavar="DOCDISTFILTER")
    parser.add_option(
      "-d", "--documentDistance", dest="documentDistance", default = "sum",
      help="compute the distance DOCDIST on the segment matrix [default : -d sum]" +
           "Values : {sum}", metavar="DOCDIST")
    return parser

def opt_parser_pypoblitz():
  parser = opt_parser_pypometre()
  parser.add_option("-a", "--args", dest="args", default = "", help="dommage")
  parser.add_option("-m", "--method", dest="method", default = "fork", help="dommage")
  return parser

