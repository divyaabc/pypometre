import segmenter

class Module_nchar(segmenter.Segmenter_RegExp):
    def getRegExp(self):
      return '.{' + str(self._context["segmenter_n"]) + '}'

