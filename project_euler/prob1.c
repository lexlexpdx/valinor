#include <stdio.h>
#include <stdlib.h>


#define MAX 1000


// Iterative solution
int sum_below(int arr[])
{
    int sum = 0;

    for (int i = 0; i < 1000; i++)
    {
        if (i % 3 == 0 || i % 5 == 0)
        {
            sum += i;
        }
    }
   return sum; 
} 


// Recursive solution with memoization
int sum_below_rec(int memo[], int n)
{
    if (memo[n] != -1)
        return memo[n];
        
    if (n == 0)
        return 0;

    if (n % 3 == 0 || n % 5 == 0)
    {
        memo[n] = n;
        return n + sum_below_rec(memo, n - 1);
    }
    memo[n] = n;
    return sum_below_rec(memo, n - 1);
}


// Tabular solution
int sum_tab(int dp[], int n)
{
    dp[0] = 0;

    for (int i = 1; i <= n; i++)
    {
        dp[i] = dp[i - 1];
        if (i % 3 == 0 || i % 5 == 0)
        {
            dp[i] = i + dp[i - 1];
        }

    }
    return dp[n];
}




int main()
{
    int dp_array[MAX] = {0};
    int memo[MAX];

    for (int i = 0; i < MAX; i++)
    {
        memo[i] = -1;
    }

    int result = sum_tab(dp_array, MAX - 1);
    printf("sum tab = %d\n\n", result);
    int result_memo = sum_below_rec(memo, MAX - 1);
    printf("sum memo = %d \n", result_memo);
    

    return 0;
}