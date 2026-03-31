# Lex Albrandt
# CS358
# Assignment 4
#

# CS358 Fall'25 Assignment 4 (Part 2)

# Stmt3 - an imperative language with functions
#
#   stmt -> "var" ID "=" expr
#         | ID "=" expr 
#         | "if" "(" expr ")" stmt ["else" stmt]
#         | "while" "(" expr ")" stmt
#         | "print" "(" expr ")"
#         | "{" stmt (";" stmt)* "}" 
#         | "def" ID "(" ID ")" ":" body    
#         | ID "(" expr ")"
#
#   body -> "{" (stmt ";")* "return" expr "}"
#         | "return" expr
#
#   expr -> aexpr "<"  aexpr
#         | aexpr "==" aexpr
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
#         | ID "(" expr ")"
#         | ID
#         | NUM
#
from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
  ?start: stmt

   stmt: "var" ID "=" expr            -> decl
       | ID "=" expr                  -> assign
       | "if" "(" expr ")" stmt ["else" stmt] -> ifstmt
       | "while" "(" expr ")" stmt    -> whstmt
       | "print" "(" expr ")"         -> prstmt
       | "{" stmt (";" stmt)* "}"     -> block      
       | "def" ID "(" ID ")" ":" body -> fdef
       | ID "(" expr ")"              -> call

   body: "{" (stmt ";")* "return" expr "}" -> body
       | "return" expr                -> sbody

  ?expr: aexpr "<"  aexpr  -> less
       | aexpr "==" aexpr  -> equal
       | aexpr 

  ?aexpr: aexpr "+" term  -> add
       |  aexpr "-" term  -> sub
       |  term         

  ?term: term "*" atom  -> mul
       | term "/" atom  -> div
       | atom

  ?atom: "(" expr ")"
       | ID "(" expr ")"  -> call
       | ID               -> var
       | NUM              -> num

  COMMENT: "#" /[^\\n]*/ "\\n"
  %import common.WORD   -> ID
  %import common.INT    -> NUM
  %import common.WS
  %ignore COMMENT
  %ignore WS
"""

parser = Lark(grammar, parser='lalr')

# Variable environment
#
class Env():
    
    def __init__(self, scopes = None):
        if scopes is not None:
            self.scopes = scopes
        else:
            self.scopes = [{}]
        
    def extend(self, x, v):
        if x in self.scopes[-1]:
            raise Exception(f"Variable {x} is alread defined")
        else:
            self.scopes[-1][x] = v

    def lookup(self, x):
        for scope in reversed(self.scopes):
            if x in scope:
                return scope[x]
        raise Exception(f"Variable {x} is undefined")
    
    def update(self, x, v):
        for scope in reversed(self.scopes):
            if x in scope:
                scope[x] = v
                return
        raise Exception(f"Variable {x} is undefined")

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    def copy(self):
        return Env([scope.copy() for scope in self.scopes])
    

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

    def var(self, var):
        return self.env.lookup(str(var))

    def decl(self, id, expr):
        v = self.visit(expr)
        self.env.extend(str(id), v)

    def assign(self, id, expr):
        val = self.visit(expr)
        self.env.update(str(id), val)

    def block(self, first, *rest):
        self.env.push_scope()
        try:
            self.visit(first)
            for stmt in rest:
                self.visit(stmt)
        finally:
            self.env.pop_scope()

    def fdef(self, name, x, body):
        saved_env = self.env.copy()
        clos =  Closure(str(x), body, saved_env)
        saved_env.extend(str(name), clos)
        self.env.extend(str(name), clos)

    def sbody(self, expr):
        return self.visit(expr)

    def body(self, *items):
        *stmts, ret_expr = items
        
        self.env.push_scope()
        try:
            for stmt in stmts:
                self.visit(stmt) 
            return self.visit(ret_expr)
        finally:
            self.env.pop_scope()

    def call(self, f, arg):
        clos = self.env.lookup(str(f))
        if not isinstance(clos, Closure):
            raise Exception(f"{f} is not a function")
        
        argv = self.visit(arg)

        caller_env = self.env
        self.env = clos.env.copy()
        
        try:
            self.env.push_scope()
            self.env.extend(clos.id, argv)
            return self.visit(clos.body)
        finally:
            self.env.pop_scope()
            self.env = caller_env

    def add(self, left, right) -> int:
        return self.visit(left) + self.visit(right)

    def sub(self, left, right) -> int:
        return self.visit(left) - self.visit(right)

    def mul(self, left, right) -> int:
        return self.visit(left) * self.visit(right)

    def div(self, left, right) -> int:
        return self.visit(left) / self.visit(right)

    def less(self, left, right):
        return 1 if self.visit(left) < self.visit(right) else 0

    def equal(self, left, right):
        return 1 if self.visit(left) == self.visit(right) else 0

    def prstmt(self, val):
        print(self.visit(val))

    def ifstmt(self, cond, s1, s2 = None):
        if self.visit(cond):
            self.visit(s1)
        elif s2 is not None:
            self.visit(s2)

    def whstmt(self, cond, s1):
        while self.visit(cond):
            self.visit(s1)

import sys
def main():
    env = Env()
    try:
        prog = sys.stdin.read()
        tree = parser.parse(prog)
        print(prog)
        Eval(env).visit(tree)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
