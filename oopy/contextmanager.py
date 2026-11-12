import time


class Timer:
    def __enter__(self):
        self.start = time.time()
        # BUG: __enter__ must return the object the `as` target binds to; with
        # BUG: no return statement it returns None, so `t` becomes None

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def elapsed(self):
        return time.time() - self.start


with Timer() as t:
    pass
print(t.elapsed())  # expect a number, get AttributeError: 'NoneType' object has no attribute 'elapsed'
