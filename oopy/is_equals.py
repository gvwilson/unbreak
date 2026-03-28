class Status:
    def __init__(self, code):
        self.code = code

    def is_ok(self):
        # BUG: `is` checks object identity, not equality; two Status objects
        # BUG: with the same code are different objects in memory, so `is` returns
        # BUG: False even when the codes match; use == to compare values
        return self is Status("ok")


s = Status("ok")
print(s.is_ok())  # expect True, get False
