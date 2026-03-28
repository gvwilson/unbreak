def memoize(func):
    """Cache the results of func calls."""
    cache = {}

    def wrapper(*args, **kwargs):
        key = args                      # BUG: kwargs not included in key;
        if key not in cache:            #      different keyword args return the
            cache[key] = func(*args, **kwargs)  # same cached value
        return cache[key]

    return wrapper


@memoize
def power(base, exponent=2):
    print(f"  (computing {base}^{exponent})")
    return base ** exponent


if __name__ == "__main__":
    print(f"power(3)            = {power(3)}")           # computes 3^2 = 9
    print(f"power(3, exponent=3)= {power(3, exponent=3)}")  # BUG: returns 9 not 27
    print(f"power(3, 3)         = {power(3, 3)}")        # BUG: also returns 9
