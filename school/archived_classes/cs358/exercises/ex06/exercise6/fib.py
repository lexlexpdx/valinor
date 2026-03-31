'''
 # @ Author: Lex Albrandt
 # @ Create Time: 2026-02-23 16:41:50
 # @ Modified by: Lex Albrandt
 # @ Modified time: 2026-02-23 17:32:16
 # @ Description: CS358 Exercise 06
 '''



# ------------------------------------------------- 
# For CS358 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

# fibonacci (recursive version)
def fib(n):
    if n < 0:  return None
    if n == 0: return 0
    if n == 1: return 1
    return fib(n-2) + fib(n-1)

# fibonacci (iterative version)
def fib2(n):
    if n < 0:  
        return None
    if n == 0: 
        return 0
    if n == 1: 
        return 1

    a = 0
    b = 1
    i = 2

    while i <= n:
        a, b = b, a + b
        i += 1

    return b

# a fibbonacci number generator
def fibgen(n):
    if n <= 0:  
        return
    yield 0
    if n == 1:
        return
    yield 1
    a = 0
    b = 1
    i = 2

    while i <= n - 1:
        next_fib = a + b
        yield next_fib
        a = b
        b = next_fib
        i += 1
        


if __name__ == "__main__":
    print("fib:  ", end='')
    for i in range(11): 
        print(fib(i), end=',')
    print("\nfib2: ", end='')
    for i in range(11):
        print(fib2(i), end=',')
    print("\nfib3: ", end='')
    for x in fibgen(11):   # loop over an iterator
        print(x, end=',')
