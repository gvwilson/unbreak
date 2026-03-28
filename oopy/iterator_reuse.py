class Countdown:
    def __init__(self, start):
        self.start = start
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1


c = Countdown(3)
print(list(c))  # [3, 2, 1]
# BUG: self.current is already 0 after the first pass, so the second
# BUG: iteration raises StopIteration immediately and returns an empty list;
# BUG: the iterator never resets because __iter__ returns the same exhausted object
print(list(c))  # expect [3, 2, 1], get []
