'''
 # @ Author: Lex Albrandt
 # @ Create Time: 2026-02-23 16:44:05
 # @ Modified by: Lex Albrandt
 # @ Modified time: 2026-02-23 16:44:09
 # @ Description: CS 358, exercise 6
 '''

# Part a
x = 0

def e1():
    global x
    x += 1
    return x

def e2():
    return x

def sum(e1, e2):
    return e1 + e2

result1 = sum(e1(), e2())
print(f"Result 1: {result1}")

x = 0

result2 = sum(e2(), e1())
print(f"Result 2: {result2}")


# Part b
data = []

def add_list():
    x = 1
    data.append(x)
    return len(data)

result = add_list()
print(f"List after first call: {data}, Num values in list: {result}")

result = add_list()
print(f"List second call: {data}, Num values in list: {result}")