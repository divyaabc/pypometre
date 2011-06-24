import distance
#import cpyext
from StringMatcher import StringMatcher

import sys
sys.path.append('..')
import tool_dataStructures as tds

class Module_lv(distance.Distance):
  def process(self, seg1, seg2):
    text1 = seg1.getContent() 
    text2 = seg2.getContent() 
    d =  self.processText(text1, text2)
    return d

  def processText(self, text1, text2):
    String_test = StringMatcher()
    String_test.set_seqs(text1, text2)
    dist = String_test.distance()
#    dist = tds.levenshtein(text1,text2)
    return float(dist) / max(len(text1),len(text2))

if __name__ == "__main__":
    module = Module_levenshtein(None)
    for couple in (('niche', 'chiens'), ('chien', 'chiens'), ('chien', 'chat')):
        print couple, '->', module.processText(*couple)
 
