import json
import datetime

EXPENSE_FILE = "expenses.json"
CATEGORIES_FILE = "categories.json"
BALANCE_FILE = "balance.json"


# Load balance from file
def load_balance():
    """
    Load the user's balance from a file.

    This function attempts to read the balance from a JSON file. If the file does not exist
    or contains invalid data, it prompts the user to set an initial balance.

    Returns:
        float: The current balance stored in the file, or a new balance set by the user.
    """
    try:
        with open(BALANCE_FILE, "r") as file:
            return json.load(file).get("balance", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return set_initial_balance()


# Save balance to file
def save_balance(balance):
    """
    Save the user's balance to a file.

    This function writes the balance to a JSON file, ensuring that the latest balance
    is stored persistently.

    Args:
        balance (float): The balance amount to save.
    """
    try:
        with open(BALANCE_FILE, "w") as file:
            json.dump({"balance": balance}, file, indent=4)
    except Exception as e:
        print(f"Error saving balance: {e}")


# Set initial balance
def set_initial_balance():
    """
    Prompt the user to enter an initial balance and validate the input.

    This function ensures that the user enters a non-negative numeric value for the initial balance.
    If the input is invalid (e.g., a negative number or non-numeric input), it prompts the user to try again.
    Once a valid balance is provided, it saves the balance to a file and returns it.

    Returns:
        float: The initial balance set by the user.
    """
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
    """
    Load expenses from the file or create a new file if it doesn't exist.

    Returns:
        list: A list of expenses loaded from the file, or an empty list if the file doesn't exist or is invalid.
    """
    try:
        with open(EXPENSE_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Save expenses to file
def save_expenses(expenses):
    """
    Save the expense list to a file.

    Args:
        expenses (list): The list of expenses to save.
    """
    try:
        with open(EXPENSE_FILE, "w") as file:
            json.dump(expenses, file, indent=4)
    except Exception as e:
        print(f"Error saving expenses: {e}")


# Load categories from file
def load_categories():
    """
    Load categories from the file or create a new file with default categories if it doesn't exist.

    Returns:
        list: A list of categories loaded from the file, or the default categories if the file doesn't exist or is invalid.
    """
    try:
        with open(CATEGORIES_FILE, "r") as file:
            categories = json.load(file)
            print("Categories loaded successfully!")  # Debug message
            return categories
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading categories: {e}. Creating default categories...")  # Debug message
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
    """
    Display available categories to the user.

    Args:
        categories (list): The list of categories to display.
    """
    print("\nAvailable Categories:")
    for category in categories:
        print(f"{category['id']}. {category['name']}")


#Get a valid amount input
def get_valid_amount(prompt):
    """
    Get a valid amount input from the user.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        float: The valid amount entered by the user.
    """
    while True:
        try:
            amount = float(input(prompt))
            if amount < 0:
                print("Amount cannot be negative. Please try again.")
                continue
            return amount
        except ValueError:
            print("Invalid input! Please enter a valid number.")

# Get a valid string input
def get_valid_string(prompt):
    """
    Get a non-empty string input from the user.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: The non-empty string entered by the user.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value.capitalize()
        print("Input cannot be empty. Please try again.")


# Get a valid category ID input
def get_valid_category_id(categories):
    """
    Get a valid category ID from the user.

    Args:
        categories (list): The list of available categories.

    Returns:
        int: The valid category ID entered by the user.
    """
    while True:
        try:
            category_id = int(input("Enter category ID: "))
            if any(cat["id"] == category_id for cat in categories):
                return category_id
            else:
                print("Invalid category ID. Please try again.")
        except ValueError:
            print("Invalid input! Please enter a number.")

# Add a new expense
def add_expense(expenses, categories, balance):
    """
    Add a new expense entry to the budget tracker.

    This function prompts the user to enter an expense amount, validates it, and ensures
    that the balance is sufficient. The user selects a category, enters a description, and
    the expense is recorded with a timestamp. The balance is updated and saved.

    Args:
        expenses (list): The list of recorded expenses.
        categories (list): The list of available categories.
        balance (float): The user's current balance.

    Returns:
        float: The updated balance after deducting the expense.
    """
    while True:
        amount = get_valid_amount("Enter expense amount: ")
        if amount > balance:
            print("Insufficient balance! Reduce the amount or add more funds.")
            return balance

        display_categories(categories)
        category_id = get_valid_category_id(categories)
        description = input("Enter description: ").capitalize()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        expenses.append({"amount": -amount, "category_id": category_id, "description": description, "date": date})
        save_expenses(expenses)
        balance -= amount
        save_balance(balance)

        print(f"Expense added! Remaining balance: ${balance:.2f}")

        continue_using = input("Do you want to continue using the budget tracker? (yes/no): ").strip().lower()
        if continue_using == "no":
            print("Goodbye!")
            exit()

        return balance


# Add funds to the budget
def add_funds(expenses, balance):
    """
    Add funds to the budget tracker.

    This function prompts the user to enter an amount to add to their balance.
    The user also enters a description (e.g., salary, gift, etc.), and the transaction
    is recorded with a timestamp. The balance is updated and saved.

    Args:
        expenses (list): The list of recorded transactions.
        balance (float): The user's current balance.

    Returns:
        float: The updated balance after adding funds.
    """
    while True:
        amount = get_valid_amount("Enter the amount you want to add: ")
        description = input("Enter the source of income (e.g., tutoring, gift, salary): ").capitalize()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        expenses.append({"amount": amount, "category_id": "Income", "description": description, "date": date})
        save_expenses(expenses)
        balance += amount
        save_balance(balance)

        print(f"Funds added! New balance: ${balance:.2f}")

        continue_using = input("Do you want to continue using the budget tracker? (yes/no): ").strip().lower()
        if continue_using == "no":
            print("Goodbye!")
            exit()

        return balance


# View expenses
def view_expenses(expenses, categories):
    """
    Display all recorded expenses.

    This function iterates through the list of expenses and prints each expense
    with its corresponding category, description, amount, and timestamp.

    Args:
        expenses (list): The list of recorded expenses.
        categories (list): The list of available categories.
    """
    if not expenses:
        print("No expenses recorded yet.")
        return

    for idx, expense in enumerate(expenses, 1):
        category = next((cat["name"] for cat in categories if cat["id"] == expense.get("category_id")), "Income")
        print(f"{idx}. ${expense['amount']:.2f} - {category} ({expense['description']}) on {expense['date']}")


# Filter expenses by category
def filter_expenses_by_category(expenses, categories):
    """
    Filter and display expenses by category.

    Args:
        expenses (list): The list of expenses.
        categories (list): The list of available categories.
    """
    display_categories(categories)
    category_id = get_valid_category_id(categories)

    # Use .get() to handle missing category_id keys
    filtered = [exp for exp in expenses if exp.get("category_id") == category_id]

    if not filtered:
        print(f"No expenses found for category ID {category_id}.")
    else:
        category_name = next((cat["name"] for cat in categories if cat["id"] == category_id), "Unknown")
        print(f"\nExpenses for {category_name}:")
        for exp in filtered:
            print(f"${exp['amount']:.2f} - {exp['description']} on {exp['date']}")

# View total spending
def view_total_spending(expenses):
    """
    Calculate and display the total spending.

    This function sums all negative amounts in the expenses list (expenses are stored as negative values).
    It then prints the total spending amount in absolute value format.

    Args:
        expenses (list): The list of recorded expenses.
    """
    total_spent = sum(exp["amount"] for exp in expenses if exp["amount"] < 0)
    print(f"Total spending: ${abs(total_spent):.2f}")


# View current balance
def view_balance(balance):
    """
    Display the current available balance.

    Args:
        balance (float): The user's current balance.
    """
    print(f"Current balance: ${balance:.2f}")


# Main program loop
def main():
    """
    Main program loop for the budget tracker.

    This function initializes the budget tracker by loading or setting an initial balance.
    It then enters a loop displaying the main menu, allowing the user to:
    1. Add an expense
    2. Add funds
    3. View recorded expenses
    4. Filter expenses by category
    5. View total spending
    6. View the current balance
    7. Exit the program

    The loop continues until the user selects the exit option, at which point
    the balance and expenses files are cleared, restarting the budget tracker.
    """
    while True:
        balance = load_balance()
        if balance == 0:
            balance = set_initial_balance()

        expenses = load_expenses()
        categories = load_categories()

        while True:
            print("\nSmart Budget Tracker")
            print("1. Add Expense")
            print("2. Add Funds")
            print("3. View Expenses")
            print("4. Filter Expenses by Category")
            print("5. View Total Spending")
            print("6. View Current Balance")
            print("7. Exit")

            choice = input("Choose an option: ")
            if choice == "1":
                balance = add_expense(expenses, categories, balance)
            elif choice == "2":
                balance = add_funds(expenses, balance)
            elif choice == "3":
                view_expenses(expenses, categories)
            elif choice == "4":
                filter_expenses_by_category(expenses, categories)
            elif choice == "5":
                view_total_spending(expenses)
            elif choice == "6":
                view_balance(balance)
            elif choice == "7":
                print("Goodbye! Restarting the budget tracker...")
                open(BALANCE_FILE, "w").close()  # Clear balance file
                open(EXPENSE_FILE, "w").close()  # Clear expenses file
                return
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
