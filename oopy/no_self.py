class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    # BUG: the method signature is missing self as its first parameter;
    # BUG: Python passes the instance automatically, so calling r.area()
    # BUG: supplies one argument to a function that expects zero
    def area():
        return self.width * self.height


r = Rectangle(4, 6)
print(r.area())
