class Distance:
    def __init__(self, context):
        self._context = context
        self.analyse()

    def analyse(self):
        pass

    def __call__(self, seg1, seg2):
        #self.preprocess(document)
        return self.process(seg1, seg2)
        #self.postprocess(document)
        #return document

    #def preprocess(self, document):
    #    print " + Filter :",  document
    #    self._t0 = time.time()

    def process(self, seg1, seg2):
        raise NotImplementedError()

    #def postprocess(self, document):
    #    print " - Filter :",  document
    #    print "   Duration(s) : %.2f"% time.time() - self.t0

