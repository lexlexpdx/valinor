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
        if not isinstance(val, list):
            raise Exception(f"[Stmt2] Indexing requires a range, got {val}")
        if not isinstance(idx, int):
            raise Exception(f"[Stmt2] Index must be an integer, got {idx}")
        return val[idx]

    def rng(self, lo_exp, hi_exp):
        lo = self.visit(lo_exp)
        hi = self.visit(hi_exp)
        return list(range(lo, hi))

    def assign(self, id, expr):
        val = self.visit(expr)
        self.env.update(str(id), val)

<<<<<<< HEAD:school/cs358/assignments/assign3/stmt2.py
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
=======
    def block(self, first, *rest):
        self.env.push_scope()
        try:
            self.visit(first)
            for stmt in rest:
                self.visit(stmt)
        finally:
            self.env.pop_scope()
            
    def prstmt(self, val):
        print(self.visit(val))

    def add(self, left, right) -> int:
        xv = self.visit(left)
        yv = self.visit(right)
        if not isinstance(xv, int) or not isinstance(yv, int):
            raise Exception(f"[Stmt2] Arith op expects int operands, got {xv} and {yv}")
        return xv + yv

    def sub(self, left, right) -> int:
        xv = self.visit(left)
        yv = self.visit(right)
        if not isinstance(xv, int) or not isinstance(yv, int):
            raise Exception(f"[Stmt2] Arith op expects int operands, got {xv} and {yv}")
        return xv - yv

    def mul(self, left, right) -> int:
        xv = self.visit(left)
        yv = self.visit(right)
        if not isinstance(xv, int) or not isinstance(yv, int):
            raise Exception(f"[Stmt2] Arith op expects int operands, got {xv} and {yv}")
        return xv * yv

    def div(self, left, right) -> int:
        xv = self.visit(left)
        yv = self.visit(right)
        if not isinstance(xv, int) or not isinstance(yv, int):
            raise Exception(f"[Stmt2] Arith op expects int operands, got {xv} and {yv}")
        return xv // yv

    def less(self, left, right):
        xv = self.visit(left)
        yv = self.visit(right)
        if not isinstance(xv, int) or not isinstance(yv, int):
            raise Exception(f"[Stmt2] Relational op requires integer operands, got {xv} {yv}")
        if xv < yv:
            return 1
        else:
            return 0
>>>>>>> a4733db619dfac6bd99e30834f9282903c553d35:school/archived_classes/cs358/assignments/assign3/stmt2.py

    def equal(self, left, right):
        xv = self.visit(left)
        yv = self.visit(right)
        if not isinstance(xv, int) or not isinstance(yv, int):
            raise Exception(f"[Stmt2] Equality op requires integer operands, got {xv} {yv}")
        if xv == yv:
            return 1
        else:
            return 0

    def ifstmt(self, cond, s1, s2 = None):
        if self.visit(cond):
            self.visit(s1)
        elif s2 is not None:
            self.visit(s2)

    def whstmt(self, cond, s1):
        while True:
            val = self.visit(cond)
            if val == 0 or (isinstance(val, list) and len(val) == 0):
                break
            self.visit(s1)

    def forlp(self, id, rng_expr, body):
        r = self.visit(rng_expr)
        if not isinstance(r, list):
            raise Exception(f"Expected range in for loop, got {r}")
        
        lo, hi = r[0], r[-1] + 1
        
        self.env.push_scope()
        try:
            self.env.extend(str(id), lo)
        
            while self.env.lookup(str(id)) < hi:
                self.visit(body)
                self.env.update(str(id), self.env.lookup(str(id)) + 1)
        finally:
            self.env.pop_scope()
        
# A new input routine - sys.stdin.read() 
# - It allows source program be written in multiple lines
#
import sys
def main():

    env = Env()

    try:
        prog = sys.stdin.read()
        tree = parser.parse(prog)
        print(prog)
        Eval(env).visit(tree)
        # print(env.lookup('x'))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

