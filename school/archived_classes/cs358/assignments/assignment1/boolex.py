# Lex Albrandt
#

# CS358 Winter'26 Assignment 1 (Part 1)
#
# BoolEx - a Boolean expression language
#

from lark import Lark, v_args
from lark.visitors import Interpreter

# 0. Grammar
#
# (a) port BoolEx's grammar here
# (b) attach AST nodes: andop, orop, notop, truev, falsev
#

grammar = """
?start: orex
?orex: orex "or" andex      -> orop
    | andex
?andex: andex "and" notex    -> andop
    | notex
?notex: "not" notex         -> notop
    | atom
?atom : "(" orex ")"
    | "True"                -> truev
    | "False"               -> falsev
%ignore " "
"""

# 1. Parser
#
# It should return an AST.
#
# E.g. For input "(True or not False) and True",
#      the AST should look like:
#          andop  
#            orop
#              truev
#              notop
#                falsev
#            truev
#
parser = Lark(grammar)

# 2. Interpreter
#
# Evaluate an AST to a Boolean value.
#
# E.g. Evaluating the above AST should result in True
#
@v_args(inline=True)
class Eval(Interpreter):

    def truev(self) -> bool:
        return True

    def falsev(self) -> bool:
        return False

    def notop(self, val):
        return not self.visit(val)

    def andop(self, left, right):
        return self.visit(left) and self.visit(right)

    def orop(self, left, right):
        return self.visit(left) or self.visit(right)


# 3. Convert the AST to a prefix form
#
# E.g. Converting the above AST should return 
#      and or True not False True
#
@v_args(inline=True)
class toPrefix(Interpreter):

    def truev(self) -> str:
        return "True"

    def falsev(self) -> str:
        return "False"

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


def main():
    while True:
        try:
            expr = input("Enter a bool expr: ")
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
