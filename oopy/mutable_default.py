class Bag:
    # BUG: the default list [] is created once when the class is defined,
    # BUG: not each time __init__ runs, so all Bag instances that omit items
    # BUG: share the same list object
    def __init__(self, items=[]):
        self.items = items

    def add(self, item):
        self.items.append(item)


a = Bag()
b = Bag()
a.add("apple")
print(b.items)  # expect [], get ['apple']
