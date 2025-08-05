import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

selected_cafe = None
main_menu_frame = None

# Function to set the selected cafe and show main menu
def set_cafe(cafe):
    global selected_cafe
    selected_cafe = cafe
    show_main_menu()

# Function to launch customer GUI
def launch_customer():
    import main
    main.main(selected_cafe)

# Function to launch staff GUI
def launch_staff():
    import staff
    staff.main(selected_cafe)

root = tk.Tk()
root.title("Smart CTS Cafe System")
root.geometry("500x400")
root.configure(bg="#f5f5f5")

# Banner or logo (optional, use your own image path)
# logo = PhotoImage(file="logo.png")
# tk.Label(root, image=logo, bg="#f5f5f5").pack(pady=10)

label = tk.Label(root, text="Welcome to Smart CTS Cafe System", font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333")
label.pack(pady=20)

cafe_frame = tk.Frame(root, bg="#f5f5f5")
cafe_frame.pack(pady=10)
tk.Label(cafe_frame, text="Select Cafe:", font=("Arial", 13, "bold"), bg="#f5f5f5").pack(side="left", padx=5)
for cafe, name in zip(["cafeI", "cafeII", "cafeIII"], ["Cafe I", "Cafe II", "Cafe III"]):
    ttk.Button(cafe_frame, text=name, command=lambda c=cafe: set_cafe(c), width=12).pack(side="left", padx=8)

def show_main_menu():
    global main_menu_frame
    if main_menu_frame:
        main_menu_frame.destroy()
    main_menu_frame = tk.Frame(root, bg="#f5f5f5")
    main_menu_frame.pack(pady=20)
    tk.Label(main_menu_frame, text=f"Selected Cafe: {selected_cafe}", font=("Arial", 13, "bold"), bg="#f5f5f5", fg="#00796b").pack(pady=8)
    ttk.Button(main_menu_frame, text="Place an Order (Customer)", command=launch_customer, width=30).pack(pady=10)
    ttk.Button(main_menu_frame, text="Manage Orders (Staff)", command=launch_staff, width=30).pack(pady=10)
    ttk.Button(main_menu_frame, text="Exit", command=root.destroy, width=30).pack(pady=10)

# Footer
footer = tk.Label(root, text="© 2025 CTS Cafe | Powered by Python & Tkinter", font=("Arial", 9), bg="#f5f5f5", fg="#888")
footer.pack(side="bottom", pady=8)

root.mainloop()
