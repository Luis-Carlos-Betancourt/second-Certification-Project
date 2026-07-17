class Category:
    def __init__(self, name):
        self.ledger = []
        self.name = name

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -abs(amount), "description": description})
            return True
        else:
            return False

    def get_balance(self):
        balance = 0
        for transaction in self.ledger:
            balance += transaction["amount"]
        return balance

    def check_funds(self, amount):
        if amount <= 0 or not isinstance(amount, (int, float)):
            return
        if self.get_balance() >= amount:
            return True
        else:
            return False

    def transfer(self, amount, category):
        if self.check_funds():
            self.withdraw(amount, f"Transfer to {category.name}")


def create_spend_chart(categories):
    pass


# testing
mi_deposit = Category("libros")
mi_deposit.deposit(1000000, "initial deposit")
mi_deposit.withdraw(15, "purchase books")
