class Cart:
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    # BUG: __len__ returns a hard-coded 1 instead of the real length, so an
    # BUG: empty cart is truthy and `if cart:` behaves as if it had items
    def __len__(self):
        return 1


cart = Cart()
if cart:
    print("cart has items")  # expect no output, but prints this
else:
    print("cart is empty")
