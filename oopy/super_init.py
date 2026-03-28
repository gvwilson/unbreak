class Animal:
    def __init__(self, name):
        self.name = name


class Dog(Animal):
    def __init__(self, name, breed):
        # BUG: super().__init__() is never called, so self.name is never set
        # BUG: Animal.__init__ is responsible for that attribute
        self.breed = breed

    def describe(self):
        return f"{self.name} is a {self.breed}"


d = Dog("Rex", "Labrador")
print(d.describe())
