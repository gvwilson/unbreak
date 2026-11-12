def make_multipliers():
    """Return a list of functions that multiply by 0, 1, 2, 3, 4."""
    multipliers = []
    for i in range(5):
        # BUG: each lambda captures the variable `i`, not its value; by the
        # BUG: time they are called, `i` is 4, so every lambda multiplies by 4
        multipliers.append(lambda x: x * i)
    return multipliers


funcs = make_multipliers()
print([f(10) for f in funcs])  # expect [0, 10, 20, 30, 40], get [40, 40, 40, 40, 40]
