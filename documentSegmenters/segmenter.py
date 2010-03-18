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
        print " + Segmentation :",  document
        self._t0 = time.time()

    def process(self, document):
        raise NotImplementedError()

    def postprocess(self, document):
        print " - Segmentation :",  document
        print "   Duration(s) : %.2f"% (time.time() - self._t0)

class Segmenter_RegExp(Segmenter):
    def process(self, document):
        import re
        text = document.getFilteredContent()
        regExp = re.compile(self.getRegExp(), re.M)
        start = 0
        document.initSegmentation()
        for match in regExp.finditer(text):
            end = match.end()
            length = end - start
            document.addSegment(start, length) 
            start = end 

    def getRegExp(self):
        raise NotImplementedError()

    def getNewValue(self):
        raise NotImplementedError()

