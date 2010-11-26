import distance
from StringMatcher import StringMatcher

class Module_levenshtein(distance.Distance):
    def process(self, seg1, seg2):
        text1 = seg1.getContent() 
        text2 = seg2.getContent() 
        #print repr(text1)
        #print repr(text2)
        d =  self.processText(text1, text2)
        #print d
        return d

    def processText(self, text1, text2):
      String_test = StringMatcher()
      String_test.set_seqs(text1,text2)
      dist = String_test.distance()
      return float(dist) / max(len(text1),len(text2))

if __name__ == "__main__":
    module = Module_levenshtein(None)
    for couple in (('niche', 'chiens'), ('chien', 'chiens'), ('chien', 'chat')):
        print couple, '->', module.processText(*couple)
 
