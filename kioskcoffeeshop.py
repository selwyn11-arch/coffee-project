import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime

# Global configuration
WINDOW_WIDTH = 420
WINDOW_HEIGHT = 540
order = []

# Menus
coffee_menu = {
	"Espresso": 120,
	"Latte": 120,
	"Cappuccino": 100,
}

pastry_menu = {
	"Croissant": 60,
	"Muffin": 50,
	"Donut": 60,
}


# Main Kiosk Launch
def launch_main_menu():
	root = tk.Tk()
	root.title("A&R Coffee Shop Kiosk")
	root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
	root.resizable(False, False)

	# Background Image
	bg_image = Image.open("images/main_background_image.jpg").resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.LANCZOS)
	bg_photo = ImageTk.PhotoImage(bg_image)

	canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
	canvas.pack(fill="both", expand=True)
	canvas.create_image(0, 0, image=bg_photo, anchor="nw")

	# Font and Button Styling
	header_font = ("Comic Sans MS", 18, "bold")
	sub_font = ("Comic Sans MS", 12)
	button_style = {
		"font": sub_font,
		"bg": "#6F4E37",
		"fg": "white",
		"activebackground": "#8B5E3C",
		"width": 24,
		"bd": 2,
		"relief": "groove"
	}

	# Add item to order with confirmation
	def add_item(item_name, price):
		if messagebox.askyesno("Confirm Order", f"Add {item_name} (php{price:.2f}) to your order?"):
			order.append((item_name, price))
			messagebox.showinfo("Added", f"{item_name} has been added!")

	# Display a menu (coffee or pastry)
	def show_menu(menu, title):
		menu_win = tk.Toplevel(root)
		menu_win.title(title)
		menu_win.geometry(f"700x{WINDOW_HEIGHT}")
		menu_win.resizable(False, False)

		# Background and layout based on menu type
		if title == "Pastry Menu":
			bg_path, bg_content, bg_title, frame_x, frame_y = "images/pastry_background_image.jpg", "#c78e49", "#c78e49", 150, 125
		else:
			bg_path, bg_content, bg_title, frame_x, frame_y = "images/coffeemenu_background_image.jpg", "white", "#6F4E37", 520, 100

		menu_bg_image = Image.open(bg_path).resize((700, WINDOW_HEIGHT), Image.LANCZOS)
		menu_bg_photo = ImageTk.PhotoImage(menu_bg_image)

		canvas = tk.Canvas(menu_win, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
		canvas.pack(fill="both", expand=True)
		canvas.create_image(0, 0, image=menu_bg_photo, anchor="nw")
		canvas.image = menu_bg_photo  # Prevent garbage collection

		# Menu frame with buttons
		frame = tk.Frame(menu_win, bg=bg_content, padx=10)
		canvas.create_window(frame_x, frame_y, window=frame, anchor="n")

		tk.Label(frame, text=title, font=header_font, bg=bg_title, fg="white").pack(pady=10)

		for item, price in menu.items():
			tk.Button(frame, text=f"{item} - php{price:.2f}",
					  command=lambda i=item, p=price: add_item(i, p), **button_style).pack(pady=6)

		tk.Button(frame, text="Back", command=menu_win.destroy, **button_style).pack(pady=20)

	# Display current order summary
	def view_order():
		if not order:
			messagebox.showinfo("Order", "Your order is empty.")
			return
		summary = "\n".join([f"{item} - php{price:.2f}" for item, price in order])
		total = sum(price for _, price in order)
		messagebox.showinfo("Your Order", f"{summary}\n\nTotal: php{total:.2f}")

	# Checkout and show receipt
	def checkout():
		if not order:
			messagebox.showwarning("No Order", "You have no items to checkout.")
			return

		total = sum(price for _, price in order)
		if messagebox.askyesno("Proceed to Payment", f"Total amount is php{total:.2f}\nProceed to pay?"):
			save_to_database()
			show_receipt()
			order.clear()

	# Placeholder for database interaction
	def save_to_database():
		print("Order saved to database:")
		for item, price in order:
			print(f"- {item}: php{price:.2f}")

	# Generate and display the receipt
	def show_receipt():
		receipt_win = tk.Toplevel()
		receipt_win.title("Receipt")
		receipt_win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
		receipt_win.configure(bg="#FFF8DC")

		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		tk.Label(receipt_win, text="☕ A&R Coffee Receipt ☕", font=header_font, bg="#FFF8DC", fg="#3B2F2F").pack(pady=10)
		tk.Label(receipt_win, text=now, font=("Arial", 10), bg="#FFF8DC").pack(pady=5)

		receipt_text = tk.Text(receipt_win, width=45, height=15, font=("Courier", 10),
							   bg="#fdf5e6", relief="sunken", bd=2)
		receipt_text.pack(pady=10)
		receipt_text.insert("end", f"{'Item':<25}{'Price'}\n")
		receipt_text.insert("end", "-" * 35 + "\n")

		total = 0
		for item, price in order:
			receipt_text.insert("end", f"{item:<25}php{price:.2f}\n")
			total += price

		receipt_text.insert("end", "-" * 35 + "\n")
		receipt_text.insert("end", f"{'TOTAL':<25}php{total:.2f}\n\n")
		receipt_text.insert("end", "Thank you for your visit!")
		receipt_text.config(state="disabled")

		tk.Button(receipt_win, text="Back", command=receipt_win.destroy, **button_style).pack(pady=5)
		tk.Button(receipt_win, text="Close", command=receipt_win.destroy, **button_style).pack(pady=5)

	# Main menu layout
	header_label = tk.Label(root, text="A&R Coffee Kiosk", font=header_font, bg="#FFF8DC", fg="#3B2F2F", padx=20)
	canvas.create_window(WINDOW_WIDTH // 2, 40, window=header_label)

	button_frame = tk.Frame(root, bg="#F5F5F5", padx=10, pady=10)
	canvas.create_window(WINDOW_WIDTH // 2, 240, window=button_frame)

	tk.Button(button_frame, text="☕ Coffee Menu", command=lambda: show_menu(coffee_menu, "Coffee Menu"),
			  **button_style).pack(pady=5)
	tk.Button(button_frame, text="🥐 Pastry Menu", command=lambda: show_menu(pastry_menu, "Pastry Menu"),
			  **button_style).pack(pady=5)
	tk.Button(button_frame, text="📝 View Order", command=view_order, **button_style).pack(pady=5)
	tk.Button(button_frame, text="💳 Checkout", command=checkout, **button_style).pack(pady=5)

	exit_button = tk.Button(root, text="🚪 Exit", command=root.destroy, **button_style)
	canvas.create_window(WINDOW_WIDTH // 2, 480, window=exit_button)

	root.mainloop()


# Initial Welcome Screen
def show_start_screen():
	start_window = tk.Tk()
	start_window.title("Start Order")
	start_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
	start_window.resizable(False, False)

	# Background setup
	bg_image = Image.open("images/welcome_background_image.jpg").resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.LANCZOS)
	bg_photo = ImageTk.PhotoImage(bg_image)

	canvas = tk.Canvas(start_window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
	canvas.pack(fill="both", expand=True)
	canvas.create_image(0, 0, image=bg_photo, anchor="nw")

	# Start button
	start_button = tk.Button(start_window, text="Start Order", font=("Comic Sans MS", 14, "bold"),
							 bg="#6F4E37", fg="white", width=20, activebackground="#8B5E3C",
							 command=lambda: [start_window.destroy(), launch_main_menu()])
	canvas.create_window(WINDOW_WIDTH // 2, 480, window=start_button)

	start_window.mainloop()


# Launch the start screen
show_start_screen()
