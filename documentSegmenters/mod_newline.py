import segmenter

class Module_newline(segmenter.Segmenter):
    def getRegExp(self):
        return "\n"

