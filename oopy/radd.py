class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        ox, oy = other
        return Vector(self.x + ox, self.y + oy)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


v = Vector(1, 2)
print(v + (3, 4))   # Vector(4, 6)
# BUG: only __add__ is defined; `(3, 4) + v` has no __radd__ to handle it,
# BUG: so Python raises TypeError when the tuple is the left operand
print((3, 4) + v)   # expect Vector(4, 6), get TypeError
