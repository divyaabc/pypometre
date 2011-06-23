import distance
from StringMatcher import StringMatcher

class Module_jw(distance.Distance):
  def process(self, seg1, seg2):
    text1 = seg1.getContent() 
    text2 = seg2.getContent() 
    return self.processText(text1, text2)

  def processText(self, text1, text2):
    String_test = StringMatcher()
    String_test.set_seqs(text1,text2)
    return 1 - String_test.jaro_winkler()

if __name__ == "__main__":
    module = Module_jaro_winkler(None)
    for couple in (('thorkel', 'thorgier'), ('chien', 'chien'), ('chien', 'chat')):
        print couple, '->', module.processText(*couple)
 
