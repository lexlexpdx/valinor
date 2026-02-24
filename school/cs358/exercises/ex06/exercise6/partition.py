'''
 # @ Author: Lex Albrandt
 # @ Create Time: 2026-02-23 16:41:50
 # @ Modified by: Lex Albrandt
 # @ Modified time: 2026-02-23 17:14:03
 # @ Description: CS 358 Exercise 06
 '''


#------------------------------------------------------------------------------ 
# For CS358 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

# distribute list elements into four sublists based on their types
def partition(lst):
    il = []
    fl = []
    sl = []
    ol = []
    for i in lst:
        ty = type(i)
        if   ty == int:   il.append(i); 
        elif ty == float: fl.append(i); 
        elif ty == str:   sl.append(i); 
        else:             ol.append(i); 
    return (il, fl, sl, ol)

# version 2: use 'match-case' instead of 'if-else'
def partition2(lst):
    il = []
    fl = []
    sl = []
    ol = []

    for element in lst:
        match element:
            case int():
                il.append(element)
            case float():
                fl.append(element)
            case str():
                sl.append(element)
            case _:
                ol.append(element)

    return (il, fl, sl, ol)
    
if __name__ == "__main__":
    mylst = [1,2.2,"3","four",{5,6},[7],(8,9),10]
    il,fl,sl,ol = partition(mylst)
    print("int:  ", il)            
    print("float:", fl)    
    print("str:  ", sl)            
    print("other:", ol)            
    il,fl,sl,ol = partition2(mylst)
    print("int:  ", il)            
    print("float:", fl)    
    print("str:  ", sl)            
    print("other:", ol)            
