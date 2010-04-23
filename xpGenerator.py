import glob
import random
import string

#filter = ["t","s"]
filter = ["t"]

#segmenter = ["l:1","l:2","l:3","c:10","c:20","c:30"]
segmenter = ["l:1","l:2","l:3","l:4"]
#segmenter = ["l:1"]

#segmentDistances = ["lv","ie","j","jw","eq"]
segmentDistances = ["lv"]

#documentDistanceFilter = ["h,c,t","t,h,c,t"]
documentDistanceFilter = ["h,c,t"]

documentDistance = ["sum"]

#glob_corpus = ['./corpus/python1/1*.py']
glob_corpus = ['./corpus/python1/*.py']
corpus = []
for doc in glob_corpus :
  corpus.append(" ".join(glob.glob(doc)))


all_experiments = {
  "xp_mu": (('-t',), filter,
            ('-c',), segmenter,
            ('-s',), segmentDistances,
            ('-l',), documentDistanceFilter,
            ('-d',), documentDistance,
            corpus)
}

def print_all_experiments(): 
  all_xps = []
  cptout = 0
  for name, args in all_experiments.iteritems():
    xps = [["python pypometre.py"]]
    for lst in args:
      new_xps = []
      for xp in xps:
        for a in lst:
          new_xps.append(xp + [a])
      xps = new_xps
    all_xps += xps

  for i,xp in enumerate(all_xps):
    xp = xp[0] + ' -o %i.js '%(i) + " ".join(xp[1:])
    print xp
 
print_all_experiments()
