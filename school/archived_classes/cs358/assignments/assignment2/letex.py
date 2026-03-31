# Lex Albrandt
# CS358
# Assignment 2

# Imports
from lark import Lark,  v_args, Token
from lark.visitors import Interpreter

grammar = """
?start: expr0
?expr0: "let" ID "=" expr0 "in" expr0 -> let
    | expr
?expr: expr "+" term -> add
    | expr "-" term -> sub
    | term
?term: term "*" atom -> mul
    | term "/" atom -> div
    | atom
?atom: "(" expr0 ")"
    | ID -> var
    | NUM -> num
%import common.INT -> NUM
%import common.CNAME -> ID
%ignore " "
"""

class Env(dict):

    def extend(self, x, v):
        if x in self:
            self[x].insert(0, v)
        else:
            self[x] = [v]

    def lookup(self, x):
        vals = super().get(x)
        if not vals:
            raise Exception("Undefined Variable: " + x)
        return vals[0]

    def retract(self, x):
        assert x in self, "Undefined variable: " + x
        self[x].pop(0)


@v_args(inline = True)
class Eval(Interpreter):

    def __init__(self, env):
        self.env = env
        super().__init__()

    def num(self, val) -> int:
        return int(val)

    def var(self, val):
        return self.env.lookup(str(val))

    def let(self, x, exp, body):

        # evaluate let binding expression
       val = self.visit(exp)

       # Store binding into current environment's variable
       self.env.extend(str(x), val)

       # Evaluate let construct's body expression
       result = self.visit(body)

       # remove binding from the environment
       self.env.retract(str(x))
       
       return result

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

    # Env class test
    env = Env()
    env.extend('x', 42)
    print(env.lookup('x'))
    env.extend('x', 99)
    print(env.lookup('x'))
    env.retract('x')
    print(env.lookup('x'))
    env.retract('x')
    try:
        print(env.lookup('x'))
    except Exception as e:
        print(e)
    
    while True:
        try:
            prog = input("Enter an expr: ")
            tree = parser.parse(prog)
            print(tree.pretty())
            print("tree.Eval() = ", Eval(env).visit(tree))
            # print(f"tree.toPrefix = {toPrefix().visit(tree)}")
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")
    
if __name__ == '__main__':
    main()