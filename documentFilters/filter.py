#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
#import cStringIO as StringIO

class Filter:
    def __init__(self, context):
        self._context = context
        self.analyse()
    
    def __call__(self, document):
      import copy
      document_filter = copy.copy(document)
      self.preprocess(document_filter)
      self.process(document_filter)
      self.postprocess(document_filter)
      return document_filter

    def analyse(self):
        pass

    def preprocess(self, document):
        self._t0 = time.time()

    def process(self, document):   
        raise NotImplementedError()

    def postprocess(self, document):
        pass


class Filter_RegExp(Filter):
    def process(self, document):
        import re
        text = document.getContent()
        text_unicode = unicode(text,'utf-8')
        regExp = re.compile(u''+self.getRegExp(), re.UNICODE)
        text_unicode = regExp.sub(u''+self.getNewValue(), text_unicode)
        text = text_unicode.encode('utf-8','replace')
        document.setContent(text)
 
    def getRegExp(self):
        raise NotImplementedError()

    def getNewValue(self):
        raise NotImplementedError()
