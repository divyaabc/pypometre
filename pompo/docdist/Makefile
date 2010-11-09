include ../makefile.inc

CPPFLAGS +=-I..
CFLAGS +=-fPIC -shared
LDFLAGS=-fPIC -shared


all: matching.so

matching.so: matching.o asp.o
	$(CC) -I.. $^ $(LDFLAGS) -o $@

%.so: %.o
	$(CC) -I.. $< $(LDFLAGS) -o $@

clean:
	rm -rf *.so *.o