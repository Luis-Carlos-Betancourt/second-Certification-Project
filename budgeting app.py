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
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        else:
            return False

    def __str__(self):
        title = self.name.center(30, "*") + "\n"
        items = ""

        for transaction in self.ledger:
            desc = transaction["description"][:23]
            amount = f"{transaction['amount']:.2f}"
            amount = amount[:7]
            items += f"{desc.ljust(23)}{amount.rjust(7)}\n"

        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    spendings = []
    for category in categories:
        total_spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                total_spent += abs(item["amount"])
        spendings.append(total_spent)

    total_all_categories = sum(spendings)

    percentages = []
    for spending in spendings:
        if total_all_categories > 0:
            percentage = (spending / total_all_categories) * 100
            percentage = int(percentage // 10) * 10
        else:
            percentage = 0
        percentages.append(percentage)

    chart = "Percentage spent by category\n"

    for i in range(100, -1, -10):
        chart += str(i).rjust(3) + "| "
        for p in percentages:
            if p >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    max_len = max([len(cat.name) for cat in categories])

    for i in range(max_len):
        chart += "     "
        for category in categories:
            if i < len(category.name):
                chart += category.name[i] + "  "
            else:
                chart += "   "
        if i < max_len - 1:
            chart += "\n"

    return chart


food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
clothing = Category("Clothing")
food.transfer(50, clothing)
print(food)
