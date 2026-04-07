# Lex Albrandt
#

# CS358 Winter'26 Assignment 1 (Part 2)
#
# MixEx - a Mixed expression language
#

from lark import Lark, v_args
from lark.visitors import Interpreter

# 0. Grammar
#
# Merge grammars from arithex.py (Exercise 2) and boolex.py;
# you need to figure out the ordering of the grammar rules
# based on operator precedence
#
grammar = """
?start: orex
?orex: orex "or" andex          -> orop
    | andex
?andex: andex "and" notex       -> andop
    | notex
?notex: "not" notex             -> notop
    | expr
?expr: expr "+" term            -> add
    | expr "-" term             -> sub
    | term
?term: term "*" atom            -> mul
    | term "/" atom             -> div
    | atom
?atom: "(" orex ")"
    | NUM                       -> num
    | "True"                    -> truev
    | "False"                   -> falsev
%import common.INT              -> NUM
%ignore " "
"""

# 1. Parser
#
# It should return an AST.
#
# E.g. For input "1 + 2 or True and 3"
#      the AST should look like:
#          orop
#            add
#              num 1
#              num 2
#            andop
#              truev
#              num 3
#
parser = Lark(grammar)

# 2. Interpreter
#
# Evaluate an AST to a Boolean value.
# E.g. Evaluating the above AST should result in 3
#
@v_args(inline=True)
class Eval(Interpreter):

    def num(self, val) -> int:
        return int(val)

    def truev(self) -> bool:
        return True
    
    def falsev(self) -> bool:
        return False

    def mul(self, left, right) -> int:
        return self.visit(left) * self.visit(right)

    def div(self, left, right) -> int:
        return self.visit(left) / self.visit(right)

    def add(self, left, right) -> int:
        return self.visit(left) + self.visit(right)

    def sub(self, left, right) -> int:
        return self.visit(left) - self.visit(right)

    def notop(self, val):
        return not self.visit(val)

    def andop(self, left, right):
        return self.visit(left) and self.visit(right)

    def orop(self, left, right):
        return self.visit(left) or self.visit(right)

    


# 3. Convert the AST to a prefix form
#
# E.g. Converting the above AST should return 
#      or + 1 2 and True 3
#
@v_args(inline=True)
class toPrefix(Interpreter):
    
    def truev(self) -> str:
        return "True"

    def falsev(self) -> str:
        return "False"

    def num(self, val) -> str:
        return str(val)

    def notop(self, val) -> str:
        return f"not {self.visit(val)}"

    def andop(self, left, right) -> str:
        left_val = self.visit(left)
        right_val = self.visit(right)
        return f"and {left_val} {right_val}"

    def orop(self, left, right) -> str:
        left_val = self.visit(left)
        right_val = self.visit(right)
        return f"or {left_val} {right_val}"

    def add(self, left, right) -> int:
        left_val = self.visit(left)
        right_val = self.visit(right)
        return f"+ {left_val} {right_val}"

    def sub(self, left, right) -> int:
        left_val = self.visit(left)
        right_val = self.visit(right)
        return f"- {left_val} {right_val}"

    def mul(self, left, right) -> int:
        left_val = self.visit(left)
        right_val = self.visit(right)
        return f"* {left_val} {right_val}"

    def div(self, left, right) -> int:
        left_val = self.visit(left)
        right_val = self.visit(right)
        return f"/ {left_val} {right_val}"

def main():
    while True:
        try:
            expr = input("Enter a mixed expr: ")
            tree = parser.parse(expr)
            print(expr)
            print(tree.pretty(), end="")
            print("Eval: ", Eval().visit(tree))
            print("Prefix: ", toPrefix().visit(tree))
            print()
        except EOFError:
            break
        except Exception as e:
            print("***", e)

if __name__ == '__main__':
    main()
