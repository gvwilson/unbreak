class Widget:
    count = 0

    def __init__(self):
        Widget.count += 1

    # BUG: @staticmethod does not receive any implicit first argument,
    # BUG: so cls is undefined inside how_many(); use @classmethod to
    # BUG: receive the class as cls automatically
    @staticmethod
    def how_many():
        return cls.count


w1 = Widget()
w2 = Widget()
print(Widget.how_many())
