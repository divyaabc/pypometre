DEBUG=   -g
OPT= -O3 -march=native -DNDEBUG -fopenmp 
LDFLAGS= 
CFLAGS=  -W -Wall $(DEBUG) $(OPT) -fPIC