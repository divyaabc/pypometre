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
            for i in (-2, -1, 0, 1, 2):
                value += weightsimplifiedMatrix.get((x+i, y+i), 1.0)
            value /= 5.0
            if value >= 0.7:
                value = 1.0
            total += 1.0 - value
#    print "+",total
    total /= len(simplifiedMatrix)
#    print len(simplifiedMatrix)
#    print "-",total
#    print "*****"
    return total 
