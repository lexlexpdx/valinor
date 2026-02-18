# Lex Albrandt
# CS358
# Exercise 5

# LetEx2 - a let expression language with range construct
#
#  expr0 -> "let" ID "=" expr0 "in" expr0
#        |  expr
#
#  expr  -> expr "+" term
#        |  expr "-" term
#        |  term         
#
#  term  -> term "*" atom
#        |  term "/" atom
#        |  atom
#
#  atom  -> "(" expr0 ")"
#        |  "range" "(" expr "," expr ")"
#        |  atom "[" expr "]"
#        |  ID           
#        |  NUM          
#
from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
  ?start: expr0

  ?expr0: "let" ID "=" expr0 "in" expr0 -> let
       | expr

  ?expr: expr "+" term  -> add
       | expr "-" term  -> sub
       | term         

  ?term: term "*" atom  -> mul
       | term "/" atom  -> div
       | atom

  ?atom: "(" expr0 ")"
       | "range" "(" expr "," expr ")" -> rng
       | atom "[" expr "]" -> idx
       | ID             -> var
       | NUM            -> num
 
  %import common.WORD   -> ID
  %import common.INT    -> NUM
  %import common.WS
  %ignore WS
"""

parser = Lark(grammar)

# Variable environment
#
class Env(dict):
    def extend(self,x,v):
        if x in self: 
            self[x].insert(0,v)
        else:
            self[x] = [v]
    def lookup(self,x): 
        vals = super().get(x)
        if not vals:
            raise Exception("Undefined variable: " + x)
        return vals[0]
    def retract(self,x):
        assert x in self, "Undefined variable: " + x
        self[x].pop(0)


# Interpreter
#
@v_args(inline=True)
class Eval(Interpreter):
    def __init__(self, env):
        super().__init__()
        self.env = env
    def num(self, val):  return int(val)
    def add(self, x, y): return self.visit(x) + self.visit(y)
    def sub(self, x, y): return self.visit(x) - self.visit(y)
    def mul(self, x, y): return self.visit(x) * self.visit(y)
    def div(self, x, y): return self.visit(x) // self.visit(y)

    def var(self, val):
        return self.env.lookup(str(val))

    def let(self, x, exp, body):
        
        # get the variable name which is parsed ID from Lark
        name = str(x)

        # Evaluate the initializer expression. Computes value that will
        # be bound to name
        val = self.visit(exp)

        # Push new binding into the envrionment
        self.env.extend(name, val)

        try:
            # Evaluate using extended environment
            return self.visit(body)
        
        # Always remove the temporary binding
        finally:
            self.env.retract(name)

    def rng(self, a, b):
        low = self.visit(a)
        high = self.visit(b)
        return list(range(low, high))

    def idx(self, atom, exp):
        seq = self.visit(atom)
        i = self.visit(exp)
        return seq[i]


def main():
    env = Env()
    while True:
        try:
            expr = input("Enter a let expr: ")
            tree = parser.parse(expr)
            print(expr)
            print(tree.pretty(), end="")
            print("tree.Eval() =", Eval(env).visit(tree))
            print()
        except EOFError:
            break
        except Exception as e:
            print("***", e)

if __name__ == '__main__':
    main()
