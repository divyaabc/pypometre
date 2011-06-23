import segmenter

class Module_a(segmenter.Segmenter):
    def process(self, document):
        text = document.getContent()
        document.addSegment(0, len(text))
