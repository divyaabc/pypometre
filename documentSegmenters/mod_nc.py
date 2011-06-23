import segmenter

class Module_nc(segmenter.Segmenter_RegExp):
    def getRegExp(self):
      return '.{' + str(self._context["segmenter_n"]) + '}'

