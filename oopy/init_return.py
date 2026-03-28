class Config:
    def __init__(self, debug):
        self.debug = debug
        # BUG: __init__ must return None; Python raises TypeError if it
        # BUG: returns any other value, including the instance itself
        return self


c = Config(True)
print(c.debug)
