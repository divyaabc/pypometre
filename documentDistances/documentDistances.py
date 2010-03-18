class Distance:
    def __init__(self, context):
        self._context = context
        self.analyse()

    def analyse(self):
        pass

    def __call__(self, matrix):
        #self.preprocess(document)
        return self.process(matrix)
        #self.postprocess(document)
        #return document

    #def preprocess(self, document):
    #    print " + Filter :",  document
    #    self._t0 = time.time()

    def process(self, seg1, seg2):
        raise NotImplementedError()

