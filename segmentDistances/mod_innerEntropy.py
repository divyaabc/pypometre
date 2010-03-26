import distance
import math

class Module_innerEntropy(distance.Distance):
  def process(self, seg1, seg2):
    text1 = unicode(seg1.getContent(),'utf-8')
    text2 = unicode(seg2.getContent(),'utf-8')
    e1 = getInnerEntropy(text1) 
    e2 = getInnerEntropy(text2)
    res = getDiff(e1,e2)
    return res

def getDiff(a,b) :
  m = max(a,b)
  if m == 0 :
    return 0
  else :
    return abs(a-b) / max(a,b)

def getInnerEntropy(_str) :
  alphabet = getAlphabet(_str)
  str_len = len(_str)
  entropy = 0
  for l,nb in alphabet.iteritems() :
    prob = float(nb) / float(str_len)
    entropy -= float(prob) * math.log(prob,2) 
  return entropy
    
def getAlphabet(_str) :
  alphabet = {}
  for l in _str :
    if l in alphabet.keys() :
      alphabet[l] += 1
    else :
      alphabet[l] = 1
  return alphabet


