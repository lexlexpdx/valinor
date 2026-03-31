# Lex Albrandt
# CS358
# Assignment 4
#

# CS358 Fall'25 Assignment 4 (Part 1)

# FunEx - an expression language with lambda functions
#
#   expr0 -> "let" ID "=" expr0 "in" expr0
#          | expr
#
#   expr -> "lambda" ID ":" expr 
#         | expr "(" expr ")"    
#         | aexpr 
#
#   aexpr -> aexpr "+" term
#          | aexpr "-" term
#          | term         
#
#   term -> term "*" atom
#         | term "/" atom
#         | atom
#
#   atom -> "(" expr ")"
#         | ID
#         | NUM
#
from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
  ?start: expr0

  ?expr0: "let" ID "=" expr0 "in" expr0 -> let
       | expr

  ?expr: "lambda" ID ":" expr -> func
       | expr "(" expr ")"    -> call
       | aexpr 

  ?aexpr: aexpr "+" term  -> add
       |  aexpr "-" term  -> sub
       |  term         

  ?term: term "*" atom  -> mul
       | term "/" atom  -> div
       | atom

  ?atom: "(" expr0 ")"
       | ID             -> var
       | NUM            -> num
 
  %import common.WORD   -> ID
  %import common.INT    -> NUM
  %import common.WS
  %ignore WS
"""

parser = Lark(grammar, parser='lalr')

# Variable environment
#
class Env():
    
    def __init__(self, parent = None):
        # a place to store bindings
        self.bindings = {}
        # a way to access outer bindings
        self.parent = parent

    def bind(self, name, value):

        # Binds a name and a value
        self.bindings[name] = value

    def lookup(self, name):
        # look in self.bindings for name, if it exists, return the value 
        if name in self.bindings:
            return self.bindings[name]

        # looking parent's bindings, if it exists, return the value
        if self.parent is not None:
            return self.parent.lookup(name)
        
        # if binding does not exist, throw an error
        raise Exception(f"Undefined variable {name}")
            

# Closure
#
class Closure():
    def __init__(self,id,body,env):
        self.id = id
        self.body = body
        self.env = env

# Interpreter
#
@v_args(inline=True)
class Eval(Interpreter):

    def __init__(self, env):
        self.env = env
        super().__init__()

    def num(self, val):  
        return int(val)
    
    def var(self, id):
        return self.env.lookup(str(id))

    def let(self, x, exp, body):

        # evaluate the expression
        val = self.visit(exp)

        # create child environment
        child = Env(self.env)

        # body is evaluated in current environment and extended
        child.bind(str(x), val)

        return Eval(child).visit(body)

    def add(self, left, right) -> int:
        return self.visit(left) + self.visit(right)

    def sub(self, left, right) -> int:
        return self.visit(left) - self.visit(right)

    def mul(self, left, right) -> int:
        return self.visit(left) * self.visit(right)

    def div(self, left, right) -> int:
        return self.visit(left) / self.visit(right)

    def func(self, x, body):
        return Closure(str(x), body, self.env)

    def call(self, f, arg):
        # evaluate f to a closure
        clos = self.visit(f)

        argv = self.visit(arg)

        call_env = Env(clos.env)
        call_env.bind(clos.id, argv)

        return Eval(call_env).visit(clos.body)

import sys
def main():
    env = Env()
    
    try:
        prog = sys.stdin.read()
        tree = parser.parse(prog)
        print(prog)
        print(Eval(env).visit(tree))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
