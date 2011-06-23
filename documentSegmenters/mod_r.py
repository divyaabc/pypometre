import random

class Module_r:

    def __init__(self, context):
      self._context = context

    def __call__(self, document):
      self.process(document)
      return document

    def process(self,document):
      # On recupere le contenu
      text= document.getContent()
      start= 0
      end= len(text)

      # Tant qu'il reste du texte, on decoupe:
      segmentLength= self.makeRandom()
      while end - start >= segmentLength:
        document.addSegment(start,segmentLength)
        start += segmentLength
        segmentLength= self.makeRandom()
      # Et le reste pour le dernier segment
      document.addSegment(start, end-start)

    def makeRandom(self):
      # le nb fixe + le nb aleatoire:
      return self._context["nchar_const"] + random.randrange(0, self._context["nchar_var"], 1)
