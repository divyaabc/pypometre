import distance

class Module_equals(distance.Distance):
    def process(self, seg1, seg2):
        text1 = seg1.getContent() 
        text2 = seg2.getContent() 
        return float(int(text1 != text2))
 
