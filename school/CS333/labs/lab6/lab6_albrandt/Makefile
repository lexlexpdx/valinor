# Lex Albrandt
# albrandt@pdx.edu
# CS333
# Lab6 Makefile
#

CC = gcc
DEFINES = 
DEBUG = -g3 -O0
WERROR = -Wall -Wextra -Wshadow -Wunreachable-code -Wredundant-decls \
	 -Wmissing-declarations -Wold-style-definition \
	 -Wmissing-prototypes -Wdeclaration-after-statement \
	 -Wno-return-local-addr -Wunsafe-loop-optimizations \
	 -Wuninitialized -Werror
CFLAGS = $(DEBUG) $(WERROR)
LDFLAGS =
PERMS = og-rx

PROG1 = rockem_server
PROG2 = rockem_client
PROG3 = 
PROGS = $(PROG1) $(PROG2)

all: $(PROGS)

$(PROG1): $(PROG1).o
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

$(PROG1).o: $(PROG1).c
	$(CC) $(CFLAGS) -c $<

$(PROG2): $(PROG2).o
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

$(PROG2).o: $(PROG2).c
	$(CC) $(CFLAGS) -c $<

# Non-build rules
.PHONY: all clean cls tar git get

# Clean
clean cls:
	rm -f $(PROGS) *.o *~ \#*

# Tarball
tar:
	tar cvfa lab6_${LOGNAME}.tar.gz *.[c] [mM]akefile

# git revision control
git get:
	git status
	git add *.[ch] [mM]akefile
	git commit
	git push


