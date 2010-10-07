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

def opt_parser():
#fonction main
    parser = OptionParser()

    parser.add_option(
      "-o", "--fileout", dest="fileout", default = "out.js",
      help="write report to the json file FILEOUT [default -o out.js]", metavar="FILEOUT")

    parser.add_option(
      "-q", "--quiet", action="store_false", dest="verbose", default=True,
      help="don't print status messages to stdout" )

    parser.add_option(
      "-t", "--filter", dest= "documentFilter", default = ["t"],
      type = "string", action = "callback", callback = read_list_arg1,
      help="FILTER applied on each document [default : -t t] (-t f1,f2,f1 will apply f1 then f2 and f1) "+
           "Values : {t, s}", metavar="FILTER")

    parser.add_option(
      "-c", "--segmenter", dest="segmenter", default = ["l","1"],
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

