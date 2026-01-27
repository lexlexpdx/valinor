# Lex Albrandt
#

# CS358 Winter'26 Assignment 1 (Part 3)
#
# RelEx - a relational expression language
#
#   relex -> relex rop atom
#         |  atom
#   atom  -> "(" relex ")"
#         |  NUM
#   rop   -> "<"|"<="|">"|">="|"=="|"!="
#
from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
?start: relex
?relex: relex rop atom  -> relop
    | atom
?atom: "(" relex ")"
    | NUM               -> num
?rop: "<"               -> lt
    | "<="              -> lteq
    | ">"               -> gt
    | ">="              -> gteq
    | "=="              -> eq
    | "!="              -> noteq

%import common.INT      -> NUM
%import common.WS
%ignore WS
"""

parser = Lark(grammar)

# An interpreter with C semantics
# - return 1 or 0
#
@v_args(inline=True)
class EvalC(Interpreter):

    def num(self, val) -> int:
        return int(val)

    def relop(self, left, op, right) -> int:
        left_val = self.visit(left)
        right_val = self.visit(right)

        if op.data == "lt":
            return 1 if left_val < right_val else 0

        elif op.data == "lteq":
            return 1 if left_val <= right_val else 0

        elif op.data == "gt":
            return 1 if left_val > right_val else 0
        
        elif op.data == "gteq":
            return 1 if left_val >= right_val else 0
        
        elif op.data == "eq":
            return 1 if left_val == right_val else 0

        elif op.data == "noteq":
            return 1 if left_val != right_val else 0
        


# An interpreter with Python semantics
# - return True or False
#
@v_args(inline=True)
class EvalP(Interpreter):

    def num(self, val) -> int:
        return int(val)

    def relop(self, left, op, right) -> int:
        left_val = self.visit(left)
        right_val = self.visit(right)

        if left.data == "relop":

            # extract middle value
            middle = self.visit(left.children[2])

            # extract left value
            left_result = self.visit(left)

            # do current comparison
            current = self.compare(middle, op, right_val)
            return left_result and current
        else:
            return self.compare(left_val, op, right_val)
            

    def compare(self, left_val, op, right_val):
        if op.data == "lt":
            return left_val < right_val
        elif op.data == "lteq":
            return left_val <= right_val
        elif op.data == "gt":
            return left_val >= right_val
        elif op.data == "gteq":
            return left_val >= right_val
        elif op.data == "eq":
            return left_val == right_val
        elif op.data == "noteq":
            return left_val != right_val


def main():
    while True:
        try:
            prog = input("Enter an expr: ")
            tree = parser.parse(prog)
            print(prog)
            print(tree.pretty(),end="")
            print("EvalC:", EvalC().visit(tree))
            print("EvalP:", EvalP().visit(tree))
            print()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
