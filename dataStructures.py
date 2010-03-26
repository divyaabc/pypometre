import array
import UserList
import chardet

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

#    def __getitem__(self, line):
#        return LazyLine(self._array, self._width, line*self._width)

#    def __len__(self):
#        return self._height

class Document:
    def __init__(self, fileName):
        self._fileName = fileName
        content = open(fileName).read()
        info  = chardet.detect(content)
        content_unicode = unicode(content,info['encoding'])
        content = content_unicode.encode('utf-8','replace')
        self._content = content
#        self._filteredContent = None
        self._segmentation = None

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
          for segment in self._segmentation :
            res += "  "+str(segment) + "\n"

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



