import filter



class Module_s(filter.Filter_RegExp):
    def getRegExp(self):
        print "in use"
        return "[\t ]+"

    def getNewValue(self):
        return "" 

