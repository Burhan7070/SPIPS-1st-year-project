import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import os

# Bank details
BANK_NAME = "Kotak Mahindra Bank"
ACCOUNT_NUMBER = "1234567890"
IFSC = "KKBK0001234"
ACCOUNT_HOLDER = "Star Aluminium Pvt. Ltd."

class Hotel:
    def __init__(self):
        self.rooms = {}
        self.available_rooms = {
            'standard': [101, 102, 103],
            'deluxe': [201, 202, 203],
            'executive': [301, 302, 303],
            'suite': [401, 402, 403]
        }
        self.room_price = {
            'standard': 2000,
            'deluxe': 4000,
            'executive': 6000,
            'suite': 8000
        }

    def checkin(self, name, address, phone, room_type, checkin_date):
        if not self.available_rooms.get(room_type):
            return False, f"{room_type.capitalize()} rooms are not available."
        room_number = self.available_rooms[room_type].pop(0)
        self.rooms[room_number] = {
            'name': name,
            'address': address,
            'phone': phone,
            'checkin': checkin_date,
            'room_type': room_type,
            'room_service': 0
        }
        return True, f"{name} checked in to room {room_number}."

    def add_room_service(self, room_number, service_choice_qty):
        menu = {
            1: ('Tea', 70),
            2: ('Coffee', 100),
            3: ('Juice', 50),
            4: ('Breakfast', 150),
            5: ('Lunch', 200)
        }
        if room_number not in self.rooms:
            return "Invalid room number or room not occupied."
        total_bill = 0
        for choice, qty in service_choice_qty.items():
            if choice in menu:
                total_bill += menu[choice][1] * qty
        self.rooms[room_number]['room_service'] += total_bill
        return f"Room service bill updated. Current total: ₹{self.rooms[room_number]['room_service']}"

    def get_occupied_rooms(self):
        return self.rooms

    def checkout(self, room_number):
        if room_number not in self.rooms:
            return None, "Invalid room number or room not occupied."
        checkin_date = self.rooms[room_number]['checkin']
        checkout_date = date.today()
        duration = (checkout_date - checkin_date).days
        duration = max(duration, 1)
        room_type = self.rooms[room_number]['room_type']
        room_cost_per_day = self.room_price[room_type]
        room_bill = room_cost_per_day * duration
        service_bill = self.rooms[room_number]['room_service']
        total_bill = room_bill + service_bill
        guest_info = self.rooms[room_number].copy()
        guest_info.update({
            'checkout': checkout_date,
            'duration': duration,
            'room_bill': room_bill,
            'service_bill': service_bill,
            'total_bill': total_bill
        })
        self.available_rooms[room_type].append(room_number)
        del self.rooms[room_number]
        return guest_info, None

class HotelGUI:
    def __init__(self, root):
        self.hotel = Hotel()
        self.root = root
        root.title("Hotel Management System")
        root.geometry("500x450")
        self.create_main_menu()

    def create_main_menu(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True, padx=10, pady=10)

        tk.Label(frame, text="Hotel Management System", font=("Arial", 16)).pack(pady=15)

        buttons = [
            ("Client Check-in", self.checkin_window),
            ("Room Service", self.room_service_window),
            ("View Occupied Rooms", self.view_occupied_window),
            ("Check-out", self.checkout_window)
        ]

        for text, cmd in buttons:
            tk.Button(frame, text=text, command=cmd, width=30).pack(pady=8)

    def checkin_window(self):
        win = tk.Toplevel(self.root)
        win.title("Client Check-in")
        win.geometry("400x400")

        labels = [
            "Name",
            "Address",
            "Phone (Required, digits only)",
            "Room Type (1-Standard, 2-Deluxe, 3-Executive, 4-Suite)",
            "Check-in Date (DD MM YYYY)"
        ]

        entries = []
        for label in labels:
            tk.Label(win, text=label).pack(anchor="w", padx=10, pady=4)
            entry = tk.Entry(win)
            entry.pack(padx=10, fill="x")
            entries.append(entry)

        def submit_checkin():
            try:
                name = entries[0].get()
                address = entries[1].get()
                phone = entries[2].get().strip()
                if not phone or not phone.isdigit():
                    raise ValueError("Phone number is mandatory and digits only.")
                phone = int(phone)
                room_type_map = {1: 'standard', 2: 'deluxe', 3: 'executive', 4: 'suite'}
                room_type = room_type_map.get(int(entries[3].get()))
                if not room_type:
                    raise ValueError("Invalid room type")
                d, m, y = map(int, entries[4].get().split())
                checkin_date = date(y, m, d)
                success, msg = self.hotel.checkin(name, address, phone, room_type, checkin_date)
                if success:
                    messagebox.showinfo("Success", msg)
                    win.destroy()
                else:
                    messagebox.showerror("Error", msg)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Submit", command=submit_checkin).pack(pady=20)

    def room_service_window(self):
        win = tk.Toplevel(self.root)
        win.title("Room Service")
        win.geometry("400x450")

        tk.Label(win, text="Enter Room Number").pack()
        room_entry = tk.Entry(win)
        room_entry.pack()

        menu = {
            1: ('Tea', 70),
            2: ('Coffee', 100),
            3: ('Juice', 50),
            4: ('Breakfast', 150),
            5: ('Lunch', 200)
        }

        tk.Label(win, text="Select Items and Quantity").pack()
        item_vars = {}
        qty_vars = {}

        for key, (item, price) in menu.items():
            var = tk.IntVar()
            qty = tk.IntVar(value=0)
            frame = tk.Frame(win)
            frame.pack(anchor='w')
            cb = tk.Checkbutton(frame, text=f"{item} ({price} Rs)", variable=var)
            cb.pack(side='left')
            tk.Label(frame, text="Quantity:").pack(side='left')
            qty_entry = tk.Entry(frame, textvariable=qty, width=5)
            qty_entry.pack(side='left')
            item_vars[key] = var
            qty_vars[key] = qty

        def submit_room_service():
            try:
                room_num = int(room_entry.get())
                service_items = {k: qty_vars[k].get() for k in menu if item_vars[k].get() == 1}
                service_items = {k: v for k, v in service_items.items() if v > 0}
                if not service_items:
                    messagebox.showerror("Error", "Select at least one item with quantity > 0")
                    return
                msg = self.hotel.add_room_service(room_num, service_items)
                messagebox.showinfo("Room Service", msg)
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Send to Kitchen", command=submit_room_service).pack(pady=10)

    def view_occupied_window(self):
        win = tk.Toplevel(self.root)
        win.title("Occupied Rooms")
        win.geometry("500x300")

        rooms = self.hotel.get_occupied_rooms()
        if not rooms:
            tk.Label(win, text="No rooms are currently occupied.").pack(pady=20)
            return

        tree = ttk.Treeview(win, columns=('Name', 'Phone', 'Room Type', 'Check-in Date'), show='headings')
        tree.heading('Name', text='Name')
        tree.heading('Phone', text='Phone')
        tree.heading('Room Type', text='Room Type')
        tree.heading('Check-in Date', text='Check-in Date')

        for col in ('Name', 'Phone', 'Room Type', 'Check-in Date'):
            tree.column(col, width=100)

        tree.pack(fill='both', expand=True)

        for room_num, info in rooms.items():
            tree.insert('', 'end', values=(info['name'], info['phone'], info['room_type'], info['checkin'].strftime('%d-%b-%Y')))

    def checkout_window(self):
        win = tk.Toplevel(self.root)
        win.title("Check-out")
        win.geometry("400x400")

        tk.Label(win, text="Enter Room Number to Check-out").pack(pady=10)
        room_entry = tk.Entry(win)
        room_entry.pack()

        def show_payment_bank_details(guest_info):
            scanner_win = tk.Toplevel(win)
            scanner_win.title("Bank Payment Details")
            scanner_win.geometry("420x300")

            tk.Label(scanner_win, text=f"Amount to Pay: ₹{guest_info['total_bill']}", font=('Arial', 14)).pack(pady=10)

            frame = tk.Frame(scanner_win, bd=2, relief='ridge')
            frame.pack(padx=10, pady=10, fill='both', expand=True)

            tk.Label(frame, text=f"Bank: {BANK_NAME}").pack(anchor='w', padx=10, pady=2)
            tk.Label(frame, text=f"A/c Number: {ACCOUNT_NUMBER}").pack(anchor='w', padx=10, pady=2)
            tk.Label(frame, text=f"IFSC: {IFSC}").pack(anchor='w', padx=10, pady=2)
            tk.Label(frame, text=f"Account Name: {ACCOUNT_HOLDER}").pack(anchor='w', padx=10, pady=2)

            tk.Label(scanner_win, text="(Copy and pay using your banking app)").pack()

            def mark_paid():
                messagebox.showinfo("Payment", "Payment marked as received!")
                scanner_win.destroy()
                win.destroy()
                self.show_checkout_details(guest_info)

            tk.Button(scanner_win, text="Mark as Paid", command=mark_paid).pack(pady=10)

        def submit_checkout():
            try:
                room_num = int(room_entry.get())
                guest_info, error = self.hotel.checkout(room_num)
                if error:
                    messagebox.showerror("Error", error)
                    return
                show_payment_bank_details(guest_info)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        tk.Button(win, text="Proceed to Checkout", command=submit_checkout).pack(pady=20)

    def show_checkout_details(self, info):
        details = f"""
Guest Name: {info['name']}
Address: {info['address']}
Phone: {info['phone']}
Check-in Date: {info['checkin'].strftime('%d-%b-%Y')}
Check-out Date: {info['checkout'].strftime('%d-%b-%Y')}
Days Stayed: {info['duration']}
Room Bill: ₹{info['room_bill']}
Room Service Bill: ₹{info['service_bill']}
------------------------------
Total Bill: ₹{info['total_bill']}
"""
        messagebox.showinfo("Bill Details", details)


if __name__ == '__main__':
    root = tk.Tk()
    app = HotelGUI(root)
    root.mainloop()
