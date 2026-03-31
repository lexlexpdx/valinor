def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

def fib_tr(n):
    def help(n , acc):
        if n <= 1:
            return n + acc
        return help((n - 1), acc + n)
    return help(n, 0)
    
print(fib(6))
print(fib(6))