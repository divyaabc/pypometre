import segmenter

class Module_nline(segmenter.Segmenter_RegExp):
    def getRegExp(self):
      regexp = '\n'
      for _ in xrange(self._context - 1) :
        regexp += '.*\n'
      return regexp

