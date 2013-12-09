import filter

class Module_w(filter.Filter_RegExp):
   def getRegExp(self):
     return '\r\n'

   def getNewValue(self):
     return '\n' 
