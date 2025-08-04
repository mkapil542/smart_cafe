import json
import os

ORDERS_FILE = "data/orders.json"

def save_order(order):
    os.makedirs("data", exist_ok=True)
    orders = []
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            try:
                orders = json.load(f)
            except json.JSONDecodeError:
                orders = []
    orders.append(order)
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=2)

def save_all_orders(order_list):
    os.makedirs("data", exist_ok=True)
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(order_list, f, indent=2)

def view_orders():
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def load_menu():
    path = os.path.join(os.path.dirname(__file__), "menu.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
