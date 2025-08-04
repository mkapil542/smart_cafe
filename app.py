import tkinter as tk
from tkinter import messagebox

selected_cafe = None

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

label = tk.Label(root, text="Welcome to Smart CTS Cafe System", font=("Arial", 16, "bold"))
label.pack(pady=20)

cafe_frame = tk.Frame(root)
cafe_frame.pack(pady=10)
tk.Label(cafe_frame, text="Select Cafe:", font=("Arial", 12)).pack(side="left", padx=5)
tk.Button(cafe_frame, text="Cafe I", command=lambda: set_cafe('cafeI'), width=10).pack(side="left", padx=5)
tk.Button(cafe_frame, text="Cafe II", command=lambda: set_cafe('cafeII'), width=10).pack(side="left", padx=5)
tk.Button(cafe_frame, text="Cafe III", command=lambda: set_cafe('cafeIII'), width=10).pack(side="left", padx=5)

main_menu_frame = None

def show_main_menu():
    global main_menu_frame
    if main_menu_frame:
        main_menu_frame.destroy()
    main_menu_frame = tk.Frame(root)
    main_menu_frame.pack(pady=10)
    tk.Label(main_menu_frame, text=f"Selected Cafe: {selected_cafe}", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Button(main_menu_frame, text="Place an Order (Customer)", command=launch_customer, width=30, height=2).pack(pady=10)
    tk.Button(main_menu_frame, text="Manage Orders (Staff)", command=launch_staff, width=30, height=2).pack(pady=10)

root.mainloop()
