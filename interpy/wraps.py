def logged(func):
    # BUG: missing @functools.wraps(func), so the wrapper hides the original
    # BUG: function's __name__ and __doc__ from introspection and help()
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


@logged
def add(a, b):
    """Return a + b."""
    return a + b


print(add(2, 3))       # calling add / 5
print(add.__name__)    # expect 'add', get 'wrapper'
print(add.__doc__)     # expect 'Return a + b.', get None
