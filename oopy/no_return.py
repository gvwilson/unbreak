class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def peek(self):
        # BUG: the method computes the top item but never returns it;
        # BUG: Python implicitly returns None from any function without a return statement
        if self._items:
            top = self._items[-1]


s = Stack()
s.push(42)
result = s.peek()
print(result + 1)  # TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
