class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


p = Point(3, 4)
# BUG: __slots__ removes the instance __dict__ and restricts attributes to those
# BUG: listed in the tuple; assigning p.z raises AttributeError because "z" is
# BUG: not in __slots__
p.z = 0
print(p.x, p.y, p.z)
