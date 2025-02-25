import json
import datetime

# File paths
EXPENSE_FILE = "expenses.json"
CATEGORIES_FILE = "categories.json"

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


# Get a valid amount input
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
def add_expense(expenses, categories):
    """
    Add a new expense to the list.

    Args:
        expenses (list): The list of expenses.
        categories (list): The list of available categories.
    """
    amount = get_valid_amount("Please enter expense amount: ")
    display_categories(categories)
    category_id = get_valid_category_id(categories)
    description = get_valid_string("Please enter description: ")
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    expenses.append({"amount": amount, "category_id": category_id, "description": description, "date": date})
    save_expenses(expenses)
    print("Expense added successfully!")


# View all expenses
def view_expenses(expenses, categories):
    """
    Display all recorded expenses.

    Args:
        expenses (list): The list of expenses.
        categories (list): The list of available categories.
    """
    if not expenses:
        print("No expenses recorded yet.")
        return

    for idx, expense in enumerate(expenses, 1):
        category_name = next((cat["name"] for cat in categories if cat["id"] == expense.get("category_id")), "Unknown")
        print(f"{idx}. ${expense['amount']:.2f} - {category_name} ({expense['description']}) on {expense['date']}")


# View total spending
def view_total_spending(expenses):
    """
    Calculate and display total spending.

    Args:
        expenses (list): The list of expenses.
    """
    total = sum(expense["amount"] for expense in expenses)
    print(f"Total spending: ${total:.2f}")


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


# Delete an expense
def delete_expense(expenses):
    """
    Delete an expense from the list.

    Args:
        expenses (list): The list of expenses.
    """
    view_expenses(expenses)
    try:
        index = int(input("Enter the number of the expense to delete: ")) - 1
        if 0 <= index < len(expenses):
            del expenses[index]
            save_expenses(expenses)
            print("Expense deleted successfully!")
        else:
            print("Invalid expense number.")
    except ValueError:
        print("Invalid input! Please enter a number.")


# Edit an expense
def edit_expense(expenses, categories):
    """
    Edit an existing expense.

    Args:
        expenses (list): The list of expenses.
        categories (list): The list of available categories.
    """
    view_expenses(expenses, categories)
    try:
        index = int(input("Enter the number of the expense to edit: ")) - 1
        if 0 <= index < len(expenses):
            amount = get_valid_amount("Enter new expense amount: ")
            display_categories(categories)
            category_id = get_valid_category_id(categories)
            description = get_valid_string("Enter new description: ")
            expenses[index] = {"amount": amount, "category_id": category_id, "description": description,
                               "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            save_expenses(expenses)
            print("Expense updated successfully!")
        else:
            print("Invalid expense number.")
    except ValueError:
        print("Invalid input! Please enter a number.")


# Main program loop
def main():
    """
    Main program loop for the Smart Expense Tracker.
    """
    expenses = load_expenses()
    categories = load_categories()

    while True:
        print("\nSmart Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Total Spending")
        print("4. Filter Expenses by Category")
        print("5. Delete an Expense")
        print("6. Edit an Expense")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense(expenses, categories)
        elif choice == "2":
            view_expenses(expenses, categories)
        elif choice == "3":
            view_total_spending(expenses)
        elif choice == "4":
            filter_expenses_by_category(expenses, categories)
        elif choice == "5":
            delete_expense(expenses)
        elif choice == "6":
            edit_expense(expenses, categories)
        elif choice == "7":
            print("Goodbye! See you soon!")
            break
        else:
            print("Invalid choice, please try again.")


# Entry point
if __name__ == "__main__":
    main()