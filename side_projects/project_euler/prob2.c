#include <stdio.h>
#include <stdlib.h>

#define MAX_FIB 4000000

int fib_even_it()
{
    int a = 1;
    int b = 1;
    int c = 0;
    int sum = 0;

    while (c < MAX_FIB)
    {
        if (b % 2 == 0)
            sum += b;
        c = a + b;
        a = b;
        b = c;
    }

    return sum;
}

int main()
{
    int result = fib_even_it();
    printf("sum = %d\n", result);

    return 0;
}