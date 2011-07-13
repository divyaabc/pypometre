import glob
import random
import string

#filter = ["t","s"]
#filter = ["t","id"]
filter = ["t"]
#filter = ["id"]

#segmenter = ["l:1","l:2","l:3","l:4","c:10","c:20","c:30","c:40"]
#segmenter = ["c:10","c:20","c:30","c:40"]
#segmenter = ["l:1","l:2","l:3","l:4"]
segmenter = ["l:1"]
#segmenter = ["all"]

#segmentDistances = ["lv","ie","j","jw","eq"]
#segmentDistances = ["lv","eq"]
segmentDistances = ["lv"]
#segmentDistances = ["inf"]

#documentDistanceFilter = ["h,c,t","t,h,c,t"]
#documentDistanceFilter = ["h,c,t","h,hc,c,t"]
#documentDistanceFilter = ["h,c,t"]
documentDistanceFilter = ["c,h,hc,c,t"]
#documentDistanceFilter = ["c,h,hc,c,t,c,t","c,h,hc,c,t,c,t,c,t","c,h,hc,c,t,c,t,c,t,c,t","c,h,hc,c,t,c,t,c,t,c,t,c,t"]
#documentDistanceFilter = ["t,h,c,t"]
#documentDistanceFilter = ["h"]

documentDistance = ["sum"]

#glob_corpus = ['./corpus/python1/*.py','./corpus/haskell1/*.hs','./corpus/bash1/*.sh','./corpus/bash2/*.sh']
#glob_corpus = ['./corpus/c_expression_arithmetique/**/*.all']
#glob_corpus = ['./corpus/c_serveur/**/*.all']
#glob_corpus = ['./corpus/haskell1/*.hs','./corpus/c_serveur/**/*.all','./corpus/bash1/*.sh']
glob_corpus = ['./corpus/c2/*.c']
#glob_corpus = ['./corpus/haskell1/*.hs']
#glob_corpus = ['./corpus/php1/**/*.php']
#glob_corpus = ['./corpus/c_serveur/**/*.all']
#glob_corpus = ['./corpus/c_arbre/**/*.all']
#glob_corpus = ['./corpus/bash1/*.sh']
#glob_corpus = ['./corpus/java_p4/*.all']

corpus = []
for doc in glob_corpus :
  corpus.append(" ".join(glob.glob(doc)))

all_experiments = {
  "xp_mu": (('-t',), filter,
            ('-c',), segmenter,
            ('-s',), segmentDistances,
            ('-l',), documentDistanceFilter,
            ('-d',), documentDistance,
            ('-q',),
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
    xp = xp[0] + ' -o %04d.js '%(i) + " ".join(xp[1:])
    print xp
 
print_all_experiments()
