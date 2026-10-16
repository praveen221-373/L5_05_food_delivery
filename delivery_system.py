"""Food delivery order queue manager."""


import json
from datetime import datetime

# Shared in-memory order state.
orders = {}
next_id = 1
menu = {}
VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]


def create_order(customer, items, order_history=None):
    """Create a new order and return its order id."""
    global next_id
    if order_history is None:
        order_history = []
    total = 0
    for item in items:
        total += menu.get(item, 99)
    orders[next_id] = {
        "customer": customer,
        "items": items,
        "total": total,
        "status": "placed",
    }
    order_history.append(next_id)
    next_id += 1
    return order_history[-1]


def update_order_status(order_id, status):
    """Update the status of an existing order."""
    if order_id not in orders:
        print("Invalid order id:", order_id)
        return False
    if status not in VALID_STATUSES:
        print("Invalid status:", status)
        return False
    orders[order_id]["status"] = status
    return True


def read_menu_config(file="menu.json"):
    """Load menu prices from a JSON file, or use defaults."""
    global menu
    try:
        with open(file, encoding="utf-8") as menu_file:
            loaded = json.load(menu_file)
        if isinstance(loaded, dict):
            menu = loaded
        else:
            raise ValueError("menu file must contain an object")
    except (OSError, ValueError, json.JSONDecodeError):
        menu = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}


def daily_revenue():
    """Return the total revenue for delivered orders."""
    revenue = 0
    for order in orders.values():
        if order["status"] == "delivered":
            revenue += order["total"]
    return revenue


def backup_orders(file="orders.json"):
    """Save the current order queue to a JSON file."""
    with open(file, "w", encoding="utf-8") as backup_file:
        json.dump(orders, backup_file, indent=2, ensure_ascii=False)


def _validate_order(order):
    """Validate a single restored order entry."""
    if not isinstance(order, dict):
        return None
    required = {"customer", "items", "total", "status"}
    if not required.issubset(order):
        return None
    if not isinstance(order["items"], list):
        return None
    if not isinstance(order["total"], (int, float)):
        return None
    if order["status"] not in VALID_STATUSES:
        return None
    return order


def restore_orders(file="orders.json"):
    """Restore the order queue from a JSON file."""
    global orders, next_id
    try:
        with open(file, encoding="utf-8") as backup_file:
            loaded = json.load(backup_file)
    except FileNotFoundError:
        print("Backup file not found:", file)
        return
    except (OSError, json.JSONDecodeError, ValueError):
        print("Invalid backup file:", file)
        return

    if not isinstance(loaded, dict):
        print("Invalid backup data")
        return

    restored = {}
    for key, value in loaded.items():
        try:
            order_id = int(key)
        except (TypeError, ValueError):
            print("Invalid order id in backup:", key)
            continue
        validated = _validate_order(value)
        if validated is None:
            print("Skipping malformed order:", key)
            continue
        restored[order_id] = validated

    orders = restored
    next_id = (max(orders) + 1) if orders else 1


def print_queue():
    """Print the current order queue."""
    print(f"Order queue at {datetime.now()}")
    for order_id, order in orders.items():
        print(
            order_id,
            order["customer"],
            order["status"],
            order["total"],
        )


def main():
    """Run the order queue demonstration."""
    read_menu_config()
    order_a = create_order("Asha", ["pizza", "coke"])
    order_b = create_order("Ravi", ["burger", "sushi"])
    order_c = create_order("", [])
    update_order_status(order_a, "delivered")
    update_order_status(order_b, "teleported")
    update_order_status(42, "delivered")
    update_order_status(order_c, "delivered")
    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    print_queue()


main()
