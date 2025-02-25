import json
import datetime

EXPENSE_FILE = "expenses.json"
CATEGORIES_FILE = "categories.json"
BALANCE_FILE = "balance.json"


# Load balance from file
def load_balance():
    try:
        with open(BALANCE_FILE, "r") as file:
            return json.load(file).get("balance", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return set_initial_balance()


# Save balance to file
def save_balance(balance):
    try:
        with open(BALANCE_FILE, "w") as file:
            json.dump({"balance": balance}, file, indent=4)
    except Exception as e:
        print(f"Error saving balance: {e}")


# Set initial balance
def set_initial_balance():
    while True:
        try:
            balance = float(input("Enter your initial balance: "))
            if balance < 0:
                print("Balance cannot be negative. Try again.")
                continue
            save_balance(balance)
            return balance
        except ValueError:
            print("Invalid input! Please enter a valid number.")


# Load expenses from file
def load_expenses():
    try:
        with open(EXPENSE_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Save expenses to file
def save_expenses(expenses):
    try:
        with open(EXPENSE_FILE, "w") as file:
            json.dump(expenses, file, indent=4)
    except Exception as e:
        print(f"Error saving expenses: {e}")


# Load categories from file
def load_categories():
    try:
        with open(CATEGORIES_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        default_categories = [
            {"id": 1, "name": "Food"},
            {"id": 2, "name": "Transport"},
            {"id": 3, "name": "Entertainment"},
            {"id": 4, "name": "Shopping"},
            {"id": 5, "name": "Other"}
        ]
        with open(CATEGORIES_FILE, "w") as file:
            json.dump(default_categories, file, indent=4)
        return default_categories


# Display available categories
def display_categories(categories):
    print("\nAvailable Categories:")
    for category in categories:
        print(f"{category['id']}. {category['name']}")


# Get valid amount
def get_valid_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount < 0:
                print("Amount cannot be negative. Try again.")
                continue
            return amount
        except ValueError:
            print("Invalid input! Enter a valid number.")


# Get valid category ID
def get_valid_category_id(categories):
    while True:
        try:
            category_id = int(input("Enter category ID: "))
            if any(cat["id"] == category_id for cat in categories):
                return category_id
            else:
                print("Invalid category ID. Try again.")
        except ValueError:
            print("Invalid input! Enter a number.")


# Add a new expense
def add_expense(expenses, categories, balance):
    amount = get_valid_amount("Enter expense amount: ")
    if amount > balance:
        print("Insufficient balance! Reduce the amount or add more funds.")
        return balance
    display_categories(categories)
    category_id = get_valid_category_id(categories)
    description = input("Enter description: ").capitalize()
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    expenses.append({"amount": amount, "category_id": category_id, "description": description, "date": date})
    save_expenses(expenses)
    balance -= amount
    save_balance(balance)
    print(f"Expense added! Remaining balance: ${balance:.2f}")
    return balance


# View expenses
def view_expenses(expenses, categories):
    if not expenses:
        print("No expenses recorded yet.")
        return
    for idx, expense in enumerate(expenses, 1):
        category_name = next((cat["name"] for cat in categories if cat["id"] == expense.get("category_id")), "Unknown")
        print(f"{idx}. ${expense['amount']:.2f} - {category_name} ({expense['description']}) on {expense['date']}")


# View total spending
def view_total_spending(expenses):
    total = sum(expense["amount"] for expense in expenses)
    print(f"Total spending: ${total:.2f}")


# View current balance
def view_balance(balance):
    print(f"Current balance: ${balance:.2f}")


# Main program loop
def main():
    balance = load_balance()
    if balance == 0:
        balance = set_initial_balance()
    if balance == 0:
        balance = set_initial_balance()
        expenses = load_expenses()
        categories = load_categories()
    expenses = load_expenses()
    categories = load_categories()
    balance = load_balance()

    while True:
        print("\nSmart Budget Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Total Spending")
        print("4. View Current Balance")
        print("5. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            balance = add_expense(expenses, categories, balance)
        elif choice == "2":
            view_expenses(expenses, categories)
        elif choice == "3":
            view_total_spending(expenses)
        elif choice == "4":
            view_balance(balance)
        elif choice == "5":
            print("Goodbye! Restarting the budget tracker...")
            open(BALANCE_FILE, "w").close()  # Clear balance file
            open(EXPENSE_FILE, "w").close()  # Clear expenses file
            return
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()





