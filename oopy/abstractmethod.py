from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def speak(self):
        """Return the sound this animal makes."""


class Dog(Animal):
    # BUG: Dog never implements the abstract method speak, so it is still
    # BUG: abstract and Python refuses to instantiate it
    def __init__(self, name):
        self.name = name


d = Dog("Rex")  # expect a Dog, get TypeError: Can't instantiate abstract class Dog
