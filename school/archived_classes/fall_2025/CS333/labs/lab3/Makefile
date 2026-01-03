# Lex Albrandt
# albrandt@pdx.edu
# CS333
# Lab3 Makefile
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
LDFLAGS = -lcrypt
PERMS = og-rx

PROG1 = thread_hash
PROG2 = 
PROG3 = 
PROGS = $(PROG1)

all: $(PROGS)

$(PROG1): $(PROG1).o
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

$(PROG1).o: $(PROG1).c
	$(CC) $(CFLAGS) -c $<

# Non-build rules
.PHONY: all clean cls tar git get

# Clean
clean cls:
	rm -f $(PROGS) *.o *~ \#*

# Tarball
tar:
	tar cvfa lab3_${LOGNAME}.tar.gz *.[c] [mM]akefile

# git revision control
git get:
	git status
	git add *.[ch] [mM]akefile
	git commit
	git push


