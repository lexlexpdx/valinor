# Lex Albrandt
# CS358
# Exercise 5

# Variable environment (new version)
#
# In this version, multiple variables may be defined in a scope, and 
# a variable's value may be updated.
#
# Idea: A seperate environment for each scope; keep all open scopes'
#       evironments in a list.
#
class Env(dict):
    prev = []   # a list for keeping previous envs

    # Push current env to the prev list, return a new empty env
    def openScope(self):
        self.prev.append(self)
        return Env()

    # Pop off the top env from the prev list, return this env
    def closeScope(self):
        if not self.prev:
            raise IndexError("Close scope: no existing scope")
        return self.prev.pop()

    # Add an entry to current env; if an entry already exists, it
    # raises an exception for trying to redefine a variable
    def extend(self,x,v): 
        if x in self:
            raise Exception(f"Cannot redefine variable {x}")
        else:
            self[x] = v
        

    # Start searching from current env, and if necessary, continue
    # with the envs in the prev list; return the first matching entry.
    # If can't find, raise an exception for undefined variable
    def lookup(self,x): 
        if x in self:
            return self[x]
        for env in reversed(self.prev):
            if x in env:
                return env[x]
        raise Exception(f"Undefined variable {x}")

    # Search to find the first matching entry. If found, update the
    # value of the entry; otherwise raise an exception for undefined
    # variable
    def update(self,x,v):
        if x in self:
            self[x] = v
            return
        for env in reversed(self.prev):
            if x in env:
                env[x] = v
                return
        raise Exception(f"Undefined variable {x}")

    # Show the content of all envs
    def display(self, msg):
        print(msg, self, self.prev)

env = Env()     # always pointing to the current env

def main():
    global env
    env.extend("x", 0)         # scope0
    env.extend("y", 10)
    env.display("Scope 0:")

    env = env.openScope()      # scope1
    env.update("x", 5)
    env.extend("x", 1)
    env.display("Scope 1:")
    x = env.lookup("x")
    y = env.lookup("y")
    print("x,y =", x, y, "(should be 1,10)")

    env = env.openScope()      # scope2
    env.update("y", 11)
    env.extend("y", 12)
    env.display("Scope 2:")
    x = env.lookup("x")
    y = env.lookup("y")
    print("x,y =", x, y, "(should be 1,12)")

    env = env.closeScope()
    env = env.closeScope()
    env.display("Scope 0:")
    x = env.lookup("x")
    y = env.lookup("y")
    print("x,y =", x, y, "(should be 5,11)")

if __name__ == "__main__":
    main()

