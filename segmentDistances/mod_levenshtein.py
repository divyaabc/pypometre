import distance
from StringMatcher import StringMatcher

class Module_levenshtein(distance.Distance):
    def process(self, seg1, seg2):
        text1 = seg1.getContent() 
        text2 = seg2.getContent() 
        return self.processText(text1, text2)

    def processText(self, text1, text2):
      len_text1 = len(text1)
      len_text2 = len(text2)
      String_test = StringMatcher()
      String_test.set_seqs(text1,text2)
      dist = String_test.distance()
      return float(dist) / max(len_text1, len_text2)


    def processText2(self, text1, text2): 
        len_text1 = len(text1)
        len_text2 = len(text2)
        
        prevRow = range(len_text1+1)    
        curRow = [0 for _ in xrange(len_text1+1)]
        range_text1 = range(1, len_text1+1)
         
        for i2 in xrange(1, len_text2+1):
            c2 = text2[i2-1]
            curRow[0] = i2
            for i1 in range_text1:
                c1 = text1[i1-1]
                cost = (c1 != c2)
                curRow[i1] = min(
                    prevRow[i1  ],  #// deletion
                    curRow[i1-1],  #// insertion
                    prevRow[i1-1]   #// substitution
                    ) + cost
            prevRow, curRow = curRow, prevRow
        dist = prevRow[-1]
        return float(dist) / max(len_text1, len_text2)

if __name__ == "__main__":
    module = Module_levenshtein(None)
    for couple in (('niche', 'chiens'), ('chien', 'chiens'), ('chien', 'chat')):
        print couple, '->', module.processText(*couple)
 
