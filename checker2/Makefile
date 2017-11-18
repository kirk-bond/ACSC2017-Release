CC=gcc
CFLAGS=-m32 -Wall -Werror

all: checker

checker: checker.c harder.h
	$(CC) $(CFLAGS) -o $@ $^
	strip $@

harder.h: harder.s
	./assemble.py $< > $@

clean:
	$(RM) checker harder.h
