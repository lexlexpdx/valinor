#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define NUM 600851475143

int find_largest_factor()
{
    long long sqrt_num = sqrt(NUM);
    long long num = NUM;
    int largest = 0;

    for (int i = 2; i <= sqrt_num; i ++)
    {
        while (num % i == 0)
        {
            largest = i;
            num = num / i;
        }
    }
    if (largest > 2)
        return largest;

    else
        return 2;
}


long long large_factor_rec(long long num, int factor)
{

    if (factor >= sqrt(num))
        return num;
    
    
    if (num % factor == 0)
    {
        num = num / factor;
        if (num == 1)
            return factor;
        return large_factor_rec(num, factor + 1);
    }
    
    return large_factor_rec(num, factor + 1);
}

int main()
{
    long long number = NUM;
    int result = find_largest_factor();

    //printf("largest factor: %d", result);

    long long new_result = large_factor_rec(number, 2);
    printf("rec fact: %lld\n", new_result);

    return 0;
}