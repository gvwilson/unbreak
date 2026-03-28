class Logger:
    def log(self, message):
        print(f"LOG: {message}")


class AppLogger(Logger):
    def __init__(self):
        # BUG: self.log = "application" replaces the inherited log() method
        # BUG: with a plain string; calling self.log("...") later raises
        # BUG: TypeError because strings are not callable
        self.log = "application"

    def run(self):
        self.log("Starting up")


app = AppLogger()
app.run()
