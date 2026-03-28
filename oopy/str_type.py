class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __str__(self):
        # BUG: __str__ must return a str; returning self.celsius (an int) raises
        # BUG: TypeError when Python tries to use the result as a string
        return self.celsius


t = Temperature(100)
print(t)
