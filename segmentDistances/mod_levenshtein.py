import distance

class Module_levenshtein(distance.Distance):
    def process(self, seg1, seg2):
        text1 = seg1.getContent() 
        text2 = seg2.getContent() 
        return self.processText(text1, text2)

    def processText(self, text1, text2): 
        len_text1 = len(text1)
        len_text2 = len(text2)
        
        d = [[0 for _ in xrange(len_text1+1)] for _ in xrange(len_text2+1)]
        
        d[0] = range(len_text1+1)    
        
        for i in xrange(len_text2+1):
            d[i][0] = i    

        for i2 in xrange(1, len_text2+1):
            c2 = text2[i2-1]
            prevRow = d[i2-1]
            curRow = d[i2]
            for i1 in xrange(1, len_text1+1):
                c1 = text1[i1-1]
                cost = (c1 != c2)
                curRow[i1] = min(
                    prevRow[i1  ],  #// deletion
                    curRow[i1-1],  #// insertion
                    prevRow[i1-1]   #// substitution
                    ) + cost
        dist = d[-1][-1]
        return float(dist) / max(len_text1, len_text2)

if __name__ == "__main__":
    module = Module_levenshtein(None)
    for couple in (('niche', 'chiens'), ('chien', 'chiens'), ('chien', 'chat')):
        print couple, '->', module.processText(*couple)
 
