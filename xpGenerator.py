import glob
import random

files = ["limite_commune.shp", "troncon_route.shp"]#, "route500_lambert2.shp"]

for f in files:
    #print f, glob.glob("*.shp")
    assert (f in glob.glob("*.shp"))

options_take = ["+take_one_by_class", ""]
options_filter = ["+filter_convexhull"]

keys = ["jeanmarie", "jacques", "HHH"]

couplesKeys = [
  "%s %s"%(keys[0], keys[1]), 
  "%s %s"%(keys[0], keys[2]),
  "%s %s"%(keys[1], keys[2])
]

nbParts = ["2", "4", "8", "10", "12", "16"]

precisionLosses = ["1", "3", "5"]

nbCases = ["10 10", "6 6", "3 3"]
nbCases_mu = ["20 20"]

nbExperimentsCropping = ["4 4 20"]

all_experiments = {
  "xp_mu": (files, ('-opt',), precisionLosses, nbCases_mu),
#  "xp_codageClassCardinality": (files, nbCases),
#  "xp_correlation2":(files, "1234567890", nbParts, nbCases, ["20"], options_take),
#  "xp_repartition":(files, "1234567890", nbParts, nbCases)
}

def print_all_experiments(): 
    all_xps = []
    for name, args in all_experiments.iteritems():
        xps = [["python tatouage.5.py %s"%name]]
        for lst in args:
            new_xps = []
            for xp in xps:
                for a in lst:
                    new_xps.append(xp + [a])
            xps = new_xps
        all_xps += xps
    random.shuffle(all_xps)
    for xp in all_xps:
        print " ".join(xp)
 
print_all_experiments()
