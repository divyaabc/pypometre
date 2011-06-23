import distance
import zlib
import glob

class Module_i(distance.Distance):
  def process(self, seg1, seg2):
    text1 = seg1.getContent() 
    text2 = seg2.getContent() 
    return self.processText(text1, text2)

  def processText(self, text1, text2):
    t12 = text1 + text2
    c_t1  = float(len(zlib.compress(text1, zlib.Z_BEST_COMPRESSION)))
    c_t2  = float(len(zlib.compress(text2, zlib.Z_BEST_COMPRESSION)))
    c_t12 = float(len(zlib.compress(t12, zlib.Z_BEST_COMPRESSION)))

    distance =  1 - ((c_t1 + c_t2) - c_t12) / max(c_t1,c_t2)
    return distance

if __name__ == "__main__":
  module = Module_information(None)
  print module.processText("bababababa"*100, "a"*100)
 
