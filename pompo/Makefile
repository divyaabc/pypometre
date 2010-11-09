BIN=pompo
LIB=libpompo.so
LIBS= -ldl -fopenmp -lpng 

include makefile.inc

SRC=pompo.c
LIBPOMPO_SRC=file.c segment.c matrix.c profile.c  module.c

LIBPOMPO_OBJ=$(patsubst %.c, %.o, $(LIBPOMPO_SRC))

MAKEDEPEND = gcc -MM $(INCLUDES) -MT $*.o -o $*.d $<
DEPFILES = $(patsubst %.c, %.d, $(SRC)) 

all: $(DEPFILES) $(LIB) modules $(BIN)

%.d : %.c
	@$(MAKEDEPEND)

-include $(DEPFILES)

$(LIB): $(LIBPOMPO_OBJ)
	$(CC) $(LDFLAGS) -o $(LIB) $(LIBS) $(LIBPOMPO_OBJ) -shared -fPIC

modules:
	$(MAKE) -C distances
	$(MAKE) -C prefilters
	$(MAKE) -C segmenters
	$(MAKE) -C docdist

modules-clean:
	$(MAKE) -C distances clean
	$(MAKE) -C prefilters clean
	$(MAKE) -C segmenters clean
	$(MAKE) -C docdist clean

$(BIN): pompo.o $(LIB)
	$(CC) pompo.o -o $(BIN) $(OBJ) $(LIBS) -lpompo -L.

clean: modules-clean
	rm -rf $(LIBPOMPO_OBJ) $(OBJ) $(DEPFILES) *~ $(BIN) $(LIB)


