import segmenter

class Module_all(segmenter.Segmenter):
    def process(self, document):
        text = document.getContent()
        
#        text = unicode(text,'utf-8')
        len_text = len(text)
        document.addSegment(0, len_text)
