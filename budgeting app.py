class Category:
    def __init__(self, name):
        self.ledger = []
        self.name = name

    def deposit(self, amount, description=""):
        # Record a positive financial entry
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        # Deduct funds only if balance is sufficient
        if self.check_funds(amount):
            self.ledger.append({"amount": -abs(amount), "description": description})
            return True
        return False

    def get_balance(self):
        # Calculate current net balance from ledger history
        balance = 0
        for transaction in self.ledger:
            balance += transaction["amount"]
        return balance

    def check_funds(self, amount):
        # Validate transaction amount before processing
        if amount <= 0 or not isinstance(amount, (int, float)):
            return
        return self.get_balance() >= amount

    def transfer(self, amount, category):
        # Move funds between categories if balance permits
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def __str__(self):
        # Build category summary receipt
        title = self.name.center(30, "*") + "\n"
        items = ""

        for transaction in self.ledger:
            # Truncate description and format amount to fit layout
            desc = transaction["description"][:23]
            amount = f"{transaction['amount']:.2f}"
            amount = amount[:7]
            items += f"{desc.ljust(23)}{amount.rjust(7)}\n"

        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    # Calculate spending per category
    spendings = []
    for category in categories:
        total_spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                total_spent += abs(item["amount"])
        spendings.append(total_spent)

    total_all_categories = sum(spendings)

    # Determine percentage per category (rounded down to nearest 10)
    percentages = []
    for spending in spendings:
        if total_all_categories > 0:
            percentage = (spending / total_all_categories) * 100
            percentage = int(percentage // 10) * 10
        else:
            percentage = 0
        percentages.append(percentage)

    # Build vertical chart visual
    chart = "Percentage spent by category\n"

    for i in range(100, -1, -10):
        chart += str(i).rjust(3) + "| "
        for p in percentages:
            if p >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    # Add axis separator
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # Transpose category names to vertical orientation
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


# Execution Example
food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
clothing = Category("Clothing")
food.transfer(50, clothing)
print(food)
