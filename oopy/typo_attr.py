class Student:
    def __init__(self, name):
        # BUG: the attribute is stored as self.nane (typo) but read as self.name;
        # BUG: Python stores and reads each spelling as a separate attribute,
        # BUG: so self.name is never set and raises AttributeError
        self.nane = name

    def greet(self):
        return f"Hi, I am {self.name}"


s = Student("Alice")
print(s.greet())
