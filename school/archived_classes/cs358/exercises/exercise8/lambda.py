# Lex Albrandt
# CS358
# Exercise 8

#------------------------------------------------------------------------------ 
# For CS320 Principles of Programming Languages, Portland State University
#------------------------------------------------------------------------------ 

class Lambda: pass

class Var(Lambda): 
    # stores variable name

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'

class Fun(Lambda):
    # stores bound variable and function body

    def __init__(self, var, func_body): 
        self.var = var
        self.func_body = func_body

    def __str__(self):
        return f'\\{self.var}.{self.func_body}'

class App(Lambda):
    # stores function expression and argument

    def __init__(self, func, arg):
        self.func = func
        self.arg = arg
    def __str__(self):
        return f'({self.func})({self.arg})'

if __name__ == "__main__":
    # x = lambda x.lambda y.x
    # y = lambda x.lambda y.xy
    # z = (lambda x.xx)y
    x = Fun("x", Fun("y", Var("x"))) 
    y = Fun("x", Fun("y", App(Var("x"), Var("y"))))
    z = App(Fun("x", App(Var("x"), Var("x"))), Var("y"))
    print('Printing x')
    print(x)  # \x.\y.x        
    print('printing y')
    print(y)  # \x.\y.(x)(y)  
    print(z)  # (\x.(x)(x))(y)