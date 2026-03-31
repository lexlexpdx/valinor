from lark import Lark

# grammar = """
# ?start: stmt
# ?stmt: "if" "expr" stmt ["else" stmt] 
#     | "other"
# %ignore " "
# """

# grammar = """
# ?start: stmt
# ?stmt: "if" "expr" stmt 
#     | "if" "expr" stmt "else" stmt
#     | "other"
# %ignore " "
# """

grammar = """
?start: stmt
?stmt: "if" "expr" stmt "else" stmt
    | "if" "expr" stmt
    | "other"
%ignore " "
"""

parser = Lark(grammar, parser='lalr')
test = 'if expr if expr other else other'
tree = parser.parse(test)
print(tree.pretty())