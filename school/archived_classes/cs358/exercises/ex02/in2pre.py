# Lex Albrandt
# CS358
# Exercise 2

# Imports
from lark import Lark,  v_args, Token
from lark.visitors import Interpreter

grammar = """
?start: infix 
?infix: infix "+" infix      -> add
    | infix "-" infix      -> sub
    | infix "*" infix      -> mul
    | infix "/" infix      -> div
    | "(" infix ")"        -> paren
    | NUM                  -> num
%import common.INT -> NUM
%ignore " "
"""

@v_args(inline = True)
class Eval(Interpreter):

    def num(self, token) -> int:
        return int(token)

    def add(self, left, right) -> int:
        return self.visit(left) + self.visit(right)

    def sub(self, left, right) -> int:
        return self.visit(left) - self.visit(right)

    def mul(self, left, right) -> int:
        return self.visit(left) * self.visit(right)

    def div(self, left, right) -> int:
        return self.visit(left) / self.visit(right)

    def paren(self, val):
        return self.visit(val)

@v_args(inline = True)
class toPrefix(Interpreter):

    def num(self, val) -> str:
        return str(val)

    def add(self, left, right) -> str:
        left_val = self.visit(left)
        right_val = self.visit(right)
        return f"+ {left_val} {right_val}"

    def sub(self, left, right) -> str:
        left_val = self.visit(left)
        right_val = self.visit(right)
        return f"- {left_val} {right_val}"

    def mul(self, left, right) -> str:
        left_val = self.visit(left)
        right_val = self.visit(right)
        return f"* {left_val} {right_val}"

    def div(self, left, right) -> str:
        left_val = self.visit(left)
        right_val = self.visit(right)
        return f"/ {left_val} {right_val}"
        
    
parser = Lark(grammar)

def main():
    
    while True:
        try:
            prog = input("Enter an expr: ")
            tree = parser.parse(prog)
            print(tree.pretty())
            print("tree.Eval() = ", Eval().visit(tree))
            print(f"tree.toPrefix() = {toPrefix().visit(tree)}")
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")
    
if __name__ == '__main__':
    main()