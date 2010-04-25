import filter

class Module_s(filter.Filter_RegExp):
    def getRegExp(self):
        return "[\t ]+"

    def getNewValue(self):
        return "" 

