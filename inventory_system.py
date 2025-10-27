"""
Inventory Management System

A simple program to manage inventory items with quantity tracking.
Provides functions to add, remove, load, save, and report on inventory items.
"""

import json
from datetime import datetime
import ast


# Global variable
stock_data = {}


def add_item(item, qty, logs=None):
    """
    Add an item to the inventory.

    Args:
        item (str): The item name
        qty (int): Quantity to add
        logs (list, optional): Log list for tracking changes

    Returns:
        None
    """
    if logs is None:
        logs = []

    if not item or not isinstance(item, str):
        print("Error: Item must be a non-empty string")
        return

    if not isinstance(qty, int) or qty < 0:
        print("Error: Quantity must be a non-negative integer")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    log_message = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(log_message)
    print(log_message)


def remove_item(item, qty):
    """
    Remove an item from the inventory.

    Args:
        item (str): The item name to remove
        qty (int): Quantity to remove

    Returns:
        None
    """
    try:
        if item not in stock_data:
            raise KeyError(f"Item '{item}' not found")

        if stock_data[item] < qty:
            print(f"Warning: Only {stock_data[item]} of '{item}' available")
            qty = stock_data[item]

        stock_data[item] -= qty

        if stock_data[item] == 0:
            del stock_data[item]

        print(f"Removed {qty} of {item} from inventory")

    except KeyError as e:
        print(f"Error: {e}")
    except (TypeError, ValueError) as e:
        print(f"Invalid input: {e}")


def get_qty(item):
    """
    Get the quantity of an item in inventory.

    Args:
        item (str): The item name

    Returns:
        int: Quantity of the item, or 0 if not found
    """
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Load inventory data from a JSON file.

    Args:
        file (str): Path to the JSON file

    Returns:
        None
    """
    global stock_data  # pylint: disable=global-statement
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
        print(f"Data loaded from {file}")
    except FileNotFoundError:
        print(f"File {file} not found. Starting with empty inventory.")
        stock_data = {}
    except json.JSONDecodeError:
        print(f"Error reading {file}. Starting with empty inventory.")
        stock_data = {}


def save_data(file="inventory.json"):
    """
    Save inventory data to a JSON file.

    Args:
        file (str): Path to the JSON file

    Returns:
        None
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=2)
        print(f"Data saved to {file}")
    except IOError as e:
        print(f"Error saving data: {e}")


def print_data():
    """
    Print a report of all items in inventory.

    Returns:
        None
    """
    print("\n" + "=" * 40)
    print("Items Report")
    print("=" * 40)

    if not stock_data:
        print("No items in inventory")
    else:
        for item, quantity in stock_data.items():
            print(f"{item} -> {quantity}")

    print("=" * 40 + "\n")


def check_low_items(threshold=5):
    """
    Find items below a quantity threshold.

    Args:
        threshold (int): Minimum quantity threshold

    Returns:
        list: List of items below the threshold
    """
    result = []
    for item, quantity in stock_data.items():
        if quantity < threshold:
            result.append(item)
    return result


def main():
    """
    Main function to demonstrate inventory system functionality.

    Returns:
        None
    """
    print("Inventory Management System Starting...\n")

    # Add valid items
    add_item("apple", 10)
    add_item("banana", 5)
    add_item("orange", 3)

    # Try to add invalid items (will be rejected)
    add_item("grape", -2)  # Negative quantity
    add_item(123, 10)  # Invalid type

    # Remove items
    remove_item("apple", 3)
    remove_item("orange", 1)
    remove_item("pear", 1)  # Item doesn't exist

    # Check quantities
    print(f"\nApple stock: {get_qty('apple')}")
    print(f"Banana stock: {get_qty('banana')}")

    # Check low stock items
    low_items = check_low_items(threshold=5)
    print(f"Low stock items (< 5): {low_items}")

    # Save and load data
    save_data()

    # Print inventory report
    print_data()

    # Safe user input handling
    print("Enter a Python literal (number, list, dict, etc.):")
    user_input = input("> ")
    try:
        value = ast.literal_eval(user_input)
        print(f"You entered: {value} (type: {type(value).__name__})")
    except (ValueError, SyntaxError):
        print("Invalid input. Please enter a valid Python literal.")


if __name__ == "__main__":
    main()
