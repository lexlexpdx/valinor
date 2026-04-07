# Lex Albrandt
# CS358 
# Exercise 8

#------------------------------------------------------------------------------ 
# For CS358 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

class A:
    x = 1
    def __init__(self): 
       self.x = 2
       print('init A')

class B(A):
    def __init__(self): 
       self.x = 3
       print('init B')
    pass

if __name__ == "__main__":
    b = B()
    print(b.x)

    
# Questions
# a) 
#   i) the program prints "1"
#       This is because B inherits A's methods and class attribute,
#       and "x" is defined as a static variable in class A
#   ii) the program prints "init A\n" "2"
#       This is because class B inherits from class A, which prints from the constructor  
#       of class A and sets b.x to 2
#   iii) the program prints "init B\n" "3"
#       This is because B runs its constructor which updates b.x to 3, and we don't
#       see anything from class A's constructor because we would have to explicitly
#       call it

