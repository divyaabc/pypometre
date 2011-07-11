class DistanceFilter:
  def __init__(self, context):
    self._context = context
    self.analyse()

  def analyse(self):
    pass

  def __call__(self,matrix):
    return self.process(matrix)

  def process(self,matrix):
    raise NotImplementedError()

