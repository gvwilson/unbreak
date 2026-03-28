class Scoreboard:
    def __init__(self, player):
        self.player = player

    def record(self, points):
        # BUG: self.score is created here but __init__ never sets a starting value;
        # BUG: if report() is called before record() has run at least once,
        # BUG: self.score does not exist and raises AttributeError
        self.score = points

    def report(self):
        return f"{self.player}: {self.score}"


board = Scoreboard("Alice")
print(board.report())  # AttributeError: 'Scoreboard' object has no attribute 'score'
