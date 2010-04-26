import distance
from StringMatcher import StringMatcher

class Module_jaro(distance.Distance):
    def process(self, seg1, seg2):
        text1 = seg1.getContent() 
        text2 = seg2.getContent() 
        return self.processText(text1, text2)

    def processText(self, text1, text2):
      len_text1 = len(text1)
      len_text2 = len(text2)
      String_test = StringMatcher()
      String_test.set_seqs(text1,text2)
      return 1 - String_test.jaro()
      return float(dist) / max(len_text1, len_text2)

if __name__ == "__main__":
    module = Module_jaro(None)
    for couple in (('thorkel', 'thorgier'), ('chien', 'chien'), ('chien', 'chat')):
        print couple, '->', module.processText(*couple)
 
