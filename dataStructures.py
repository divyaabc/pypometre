import array
import UserList
import numpy
import subprocess
import re

class LazyLine:
    def __init__(self, theArray, length, offset):
        self._array = theArray
        self._length = length
        self._offset = offset

    def __getitem__(self, column):
        return self._array[self._offset + column]

    def __setitem__(self, column, value):
        self._array[self._offset + column] = value
    
    def __len__(self):
        return self._length


class DistMatrix(UserList.UserList):
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self.data = [[0.0 for _ in xrange(self._width)] 
                             for _ in xrange(self._height)
                     ]
#        init = (0.0 for _ in xrange(self._width*self._height))
#        self._array = array.array("f", init)

    def set(self, x, y, value):
        assert( 0 <= x < self._width)
        assert( 0 <= y < self._height)
        self.data[y][x] = value
#        self._array[y * self._width + x] = value

    def get(self, x, y):
        assert( 0 <= x < self._width)
        assert( 0 <= y < self._height)
        return self.data[y][x] 
#        return self._array[y * self._width + x]

    def convert2numpy(self) :
      matrix2 = []
      for line in self.data :
        matrix2.append(list(line))
      a = numpy.array(matrix2,"float32") 
      return a

#    def __getitem__(self, line):
#        return LazyLine(self._array, self._width, line*self._width)

#    def __len__(self):
#        return self._height

class Document:
    def __init__(self, fileName):
        self._fileName = fileName
        self._segmentation = []
        content = open(fileName).read()
#        print str(self)
        f = subprocess.Popen(['file','-b','-i',fileName], stdout=subprocess.PIPE)
        stdout, stderr = f.communicate()
        charset = stdout.split("=")[-1].strip()
#        print charset

        if re.search('unknown',charset) :
          content_unicode = unicode(content,"iso-8859-1")
        elif re.search('ascii',charset) :
          content_unicode = unicode(content,"ascii")
        else :
          content_unicode = unicode(content,charset)

        self._content = content_unicode.encode('utf-8','replace')

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
        res  = self._fileName + "\n"
        res += self._content + "\n"
        if self._segmentation != None :
          for cpt,segment in enumerate(self._segmentation) :
            res += str(cpt)+":  "+str(segment) + "\n"

        return res

    def __repr__(self):
        return "Document(%s)"%self._fileName

    def initSegmentation(self):
        self._segmentation = Segmentation()

    def addSegment(self, start, length):
        self._segmentation.append(Segment(self, start, length))

    def getSegmentation(self):
        return self._segmentation

class Segmentation(UserList.UserList):
    pass

class Segment:
    def __init__(self, document, offset, length):
        self._document = document
        self._offset = offset
        self._length = length

    def __str__(self) :
      return "[" + self.getContent() + "]"

    def getContent(self):
        #text = self._document.getFilteredContent()
        text = self._document.getContent()
        return text[self._offset:self._offset+self._length]

