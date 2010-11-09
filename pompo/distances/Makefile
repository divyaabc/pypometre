include ../makefile.inc

CPPFLAGS += -I..
CFLAGS += -fPIC -shared
LDFLAGS=-fPIC -shared

all: levenshtein.so hamming.so

%.so: %.o
	$(CC) -I.. $< $(LDFLAGS) -o $@

clean:
	rm -rf *.so *.o