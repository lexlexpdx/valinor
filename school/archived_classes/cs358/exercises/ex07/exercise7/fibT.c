//------------------------------------------------------------------------------ 
// For CS358 Principles of Programming Languages, Portland State University (JL)
//------------------------------------------------------------------------------ 
#include <stdlib.h>
#include <stdio.h>

long fibT(int n) {
  long helper(int n, long a, long b) {
    if (n <= 2) 
      return a;
    return helper(n-1, a+b, a);
  }
  return helper(n, 1, 1);
}

int main(int argc, char **argv) {
  int n;
  if (argc < 2) {
    printf ("Usage : fibT n\n");
    exit(0);
  }
  n = atoi(argv[1]);
  printf("fibT(%d) = %ld\n", n, fibT(n));
}
