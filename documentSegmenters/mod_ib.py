from iBlocs import *

class Module_ib:

    def __init__(self, context):
      self._context = context

    def __call__(self, document):
      self.process(document)
      return document

    def process(self,document):
      # On recupere le contenu
      text = document.getContent()
      # On trouve les blocs et on recupere une liste de (level, begin, stop)
      listeBlocs = trouveBlocs(text)

      # Pour chaque bloc, on fait un segment,
      # sauf bloc 0 qui est en fait tout le doc
      for b in listeBlocs:
        if b[0] == 0:
          continue
        start = b[1]
        segmentLength = b[2] - b[1]
        document.addSegment(start,segmentLength)
