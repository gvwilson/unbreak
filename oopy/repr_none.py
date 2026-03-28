class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        # BUG: the f-string is constructed but never returned;
        # BUG: __repr__ implicitly returns None, so repr(c) and str(c)
        # BUG: raise TypeError: __repr__ returned non-string (type NoneType)
        f"{self.rank} of {self.suit}"


c = Card("Ace", "Spades")
print(repr(c))
