import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
from tkinter import simpledialog
class BakeryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Bakery Management System")
        self.master.geometry("800x600")

        self.inventory = {}
        self.current_order = []

        self.create_widgets()
        self.load_inventory()

    def create_widgets(self):
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Inventory tab
        self.inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_frame, text="Inventory")

        # Order tab
        self.order_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.order_frame, text="Order")

        self.setup_inventory_tab()
        self.setup_order_tab()

    def setup_inventory_tab(self):
        # Item entry
        ttk.Label(self.inventory_frame, text="Item:").grid(row=0, column=0, padx=5, pady=5)
        self.item_entry = ttk.Entry(self.inventory_frame)
        self.item_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.inventory_frame, text="Price:").grid(row=0, column=2, padx=5, pady=5)
        self.price_entry = ttk.Entry(self.inventory_frame)
        self.price_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(self.inventory_frame, text="Add Item", command=self.add_item).grid(row=0, column=4, padx=5, pady=5)

        # Inventory list
        self.inventory_tree = ttk.Treeview(self.inventory_frame, columns=("Item", "Price"), show="headings")
        self.inventory_tree.heading("Item", text="Item")
        self.inventory_tree.heading("Price", text="Price")
        self.inventory_tree.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")

        # Buttons for modifying inventory
        ttk.Button(self.inventory_frame, text="Delete Item", command=self.delete_item).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(self.inventory_frame, text="Modify Item", command=self.modify_item).grid(row=2, column=1, padx=5, pady=5)

        self.inventory_frame.grid_columnconfigure(1, weight=1)
        self.inventory_frame.grid_rowconfigure(1, weight=1)

    def setup_order_tab(self):
        # Order list
        self.order_tree = ttk.Treeview(self.order_frame, columns=("Item", "Price", "Quantity", "Subtotal"), show="headings")
        self.order_tree.heading("Item", text="Item")
        self.order_tree.heading("Price", text="Price")
        self.order_tree.heading("Quantity", text="Quantity")
        self.order_tree.heading("Subtotal", text="Subtotal")
        self.order_tree.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        # Item selection
        ttk.Label(self.order_frame, text="Select Item:").grid(row=1, column=0, padx=5, pady=5)
        self.item_var = tk.StringVar()
        self.item_combobox = ttk.Combobox(self.order_frame, textvariable=self.item_var)
        self.item_combobox.grid(row=1, column=1, padx=5, pady=5)
        

        ttk.Label(self.order_frame, text="Quantity:").grid(row=1, column=2, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(self.order_frame)
        self.quantity_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(self.order_frame, text="Add to Order", command=self.add_to_order).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        ttk.Button(self.order_frame, text="Remove from Order", command=self.remove_from_order).grid(row=2, column=2, columnspan=2, padx=5, pady=5)

        ttk.Label(self.order_frame, text="Total:").grid(row=3, column=0, padx=5, pady=5)
        self.total_label = ttk.Label(self.order_frame, text="DZD0.00")
        self.total_label.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(self.order_frame, text="Finish Order", command=self.finish_order).grid(row=3, column=2, columnspan=2, padx=5, pady=5)

        self.order_frame.grid_columnconfigure(1, weight=1)
        self.order_frame.grid_rowconfigure(0, weight=1)

    def load_inventory(self):
        try:
            with open("inventory.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    self.inventory[row[0]] = float(row[1])
                    self.inventory_tree.insert("", "end", values=row)
            self.update_item_combobox()
        except FileNotFoundError:
            pass

    def save_inventory(self):
        with open("inventory.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for item, price in self.inventory.items():
                writer.writerow([item, price])

    def add_item(self):
        item = self.item_entry.get()
        price = self.price_entry.get()
        if item and price:
            try:
                price = float(price)
                self.inventory[item] = price
                self.inventory_tree.insert("", "end", values=(item, f"DZD{price:.2f}"))
                self.item_entry.delete(0, "end")
                self.price_entry.delete(0, "end")
                self.save_inventory()
                self.update_item_combobox()
            except ValueError:
                messagebox.showerror("Error", "Invalid price")
        else:
            messagebox.showerror("Error", "Please enter both item and price")

    def delete_item(self):
        selected = self.inventory_tree.selection()
        if selected:
            item = self.inventory_tree.item(selected)['values'][0]
            del self.inventory[item]
            self.inventory_tree.delete(selected)
            self.save_inventory()
            self.update_item_combobox()
        else:
            messagebox.showerror("Error", "Please select an item to delete")

    def modify_item(self):
        selected = self.inventory_tree.selection()
        if selected:
            item = self.inventory_tree.item(selected)['values'][0]
            new_price = simpledialog.askfloat("Modify Item", f"Enter new price for {item}:")
            if new_price is not None:
                self.inventory[item] = new_price
                self.inventory_tree.item(selected, values=(item, f"DZD{new_price:.2f}"))
                self.save_inventory()
                self.update_item_combobox()
        else:
            messagebox.showerror("Error", "Please select an item to modify")

    def update_item_combobox(self):
        self.item_combobox['values'] = list(self.inventory.keys())

    def update_price(self, event):
        selected_item = self.item_var.get()
        if selected_item in self.inventory:
            price = self.inventory[selected_item]
            self.price_label.config(text=f"DZD{price:.2f}")

    def add_to_order(self):
        item = self.item_var.get()
        quantity = self.quantity_entry.get()
        if item and quantity:
            try:
                quantity = int(quantity)
                price = self.inventory[item]
                subtotal = price * quantity
                self.current_order.append((item, price, quantity, subtotal))
                self.order_tree.insert("", "end", values=(item, f"DZD{price:.2f}", quantity, f"DZD{subtotal:.2f}"))
                self.update_total()
                self.quantity_entry.delete(0, "end")
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity")
        else:
            messagebox.showerror("Error", "Please select an item and enter quantity")

    def remove_from_order(self):
        selected = self.order_tree.selection()
        if selected:
            try:
                selected_item = self.order_tree.item(selected)['values'][0]
                self.order_tree.delete(selected)
                self.current_order = [item for item in self.current_order if item[0] != selected_item]
                self.update_total()
            except (IndexError, tk.TclError):
                messagebox.showerror("Error", "Failed to remove item. Please try again.")
        else:
            messagebox.showerror("Error", "Please select an item to remove")

    def update_total(self):
        total = sum(item[3] for item in self.current_order)
        self.total_label.config(text=f"DZD{total:.2f}")

    def finish_order(self):
        if self.current_order:
            with open("orders.csv", "a", newline="") as f:
                writer = csv.writer(f)
                for item in self.current_order:
                    writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), item[0], item[2]])
            messagebox.showinfo("Order Completed", "Order has been saved to orders.csv")
            self.current_order.clear()
            self.order_tree.delete(*self.order_tree.get_children())
            self.update_total()
        else:
            messagebox.showerror("Error", "No items in the current order")

if __name__ == "__main__":
    root = tk.Tk()
    app = BakeryApp(root)
    root.mainloop()