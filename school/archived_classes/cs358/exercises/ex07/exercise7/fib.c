//------------------------------------------------------------------------------ 
// For CS358 Principles of Programming Languages, Portland State University (JL)
//------------------------------------------------------------------------------ 
#include <stdlib.h>
#include <stdio.h>

long fib(int n) {
  if (n <= 2) 
    return 1;
  else return fib(n-1) + fib(n-2);
}

int main(int argc, char **argv) {
  int n;
  if (argc < 2) {
    printf ("Usage : fib n\n");
    exit(0);
  }
  n = atoi(argv[1]);
  printf("fib(%d) = %ld\n", n, fib(n));
}
