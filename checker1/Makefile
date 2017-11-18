CC=gcc
CFLAGS=-m32 -Wall -Werror

all: checker

checker: checker.c simple.h
	$(CC) $(CFLAGS) -o $@ $^
	strip $@

simple.h: simple.s
	./assemble.py $< > $@

clean:
	$(RM) checker simple.h
