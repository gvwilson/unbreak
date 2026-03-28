import math


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius ** 2


c = Circle(5)
# BUG: area is a property, not a regular method; accessing it with ()
# BUG: first evaluates the property (getting a float), then tries to call
# BUG: that float as a function, raising TypeError: 'float' object is not callable
print(c.area())
