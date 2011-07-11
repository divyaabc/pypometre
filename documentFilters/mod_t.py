import filter

class Module_t(filter.Filter_RegExp):
   def getRegExp(self):
     return '[\w]+'

   def getNewValue(self):
     return 't' 
