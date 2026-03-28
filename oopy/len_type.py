class DataSet:
    def __init__(self, data):
        self.data = data

    def __len__(self):
        # BUG: __len__ must return a non-negative integer; the / operator
        # BUG: always produces a float in Python 3, even for whole-number results,
        # BUG: and Python rejects a float here with TypeError
        return len(self.data) / 1


ds = DataSet([10, 20, 30])
print(len(ds))
