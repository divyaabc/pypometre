import documentDistances
import munkres

class Module_filteredMunkres(documentDistances.Distance):

    def process(self, matrix):
        m = munkres.Munkres()
        print "Starting munkres algorithm"
        indexes = m.compute(matrix)
        print "Stopping munkres algorithm"
                
        width = len(matrix)
        height = len(matrix[0])
        simplifiedMatrix = dict(((x, y), matrix[y][x]) for y, x in indexes)
        
        docDist = convolute(simplifiedMatrix, width, height)

        print docDist
        #print total
        return docDist 

def convolute(simplifiedMatrix, width, height):
    total = 0.0
    for y in xrange(height):
        for x in xrange(width):  
            value = 0.0
            for j in (-1, 0, 1):
                for i in (-1, 0, 1):
                    value += simplifiedMatrix.get((x+i, y+j), 1.0)
            value /= 9.0
            if value >= 0.7:
                value = 1.0
            total += 1.0 - value
#    print "+",total
    total /= len(simplifiedMatrix)
#    print len(simplifiedMatrix)
#    print "-",total
#    print "*****"
    return total 
