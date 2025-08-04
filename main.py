import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import uuid

# ---------- Menu Items ----------
MENU_ITEMS = {
    "☕ Coffee": 120,
    "🍵 Tea": 80,
    "🥐 Croissant": 100,
    "🍰 Cake": 150,
    "🥤 Smoothie": 130
}

cafe_orders_file = "orders.json"  # Default file

# ---------- Save & Show Receipt ----------
def save_order(name, selections, pickup_time, comments):
    order_id = str(uuid.uuid4())[:8]
    total = 0
    item_summary = []

    for item, qty in selections.items():
        if qty > 0:
            price = MENU_ITEMS[item]
            subtotal = qty * price
            total += subtotal
            item_summary.append(f"{item} x{qty} — ₹{subtotal}")

    if not item_summary:
        messagebox.showerror("No Items Selected", "Select at least one item with quantity > 0.")
        return

    order_data = {
        "order_id": order_id,
        "name": name,
        "items": item_summary,
        "total_price": total,
        "pickup_time": pickup_time,
        "comments": comments if comments else "N/A",
        "timestamp": datetime.now().isoformat()
    }

    try:
        with open(cafe_orders_file, "r") as f:
            orders = json.load(f)
    except FileNotFoundError:
        orders = []

    orders.append(order_data)

    with open(cafe_orders_file, "w") as f:
        json.dump(orders, f, indent=2)

    receipt = (
        f"🧾 Receipt\n\n"
        f"Order ID: {order_id}\n"
        f"Name: {name}\n"
        f"Items:\n  " + "\n  ".join(item_summary) + "\n"
        f"Total: ₹{total}\n"
        f"Pickup Time: {pickup_time}\n"
        f"Comments: {comments if comments else 'N/A'}\n\n"
        f"Thank you for your order!"
    )
    messagebox.showinfo("Order Confirmed!", receipt)

# ---------- Customer Order Screen ----------
def open_order_window():
    win = tk.Toplevel(root)
    win.title("Customer Order")

    tk.Label(win, text="Customer Name:").grid(row=0, column=0)
    name_entry = tk.Entry(win)
    name_entry.grid(row=0, column=1)

    # Item dropdowns
    item_vars = {}
    for i, (item, price) in enumerate(MENU_ITEMS.items()):
        tk.Label(win, text=f"{item} (₹{price})").grid(row=i+1, column=0)
        var = tk.IntVar(value=0)
        tk.OptionMenu(win, var, *range(11)).grid(row=i+1, column=1)
        item_vars[item] = var

    # Pickup & Comments
    tk.Label(win, text="Pickup Time (HH:MM):").grid(row=len(MENU_ITEMS)+1, column=0)
    pickup_entry = tk.Entry(win)
    pickup_entry.grid(row=len(MENU_ITEMS)+1, column=1)

    tk.Label(win, text="Comments:").grid(row=len(MENU_ITEMS)+2, column=0)
    comment_entry = tk.Entry(win)
    comment_entry.grid(row=len(MENU_ITEMS)+2, column=1)

    def place_order():
        name = name_entry.get().strip()
        pickup = pickup_entry.get().strip()
        comments = comment_entry.get().strip()
        selections = {item: var.get() for item, var in item_vars.items()}

        if not name or not pickup:
            messagebox.showerror("Missing Info", "Enter name and pickup time.")
            return

        save_order(name, selections, pickup, comments)
        win.destroy()

    tk.Button(win, text="Place Order", command=place_order, bg="green", fg="white").grid(row=len(MENU_ITEMS)+3, columnspan=2, pady=10)

# ---------- View Menu ----------
def open_menu_window():
    win = tk.Toplevel(root)
    win.title("Menu")
    tk.Label(win, text="Today's Menu", font=("Arial", 14, "bold")).pack()
    for item, price in MENU_ITEMS.items():
        tk.Label(win, text=f"{item} — ₹{price}", font=("Arial", 12)).pack(anchor="w")

# ---------- Staff Login & Corner ----------
def open_login_window():
    win = tk.Toplevel(root)
    win.title("Staff Login")

    tk.Label(win, text="Username:").pack()
    user_entry = tk.Entry(win)
    user_entry.pack()
    tk.Label(win, text="Password:").pack()
    pass_entry = tk.Entry(win, show="*")
    pass_entry.pack()

    def authenticate():
        user = user_entry.get()
        passwd = pass_entry.get()
        if user == "admin" and passwd == "cts123":
            win.destroy()
            open_staff_window()
        else:
            messagebox.showerror("Access Denied", "Incorrect credentials.")

    tk.Button(win, text="Login", command=authenticate).pack(pady=5)

def open_staff_window():
    win = tk.Toplevel(root)
    win.title("Staff Corner")
    tk.Label(win, text="Current Orders", font=("Arial", 14, "bold")).pack()

    try:
        with open(cafe_orders_file, "r") as f:
            orders = json.load(f)
    except:
        orders = []

    # Ensure all orders have a status
    status_updated = False
    for order in orders:
        if 'status' not in order:
            order['status'] = 'Pending'
            status_updated = True
    if status_updated:
        with open(cafe_orders_file, "w") as f:
            json.dump(orders, f, indent=2)

    for idx, o in enumerate(orders):
        summary = (
            f"Order ID: {o['order_id']}\n"
            f"Name: {o['name']}\n"
            f"Items:\n  " + "\n  ".join(o['items']) + "\n"
            f"Total: ₹{o['total_price']}\n"
            f"Pickup: {o['pickup_time']}\n"
            f"Comments: {o['comments']}\n"
            f"Status: {o['status']}\n"
            f"{'-'*40}"
        )
        frame = tk.Frame(win)
        frame.pack(anchor="w", fill="x", padx=10, pady=2)
        tk.Label(frame, text=summary, justify="left", font=("Arial", 10)).pack(side="left")
        status_var = tk.StringVar(value=o['status'])
        status_menu = tk.OptionMenu(frame, status_var, "Pending", "Completed", "Cancelled")
        status_menu.pack(side="left", padx=5)
        def update_status(idx=idx, var=status_var):
            orders[idx]['status'] = var.get()
            with open(cafe_orders_file, "w") as f:
                json.dump(orders, f, indent=2)
            messagebox.showinfo("Status Updated", f"Order status changed to {var.get()}.")
        tk.Button(frame, text="Update Status", command=update_status).pack(side="left", padx=5)

# ---------- Search Orders ----------
def open_search_window():
    win = tk.Toplevel(root)
    win.title("Search Orders")

    tk.Label(win, text="Enter Order ID or Name:").pack(pady=5)
    query_entry = tk.Entry(win, width=30)
    query_entry.pack()
    result_label = tk.Label(win, text="", justify="left", font=("Arial", 10))
    result_label.pack(pady=10)

    def search_order():
        query = query_entry.get().strip().lower()
        try:
            with open(cafe_orders_file, "r") as f:
                orders = json.load(f)
            found = [o for o in orders if query in o['order_id'].lower() or query in o['name'].lower()]
            if found:
                result = "\n\n".join([
                    f"Order ID: {o.get('order_id', 'N/A')}\n"
                    f"Name: {o.get('name', 'N/A')}\n"
                    f"Items: {o.get('items', 'N/A')}\n"
                    f"Pickup Time: {o.get('pickup_time', 'N/A')}\n"
                    f"Comments: {o.get('comments', 'N/A')}\n"
                    f"Status: {o.get('status', 'Pending')}\n"
                    f"{'-'*30}"
                    for o in found
                ])
                result_label.config(text=result)
            else:
                result_label.config(text="No matching orders found.")
        except Exception as e:
            result_label.config(text=f"Error: {e}")

    tk.Button(win, text="Search", command=search_order).pack(pady=5)

# ---------- Main Window ----------
def main(selected_cafe=None):
    global root, MENU_ITEMS, cafe_orders_file
    # Load the correct menu file
    menu_file = f"menu_{selected_cafe}.json" if selected_cafe else "menu.json"
    try:
        with open(menu_file, "r") as f:
            menu_data = json.load(f)
        MENU_ITEMS = {item['item']: item['price'] for item in menu_data}
    except Exception as e:
        messagebox.showerror("Menu Error", f"Could not load menu for {selected_cafe}: {e}")
        MENU_ITEMS = {}
    # Set the correct orders file
    cafe_orders_file = f"orders_{selected_cafe}.json" if selected_cafe else "orders.json"
    # Start the main window
    root = tk.Tk()
    root.title(f"Smart CTS Café - {selected_cafe}")
    tk.Label(root, text=f"Welcome to CTS Café - {selected_cafe}", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Button(root, text="🛒 Customer Order", command=open_order_window, width=25).pack(pady=5)
    tk.Button(root, text="📋 View Menu", command=open_menu_window, width=25).pack(pady=5)
    tk.Button(root, text="🔐 Staff Corner", command=open_login_window, width=25).pack(pady=5)
    tk.Button(root, text="🔎 Search Order", command=open_search_window, width=25).pack(pady=5)
    root.mainloop()

main()
