import math
import distance
#import cpyext
import sys
#import PypyLevenshtein
#sys.path.append('..')
#import tool_dataStructures as tds

class Module_cos(distance.Distance):
  def process(self, seg1, seg2):
    text1 = seg1.getContent() 
    text2 = seg2.getContent() 
    d =  self.processText(text1, text2)
    return d

  def processText(self, text1, text2):
    if text1 == text2 :
      return 0.
    vall = list(set(text1+text2))
    v1 = dict([(l,0) for l in vall])
    v2 = dict([(l,0) for l in vall])
    for l in text1 :
      v1[l] += 1

    for l in text2 :
      v2[l] += 1
    score = 1-get_angle(v1,v2,vall,len(vall)) 
    return score

def get_angle(v1,v2,base,count) :
  up,n1,n2 = 0.,0.,0.
  for i in xrange(count) :
    up += v1[base[i]]*v2[base[i]]
    n1 += math.pow(v1[base[i]],2)
    n2 += math.pow(v2[base[i]],2)
  return (up / math.sqrt(n1*n2))

if __name__ == "__main__":
    module = Module_cos(None)
    for couple in (('niche', 'chiens'), ('chien', 'chiens'), ('chien', 'chat')):
        print couple, '->', module.processText(*couple)
 
