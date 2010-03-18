
class Presenter:
    def __init__(self, context):
        self._context = context
        self.analyse()

    def analyse(self):
        pass

    def __call__(self, documentsNames, documentsDistances):
        self.process(documentsNames, documentsDistances)

    def process(self, documentsNames, documentsDistances):
        raise NotImplementedError()
