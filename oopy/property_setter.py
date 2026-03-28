import math


class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    def area(self):
        return math.pi * self._radius ** 2


c = Circle(5)
# BUG: radius is a read-only property because no @radius.setter is defined;
# BUG: assigning to c.radius raises AttributeError instead of updating the value
c.radius = 10
print(c.area())
