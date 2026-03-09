#------------------------------------------------------------------------------ 
# For CS358 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

class A:
    def __init__(self,x): 
        self.x = x
        print('init A')

class B1(A):
    def __init__(self,x): 
        print('init B1')
        self.y = x
        super().__init__(x+1)
    pass

class B2(A):
    def __init__(self,x): 
        print('init B2')
        self.z = x
        super().__init__(x+1)
    pass

class C(B1,B2):
    def __init__(self,x): 
        print('init C')
        self.w = x
        super().__init__(x+1)
    pass

if __name__ == "__main__":
    c = C(1)
    print(c.x)
    print(c.y)
    print(c.z)
    print(c.w)

# Question c)
# I predicted:
# Init C
# Init B1
# Init B2
# Init A
# 4
# 2
# 3
# 1
# This order was correct when it printed.