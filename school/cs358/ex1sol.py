# Lex Albrandt
# CS358
# Exercise 1


# ------------------------------
# Problem 1
# ------------------------------

def newstack() -> list:
    """Instantiates a new stack

    Args:
        None

    Returns:
        list: empty list
    """
    return []

def newqueue() -> list:
    """Instantiates a new queue

    Args:
        None

    Returns:
        list: empty queue
    """
    return []


def push(s: list, x: int) -> list:
    """Pushes an item onto the stack

    Args:
        s (list): stack
        x (int): item to add

    Returns:
        s (list): modified stack
    """
    s.append(x)

    return s

    
def pop(s: list) -> list:
    """Pops an item off the stack

    Args:
        s (list): stack

    Returns:
        item (int): popped item
    """
    item = s.pop()

    return item


def enqueue(q: list, x: int) -> list:
    """Enqueues an item to the queue

    Args:
        q (list): queue
        x (int): item to add

    Returns:
        q (list): modified queue
    """

    q.append(x)

    return q

    
def dequeue(q: list) -> list:
    """Dequeues an item from the queue

    Args:
        q (list): queue

    Returns:
        item (int): dequeued item
    """

    item = q.pop(0)

    return item


def testsq() -> None:
    """Tests push(), pop(), enqueue(), and dequeue()
    
    Args:
        None
    
    Returns:
        None
    """

    # Instantiate and print new stack
    s = newstack()
    print(f"Stack contents: {s}")

    # Push an item onto the stack
    push(s, 3)
    print(f"Stack contents: {s}")

    # Push 3 more items onto the stack and print results
    push(s, 4)
    push(s, 1)
    push(s, 5)
    print(f"Stack contents: {s}")

    # Pop an item from the stack and print
    pop(s)
    print(f"Stack contents: {s}")

    # Instantiate a new queue and print
    q = newqueue()
    print(f"Queue contents: {q}")

    # Enqueue an item and print
    enqueue(q, 3)
    print(f"Queue contents: {q}")

    # Enqueue 3 more items and print
    enqueue(q, 4)
    enqueue(q, 6)
    enqueue(q, 1)
    print(f"Queue contents: {q}")

    # Dequeue an item and print
    dequeue(q)
    print(f"Queue contents: {q}\n")

# Call test function
print(f"Testing problem 1.....")
testsq()

# ----------------------
# Problem 2
# ----------------------   

def palindrome(str: str) -> bool:
    """Checks to see if the string is a palindrome

    Args:
        str (str): string to test

    Returns:
        bool: Returns True if string is a palindrome, false if not
    """

    pal_test = str[::-1]
    print(f"Reversed string: {pal_test}")

    for i in range(len(str)):
        if str[i] != pal_test[i]:
            return False
    
    return True

print(f"Testing problem 2... Palindrome...")
test = palindrome("hello")
print(f"Result: {test}")

test = palindrome("racecar")
print(f"Result: {test}\n")

def factorial(n: int) -> int:
    """Function to compute the factorial of the integer

    Args:
        n (int): integer for factorial calculation

    Returns:
        fact (int): factorial of the integer
        None: if n is negative
    """
    if n < 0:
        return None

    if n == 0 or n == 1:
        return 1

    fact = 1
    for i in range(1, n + 1):
        fact = fact * i

    return fact


print(f"Testing problem 2... Factorial...")
test = factorial(4)
print(f"Result: {test}")

test = factorial(-1)
print(f"Result: {test}")

test = factorial(1)
print(f"Result: {test}")


# ------------------------------------
# Problem 3
# ------------------------------------

"""
3a. [- [+ 1 [* [** 2 3] 4]] 5] = 28
3b. [+ 1 [ ** 2 [* 3 [- 4 5]]]] = 9/8

"""