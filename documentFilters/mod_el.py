import filter

#mod_el Empty Line
class Module_el(filter.Filter_RegExp):
    def getRegExp(self):
        return "\n[\s]*\n"

    def getNewValue(self):
        return "\n"

