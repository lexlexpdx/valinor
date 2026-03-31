# Lex Albrandt
# CS358
# Exercise 8

#------------------------------------------------------------------------------ 
# For CS358 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

class A:
    def __init__(self): 
        print('init A')

class B1(A):
    def __init__(self): 
        print('init B1')
        super().__init__()

class B2(A):
    def __init__(self): 
        print('init B2')
        super().__init__()

class C(B1,B2):
    def __init__(self): 
        print('init C')
        super().__init__()

if __name__ == "__main__":
    c = C()

# Question b)
# I predicted that it would print this:
# init C
# init B1
# init A
# init B2
# init A
# 
# It only prints init A once because it goes in a linear fashion, calling
# the next class in the method resolution order

