class Person:
    def __init__(self, first, last, age):
        self.first = first
        self.last = last
        self.age = age

    def introduce(self):
        return f"I am {self.first} {self.last}, age {self.age}"


# BUG: the arguments are passed in the wrong order; age ends up in last
# BUG: and last ends up in age, so introduce() prints nonsense without
# BUG: raising an error—Python has no way to detect the mismatch
p = Person("Alice", 30, "Smith")
print(p.introduce())
