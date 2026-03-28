class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}"


class Dog(Animal):
    def __init__(self, name):
        # BUG: super().__init__() not called; self.name and self.sound are never set
        self.tricks = []

    def learn_trick(self, trick):
        self.tricks.append(trick)

    def show_tricks(self):
        return f"{self.name} knows: {', '.join(self.tricks)}"


if __name__ == "__main__":
    dog = Dog("Rex")
    dog.learn_trick("sit")
    dog.learn_trick("shake")
    print(f"Tricks: {dog.tricks}")
    print(dog.speak())       # AttributeError: 'Dog' object has no attribute 'name'
