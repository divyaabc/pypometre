import time
import cStringIO as StringIO

class Filter:
    def __init__(self, context):
        self._context = context
        self.analyse()
    
    def __call__(self, document):
        self.preprocess(document)
        self.process(document)
        self.postprocess(document)
        return document

    def analyse(self):
        pass

    def preprocess(self, document):
        print " + Filter :",  document
        self._t0 = time.time()

    def process(self, document):   
        raise NotImplementedError()

    def postprocess(self, document):
        print " - Filter :",  document
        print "   Duration(s) : %.2f"%(time.time() - self._t0)

class Filter_RegExp(Filter):
    def process(self, document):
        import re
        text = document.getContent()
        buff = StringIO.StringIO()   
        for c in text:   
            if ord(c) < 128:
                buff.write(c)
            else:
                buff.write("t")
        res = buff.getvalue()
        regExp = re.compile(self.getRegExp(), re.M)
        newValue = self.getNewValue()
        regExp.sub(newValue, res)
        document.setFilteredContent(res)
 
    def getRegExp(self):
        raise NotImplementedError()

    def getNewValue(self):
        raise NotImplementedError()
        


