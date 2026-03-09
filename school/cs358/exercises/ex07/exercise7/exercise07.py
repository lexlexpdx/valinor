'''
 # @ Author: Lex Albrandt
 # @ Create Time: 2026-03-02 09:31:35
 # @ Description: CS 358 Exercise 7
 '''

# Problem 1

def ave(x):
    def inner_y(y):
        def inner_z(z):
            return (x + y + z) // 3
        return inner_z
    return inner_y

print((ave(1)(2)(2)))

# Problem 2
def currying(f):
    def inner_x(x):
        def inner_y(y):
            return f(x, y)
        return inner_y
    return inner_x

def add(x, y):
    return x + y

print(currying(add)(2)(3))

# Problem 3
def ktimes(f, k):
    def inner(x):
        result = x
        for i in range(k):
            result = f(result)
        return result
    return inner

def inc(x):
    return x + 1

print(ktimes(inc, 0)(5))
    
# Problem 4
def mymap(f, itr):
    results = []
    for item in itr:
        result = f(item)
        results.append(result)
    if isinstance(itr, str):
        return ''.join(results)
    else:
        return type(itr)(results)

def inc(x):
    return x + 1

print(mymap(inc, [1, 2, 3]))
print(mymap(inc, (1, 2, 3)))
print(mymap(inc, {1, 2, 3}))
print(mymap(str.upper, 'abc'))
    
# Problem 5
# Recursion is still present in fib.s because the regular fib recursion involves two recursive calls
# which is not easily optimized into a loop, whereas in fibT.s, recursion is no longer present because the
# compiler easily optimized the tail recursion into a loop

# There is a significant difference in execution time between the fib program and the fibT progrm

