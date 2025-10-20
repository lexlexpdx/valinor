# Lex Albrandt
# albrandt@pdx.edu
# CS333
# Lab1 Makefile
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
PERMS = og-rx

PROG1 = cae-xor
PROG2 = mystat
PROG3 = 
PROGS = $(PROG1) $(PROG2)
INCLUDES = 

all: $(PROGS)

$(PROG1): $(PROG1).o
	$(CC) $(CFLAGS) -o $@ $^

$(PROG1).o: $(PROG1).c
	$(CC) $(CFLAGS) -c $<

$(PROG2): $(PROG2).o
	$(CC) $(CFLAGS) -o $@ $^

$(PROG2).o: $(PROG2).c
	$(CC) $(CFLAGS) -c $<


# Non-build rules
.PHONY: all clean cls tar git get

# Clean
clean cls:
	rm -f $(PROGS) *.o *~ \#*

# Tarball
tar:
	tar cvfa lab1_${LOGNAME}.tar.gz *.[ch] [mM]akefile

# git revision control
git get:
	git status
	git add *.[ch] [mM]akefile
	git commit
	git push


