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
  parser = OptionParser()

  parser.add_option(
    "-o", "", dest="fileout", default = "out.js",
    help="write report to the json file FILEOUT [default -o out.js]",
    metavar="FILEOUT")

  parser.add_option(
    "-q", "", action="store_false", dest="verbose", default=True,
    help="don't print status messages to stdout")

  parser.add_option(
    "-t", "", dest= "documentFilter", default = ["t","s","el"],
    type = "string", action = "callback", callback = read_list_arg1,
    help="FILTER applied on each document [default : -t t,s,el] (-t f1,f2 will apply f1 then f2) Values : {t, s, id, el}",
    metavar="FILTER")

  parser.add_option(
    "-c", "", dest="segmenter", default = ["nl","1"],
    type = "string", action = "callback", callback = read_list_arg2,
    help="use de segmenter SEG [default : -c nl:1] Values : {nc:[0-9], nl:[0-9], a, ib}",
    metavar="SEG")

  parser.add_option(
    "-s", "", dest="segmentDistance", default = "lv",
    help='use de distance SEGDIST between segments [default : -s lv] Values : {i, lv, ie, j, jw, eq, cos}',
    metavar="SEGDIST")

  parser.add_option(
    "-l", "", dest="documentDistanceFilter", default = ["t","c","h","c","t"],
    type = "string", action = "callback", callback = read_list_arg1,
    help = "Filters DOCDISTFILTER applied on the segment matrix [default : -l t,c,h,c,t] (-l f1,f2,f1 will apply f1 then f2 then f1) Values : {h|hungarian, t|threshold, c|convolute, hc|hungarian_clean}",
    metavar="DOCDISTFILTER")

  parser.add_option(
    "-d", "", dest="documentDistance", default = "sum",
    help="compute the distance DOCDIST on the segment matrix [default : -d sum] Values : {sum}",
    metavar="DOCDIST")

  return parser

def opt_parser_pypoblitz():
  parser = opt_parser_pypometre()
  parser.add_option("-a", "--args", dest="args", default = "", help="dommage")
  parser.add_option("-m", "--method", dest="method", default = "fork", help="-m fork")
  return parser

