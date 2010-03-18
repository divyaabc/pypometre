import segmenter

class Module_newline(segmenter.Segmenter_RegExp):
    def getRegExp(self):
        return "\n"

