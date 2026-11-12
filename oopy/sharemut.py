class BankAccount:
    history = []  # BUG: class attribute shared by all instances

    def __init__(self, owner):
        self.owner = owner

    def deposit(self, amount):
        self.history.append((self.owner, "deposit", amount))

    def withdraw(self, amount):
        self.history.append((self.owner, "withdrawal", amount))


if __name__ == "__main__":
    alice = BankAccount("Alice")
    bob = BankAccount("Bob")

    alice.deposit(100)
    bob.deposit(50)
    alice.withdraw(30)

    print(f"Alice's history: {alice.history}")
    print(f"Bob's history:   {bob.history}")  # BUG: shows Alice's transactions too
