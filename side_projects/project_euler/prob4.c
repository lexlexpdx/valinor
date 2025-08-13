#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int reverse_number(int num)
{
    int rev = 0;

    while (num > 0)
    {
        rev = rev * 10 + num % 10;
        num = num / 10;
    }

    return rev;
}

int palindrome()
{
    int largest_pal = 0;
    int product = 0;
    int rev_product = 0;
    
    for (int i = 100; i < 1000; i++)
    {
        for (int j = 100; j < 1000; j++)
        {
            product = i * j;
            rev_product = reverse_number(product);
            if (rev_product == product)
            {
                if (product > largest_pal)
                    largest_pal = product;
            }

        }
    }
    return largest_pal;
}


int main()
{
    int result = palindrome();
    printf("result = %d\n", result);

    return 0;
}