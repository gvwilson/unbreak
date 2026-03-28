class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # stored as _BankAccount__balance

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance


account = BankAccount(100)
account.deposit(50)
# BUG: Python rewrites __balance to _BankAccount__balance at compile time;
# BUG: accessing account.__balance looks for the un-mangled name and raises AttributeError
print(account.__balance)
