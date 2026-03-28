class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # BUG: defining __eq__ automatically sets __hash__ to None, making
    # BUG: Point unhashable; Python requires __hash__ whenever __eq__ is defined
    # BUG: so the type can be used as a dictionary key or set member
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


p1 = Point(1, 2)
p2 = Point(1, 2)
seen = {p1}
print(p2 in seen)
