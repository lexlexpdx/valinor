# Lex Albrandt
# CS358
# Assignment 2

# Imports
from lark import Lark,  v_args, Token
from lark.visitors import Interpreter
import sys

grammar = f"""
?start: stmt
?stmt: ID "=" expr -> stmt
    | "if" "(" expr ")" stmt ["else" stmt] -> if_expr
    | "while" "(" expr ")" stmt -> while_expr
    | "print" "(" expr ")" -> print
    | "{{" stmt (";" stmt)* "}}" -> block
?expr: expr "+" term -> add
    | expr "-" term -> sub
    | term
?term: term "*" atom -> mul
    | term "/" atom -> div
    | atom
?atom: "(" expr ")"
    | ID -> var
    | NUM -> num
%import common.INT -> NUM
%import common.CNAME -> ID
%ignore WS
%import common.WS
"""

class Env(dict):
    def __getitem__(self, key):
        return self.get(key, 0)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

@v_args(inline = True)
class Eval(Interpreter):

    def __init__(self, env):
        self.env = env
        super().__init__()

    def num(self, val) -> int:
        return int(val)

    def var(self, var):
        return self.env[var]

    def stmt(self, var, expr):
        value = self.visit(expr)
        self.env[var] = value

    def if_expr(self, cond, s1, s2 = None):
        if self.visit(cond):
            self.visit(s1)
        elif s2 is not None:
            self.visit(s2)

    def while_expr(self, cond, s1):
        while self.visit(cond):
            self.visit(s1)

    def print(self, val):
        print(self.visit(val))

    def block(self, first, *rest):
        self.visit(first)
        for stmt in rest:
            self.visit(stmt)
            
    def add(self, left, right) -> int:
        return self.visit(left) + self.visit(right)

    def sub(self, left, right) -> int:
        return self.visit(left) - self.visit(right)

    def mul(self, left, right) -> int:
        return self.visit(left) * self.visit(right)

    def div(self, left, right) -> int:
        return self.visit(left) / self.visit(right)

    
parser = Lark(grammar)

def main():
    prog = sys.stdin.read()
    tree = parser.parse(prog)
    Eval(Env()).visit(tree)
    
if __name__ == '__main__':
    main()