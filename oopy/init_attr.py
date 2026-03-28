class Point:
    def __init__(self, x, y):
        # BUG: x and y are assigned as local variables, not instance attributes
        # BUG: they are discarded when __init__ returns, leaving self with no x or y
        x = x
        y = y

    def distance(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


p = Point(3, 4)
print(p.distance())
