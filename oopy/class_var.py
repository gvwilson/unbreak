class Roster:
    # BUG: students is a class variable shared by every Roster instance;
    # BUG: appending to self.students modifies the one shared list, so
    # BUG: enrolling a student in one roster affects all others
    students = []

    def __init__(self, name):
        self.name = name

    def enroll(self, student):
        self.students.append(student)


math = Roster("Math")
science = Roster("Science")
math.enroll("Alice")
print(science.students)  # expect [], get ['Alice']
