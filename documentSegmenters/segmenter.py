import time
import dataStructures

class Segmenter:
    def __init__(self, context):
        self._context = context
        self.analyse()

    def analyse(self):
        pass

    def __call__(self, document):
        self.preprocess(document)
        self.process(document)
        self.postprocess(document)
        return document

    def preprocess(self, document):
        self._t0 = time.time()

    def process(self, document):
        raise NotImplementedError()

    def postprocess(self, document):
        pass

class Segmenter_RegExp(Segmenter):
    def process(self, document):
        import re
        text = document.getContent()
#        text = unicode(text,'utf-8')
        len_text = len(text)
#        regExp = re.compile(self.getRegExp(), re.M)
        regExp = re.compile(self.getRegExp(),re.M|re.DOTALL)
#        regExp = re.compile("t", re.M)
        start = 0
        end = len_text
        document.initSegmentation()
#        print self.getRegExp()
        for match in regExp.finditer(text):
          end = match.end()
          length = end - start
          document.addSegment(start, length) 
#          print "  [%i %i]"%(start,length)
          start = end 
        if end < len_text :
          document.addSegment(start, len_text - start)

    def getRegExp(self):
        raise NotImplementedError()

    def getNewValue(self):
        raise NotImplementedError()

