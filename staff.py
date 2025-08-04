import tkinter as tk
from tkinter import messagebox
import json

# ---------- Staff Login ----------

def open_login_window():
    login_win = tk.Toplevel()
    login_win.title("Staff Login")

    tk.Label(login_win, text="Username:").pack(pady=5)
    user_entry = tk.Entry(login_win)
    user_entry.pack()

    tk.Label(login_win, text="Password:").pack(pady=5)
    pass_entry = tk.Entry(login_win, show="*")
    pass_entry.pack()

    def authenticate():
        user = user_entry.get()
        passwd = pass_entry.get()
        if user == "admin" and passwd == "cts123":
            login_win.destroy()
            open_staff_window()
        else:
            messagebox.showerror("Access Denied", "Incorrect credentials.")

    tk.Button(login_win, text="Login", command=authenticate).pack(pady=10)

# ---------- Staff Dashboard ----------

def open_staff_window():
    try:
        with open(cafe_orders_file, "r") as f:
            orders = json.load(f)
    except FileNotFoundError:
        orders = []

    # Ensure all orders have a status and save back to file if any were missing
    status_updated = False
    for order in orders:
        if 'status' not in order:
            order['status'] = 'Pending'
            status_updated = True
    if status_updated:
        with open(cafe_orders_file, "w") as f:
            json.dump(orders, f, indent=2)

    staff_win = tk.Toplevel()
    staff_win.title("Staff Corner")

    tk.Label(staff_win, text="Current Orders", font=("Arial", 14, "bold")).pack(pady=5)

    for idx, order in enumerate(orders):
        # Add status if missing
        if 'status' not in order:
            order['status'] = 'Pending'

        order_text = (
            f"Order ID: {order.get('order_id', 'N/A')}\n"
            f"Name: {order.get('name', 'N/A')}\n"
            f"Items: {order.get('items', 'N/A')}\n"
            f"Pickup Time: {order.get('pickup_time', 'N/A')}\n"
            f"Comments: {order.get('comments', 'N/A')}\n"
            f"Status: {order.get('status', 'Pending')}\n"
            f"{'-'*40}"
        )
        frame = tk.Frame(staff_win)
        frame.pack(anchor="w", fill="x", padx=10, pady=2)
        tk.Label(frame, text=order_text, justify="left", font=("Arial", 10)).pack(side="left")
        status_var = tk.StringVar(value=order['status'])
        status_menu = tk.OptionMenu(frame, status_var, "Pending", "Completed", "Cancelled")
        status_menu.pack(side="left", padx=5)
        def update_status(idx=idx, var=status_var):
            orders[idx]['status'] = var.get()
            with open(cafe_orders_file, "w") as f:
                json.dump(orders, f, indent=2)
            messagebox.showinfo("Status Updated", f"Order status changed to {var.get()}.")
        tk.Button(frame, text="Update Status", command=update_status).pack(side="left", padx=5)

    tk.Button(staff_win, text="🔎 Search Orders", command=open_search_window).pack(pady=10)

# ---------- Staff Order Search ----------

def open_search_window():
    search_win = tk.Toplevel()
    search_win.title("Search Orders")

    tk.Label(search_win, text="Enter Order ID or Name:").pack(pady=5)
    query_entry = tk.Entry(search_win, width=30)
    query_entry.pack()

    result_label = tk.Label(search_win, text="", justify="left", font=("Arial", 10), wraplength=400)
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

    tk.Button(search_win, text="Search", command=search_order).pack(pady=5)

def main(selected_cafe=None):
    global cafe_orders_file
    cafe_orders_file = f"orders_{selected_cafe}.json" if selected_cafe else "orders.json"
    root = tk.Tk()
    root.title("Staff Login")
    open_login_window()
    root.mainloop()
