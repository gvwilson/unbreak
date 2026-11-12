def make_counter():
    count = 0

    def increment():
        # BUG: assigning to `count` makes it a local variable of `increment`,
        # BUG: so reading it on the right-hand side raises UnboundLocalError;
        # BUG: `nonlocal count` would bind it to the enclosing scope's variable
        count = count + 1
        return count

    return increment


counter = make_counter()
print(counter())  # expect 1, get UnboundLocalError
