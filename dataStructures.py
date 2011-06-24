from array import array
import UserList
import subprocess
import re

import pprint
#import tool_numpy as tn

class LinedMatrix() :
  def __init__(self, width, height, fill_val = 0.0) :
    self._len = width*height
    self._width = width
    self._height = height
    self._min = min(width,height)
    self.data = array('f', [fill_val for _ in xrange(self._len)])

  def reinit(self, w, h) :
    self._width = w
    self._height = h
    self._len = w*h
    self._min = min(w,h)


  def i2xy(self, i) :
    assert(0 <= i < self._len)
    x = i % self._width
    y = i / self._width
    return (x,y)

  def xy2i(self, x,y) :
    assert(0 <= x < self._width)
    assert(0 <= y < self._height)
    return x + y*self._width

  def convertMatrix(self, matrix) :
    w = len(matrix[0])
    h = len(matrix)
    self.__init__(w,h)
    for y in xrange(h) :
      for x in xrange(w) :
        i = x + y*self._width
        self.data[i] = matrix[y][x]

  def convertDistMatrix(self, matrix) :
    self.__init__(len(matrix[0]),len(matrix))
    cpt = 0
    for l in matrix :
      for val in l :
        self.data[cpt] = val
        cpt += 1

  def getMatrix(self) :
    return [self.data[y*self._width:(y+1)*self._width] for y in xrange(self._height)]

  def __str__(self) :
    m = []
    for y in xrange(self._height) :
      ny = y * self._width
      l = [round(val,5) for val in self.data[ny:ny+self._width]]
      m.append(l)
    return str(m)

  def set(self, x, y, val) :
    i = self.xy2i(x,y)
    self.data[i] = val

  def get(self, x, y) :
    i = self.xy2i(x,y)
    return self.data[i]


class DistMatrix():
  def __init__(self, width, height):
    self._width = width
    self._height = height
    self.data = [[0.0 for _ in xrange(self._width)]
                      for _ in xrange(self._height)]

  def set(self, x, y, value):
#    assert( 0 <= x < self._width)
#    assert( 0 <= y < self._height)
    self.data[y][x] = value

  def get(self, x, y):
#    assert( 0 <= x < self._width)
#    assert( 0 <= y < self._height)
    return self.data[y][x] 

#  def convert2numpy(self) :
#    return tn.matrix2numpy(self)

  def __str__(self) :
    return str(self.data)

class Document:
    def __init__(self, fileName):
      self._fileName = fileName
      self._segmentation = []
      content = open(fileName).read()

      f = subprocess.Popen(['file','-b','-i',fileName], stdout=subprocess.PIPE)
      stdout, stderr = f.communicate()
      charset = stdout.split("=")[-1].strip()

      if re.search('application/octet-stream', charset) :
        content_unicode = unicode(content,"iso-8859-1")
      elif re.search('unknown',charset) :
        content_unicode = unicode(content,"iso-8859-1")
      elif re.search('ascii',charset) :
        content_unicode = unicode(content,"iso-8859-1")
      elif re.search('binary',charset) :
        content_unicode = unicode(content,"iso-8859-1")
      else :
        content_unicode = unicode(content,charset)
      self._content = content_unicode.encode('utf-8','replace')
      return 

    def getContent(self):
      return self._content

    def setSegmentation(self, segmentation):
      self._segmentation = segmentation

    def setContent(self,content) :
      self._content = content

    def setFileName(self,fileName) :
      self._fileName = fileName

    def getSegmentation(self):
      return self._segmentation

    def __str__(self):
      return self._fileName

    def str_verbose(self):
      res = '%s\n%s\n'%(self._fileName, self._content)
      if self._segmentation != None :
        for cpt,segment in enumerate(self._segmentation) :
          res += '  %d: %s\n'%(cpt,str(segment))
      return res

    def __repr__(self):
      return "Document(%s)"%self._fileName

    def initSegmentation(self):
      self._segmentation = Segmentation()

    def addSegment(self, start, length):
      self._segmentation.append(Segment(self, start, length))

    def getSegmentation(self):
      return self._segmentation

#class Segmentation(UserList.UserList):
class Segmentation(UserList.UserList):
  pass


class Segment:
  def __init__(self, document, offset, length):
    self._document = document
    self._offset = offset
    self._length = length

  def __str__(self) :
    return '[%s]'%(self.getContent())#"[" + self.getContent() + "]"

  def getContent(self):
    #text = self._document.getFilteredContent()
    text = self._document.getContent()
    return text[self._offset:self._offset+self._length]

