# Lex Albrandt
#

# CS358 Winter'26 Assignment 3
#

# Stmt2 - an extended statement language 
#
#   prog -> stmt
#
#   stmt -> ID "=" expr 
#         | "if" "(" expr ")" stmt ["else" stmt]
#         | "while" "(" expr ")" stmt
#         | "print" "(" expr ")"
#         | "{" stmt (";" stmt)* "}" 
#         | "var" ID "=" expr                // new 
#         | "for" "(" ID "in" expr ")" stmt  // new 
#
#   expr -> aexpr "<"  aexpr  // *new* 
#         | aexpr "==" aexpr  // *new* 
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
#   atom: "(" expr ")"
#         | "range" "(" expr "," expr ")"  // new
#         | atom "[" expr "]"              // new
#         | ID
#         | NUM
#
from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
  ?start: stmt

   stmt: ID "=" expr                  -> assign
       | "if" "(" expr ")" stmt ["else" stmt] -> ifstmt
       | "while" "(" expr ")" stmt    -> whstmt
       | "print" "(" expr ")"         -> prstmt
       | "{" stmt (";" stmt)* "}"     -> block      
       | "var" ID "=" expr            -> decl
       | "for" "(" ID "in" expr ")" stmt  -> forlp

  ?expr: aexpr "<"  aexpr -> less
       | aexpr "==" aexpr -> equal
       | aexpr 

  ?aexpr: aexpr "+" term  -> add
       |  aexpr "-" term  -> sub
       |  term         

  ?term: term "*" atom  -> mul
       | term "/" atom  -> div
       | atom

  ?atom: "(" expr ")"
       | "range" "(" expr "," expr ")" -> rng
       | atom "[" expr "]" -> idx
       | ID                -> var
       | NUM               -> num

  COMMENT: "#" /[^\\n]*/ "\\n"
  %import common.WORD   -> ID
  %import common.INT    -> NUM
  %import common.WS
  %ignore COMMENT
  %ignore WS
"""

# With an 'lalr' parser, Lark handles the 'dangling else' 
# case correctly.
parser = Lark(grammar, parser='lalr')

# Variable environment
#
class Env():

    def __init__(self):
        self.scopes = [{}]

    def extend(self, x, v):
        if x in self.scopes[-1]:
            raise Exception(f"Variable {x} already defined")
        else:
            self.scopes[-1][x] = v

    def lookup(self, x):
        for scope in self.scopes[::-1]:
            if x in scope:
                return scope[x]
        raise Exception(f"Variable {x} undefined")

    def update(self, x, v):
        for scope in self.scopes[::-1]:
            if x in scope:
                scope[x] = v
                return
        raise Exception(f"Variable {x} undefined")

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

        
# Interpreter
#
@v_args(inline=True)
class Eval(Interpreter):

    def __init__(self, env):
        self.env = env

    def num(self, val): 
        return int(val)

    def var(self, id):
        return self.env.lookup(str(id))

    def decl(self, id, expr):
        v = self.visit(expr)
        self.env.extend(str(id), v)

    def idx(self, obj, expr):
        val = self.visit(obj)
        idx = self.visit(expr)
        return val[idx]

    def rng(self, lo_exp, hi_exp):
        lo = self.visit(lo_exp)
        hi = self.visit(hi_exp)
        return list(range(lo, hi))

    def assign(self, id, expr):
        val = self.visit(expr)
        self.env.extend(str(id), val)

    def add(self, left, right) -> int:
        return self.visit(left) + self.visit(right)

    def sub(self, left, right) -> int:
        return self.visit(left) - self.visit(right)

    def mul(self, left, right) -> int:
        return self.visit(left) * self.visit(right)

    def div(self, left, right) -> int:
        return self.visit(left) / self.visit(right)
    
    def print(self, expr):
        print(self.visit(expr))

# A new input routine - sys.stdin.read() 
# - It allows source program be written in multiple lines
#
import sys
def main():

    env = Env()
    # Env tests

    # Test variable assignment
    # env.extend('x', 42)
    # id = env.lookup(('x'))
    # print(id)

    # # Test variable assignement when already declared
    # env.extend('x', 42)
    # env.extend('x', 43)

    # Test undefined lookup
    # env.lookup('y')

    # Test update works
    # env.update('x', 43)
    # id = env.lookup('x')
    # print(id)

    # Test undefined update
    # env.update('y', 10)

    # Test popping scope when only one scope
    # env.pop_scope()
    # print(f"{len(env.scopes)}")

    # Test adding new scope
    # env.push_scope()
    # print(f"{len(env.scopes)}")

    # Test popping scope
    # env.pop_scope()
    # print(f"{len(env.scopes)}")

    # Test extend scope
    # env.extend('x', 42)
    # env.push_scope()
    # env.extend('x', 32)
    # id = env.lookup('x')
    # print(id)
    # env.pop_scope()
    # id = env.lookup('x')
    # print(id)

    # Test update in top scope
    # env.extend('x', 10)
    # env.push_scope()
    # env.extend('y', 20)
    # env.update('y', 30)
    # print(env.lookup('y'))

    # Test update in outer scope
    # env.extend('x', 10)
    # env.push_scope()
    # env.update('x', 42)
    # print(env.lookup('x'))

    # Test undefined variable
    # env.push_scope()
    # env.update('x', 42)

    # Test shadow vs update
    # env.extend('x', 1)
    # env.push_scope()
    # env.extend('x', 2)
    # env.update('x', 42)
    # print(env.lookup('x'))

    try:
        prog = sys.stdin.read()
        tree = parser.parse(prog)
        print(prog)
        Eval(env).visit(tree)
        print(env.lookup('x'))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

