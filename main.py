import tkinter as tk
from tkinter import messagebox

# Sample data
coffee_menu = {
    "Espresso": 2.50,
    "Latte": 3.50,
    "Cappuccino": 3.00
}

pastry_menu = {
    "Croissant": 2.00,
    "Muffin": 1.50,
    "Donut": 1.20
}

order = []

# GUI Setup
root = tk.Tk()
root.title("Coffee Shop Kiosk")
root.geometry("400x300")


# Functions
def add_item(item_name, price):
    confirm = messagebox.askyesno("Confirm Order", f"Add {item_name} (${price:.2f}) to your order?")
    if confirm:
        order.append((item_name, price))
        messagebox.showinfo("Added", f"{item_name} has been added!")
    else:
        return


def show_menu(menu, title):
    menu_win = tk.Toplevel(root)
    menu_win.title(title)
    menu_win.geometry("300x200")

    for item, price in menu.items():
        btn = tk.Button(menu_win, text=f"{item} - ${price:.2f}", command=lambda i=item, p=price: add_item(i, p))
        btn.pack(pady=5)


def view_order():
    if not order:
        messagebox.showinfo("Order", "Your order is empty.")
        return

    summary = "\n".join([f"{item} - ${price:.2f}" for item, price in order])
    total = sum(price for _, price in order)
    messagebox.showinfo("Your Order", f"{summary}\n\nTotal: ${total:.2f}")


def checkout():
    if not order:
        messagebox.showwarning("No Order", "You have no items to checkout.")
        return

    total = sum(price for _, price in order)
    confirm = messagebox.askyesno("Proceed to Payment", f"Total amount is ${total:.2f}\nProceed to pay?")
    if confirm:
        messagebox.showinfo("Payment Success", "Payment received. Thank you!")
        save_to_database()
        order.clear()
    else:
        return


def save_to_database():
    # Simulate saving to DB
    print("Order saved to database:")
    for item, price in order:
        print(f"- {item}: ${price:.2f}")


# Main Buttons
tk.Label(root, text="Welcome to the Coffee Kiosk!", font=("Arial", 16)).pack(pady=10)

tk.Button(root, text="Coffee Menu", command=lambda: show_menu(coffee_menu, "Coffee Menu")).pack(pady=5)
tk.Button(root, text="Pastry Menu", command=lambda: show_menu(pastry_menu, "Pastry Menu")).pack(pady=5)
tk.Button(root, text="View Order", command=view_order).pack(pady=5)
tk.Button(root, text="Checkout", command=checkout).pack(pady=5)
tk.Button(root, text="Exit", command=root.destroy).pack(pady=10)

root.mainloop()
