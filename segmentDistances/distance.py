class Distance:
    def __init__(self, context):
        self._context = context
        self.analyse()

    def analyse(self):
        pass

    def __call__(self, seg1, seg2):
        res = self.process(seg1, seg2)
        return res

    def process(self, seg1, seg2):
        raise NotImplementedError()
