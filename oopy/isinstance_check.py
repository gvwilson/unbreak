class Animal:
    def speak(self):
        return "..."


class Dog(Animal):
    def speak(self):
        return "Woof"


def make_sound(creature):
    # BUG: type() checks for an exact match and returns False for subclasses;
    # BUG: Dog is a subclass of Animal, so type(creature) == Animal is False for Dog
    # BUG: use isinstance(creature, Animal) to accept any Animal subclass
    if type(creature) == Animal:
        return creature.speak()
    raise ValueError("not an Animal")


d = Dog()
print(make_sound(d))
