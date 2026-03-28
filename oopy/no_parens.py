class Greeter:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"


g = Greeter("world")
# BUG: greet without parentheses retrieves the bound method object itself,
# BUG: not the string the method returns; the output will be something like
# BUG: <bound method Greeter.greet of <__main__.Greeter object ...>>
print(g.greet)
