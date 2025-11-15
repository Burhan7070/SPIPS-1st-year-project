import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import date

# Auto-update feature disabled (optional: pip install auto-update)
updater_enabled = False

class Hotel:
    def __init__(self):
        self.rooms = {}
        self.available_rooms = {
            "Standard": [101, 102, 103],
            "Deluxe": [201, 202, 203],
            "Executive": [301, 302, 303],
            "Suite": [401, 402, 403]
        }
        self.room_prices = {
            "Standard": 2000,
            "Deluxe": 4000,
            "Executive": 6000,
            "Suite": 8000
        }

    def checkin(self, details):
        name, adhar, phone, room_type, checkin_date = details
        typestr = room_type
        rooms_list = self.available_rooms.get(typestr)
        if rooms_list and len(rooms_list) > 0:
            room_number = rooms_list.pop(0)
            self.rooms[room_number] = {
                "name": name,
                "Adhar": adhar,
                "phone": phone,
                "checkin": checkin_date,
                "roomtype": typestr,
                "roomservice": 0
            }
            return room_number
        else:
            return None

    def roomservice(self, room_number, bill):
        if room_number in self.rooms:
            self.rooms[room_number]["roomservice"] += bill
            return True
        return False

    def display_rooms(self):
        return self.rooms

    def checkout(self, room_number):
        if room_number not in self.rooms:
            return None
        checkout_date = date.today()
        room_info = self.rooms[room_number]
        checkin_date = room_info["checkin"]
        duration = (checkout_date - checkin_date).days
        roomtype = room_info["roomtype"]
        priceperday = self.room_prices[roomtype]
        roombill = priceperday * duration
        servicebill = room_info["roomservice"]
        total = roombill + servicebill
        receipt = {
            "name": room_info["name"],
            "Adhar": room_info["Adhar"],
            "phone": room_info["phone"],
            "roomnumber": room_number,
            "checkin": checkin_date,
            "checkout": checkout_date,
            "days": duration,
            "roombill": roombill,
            "servicebill": servicebill,
            "total": total
        }
        self.available_rooms[roomtype].append(room_number)
        del self.rooms[room_number]
        return receipt

class HotelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Accommodation Management System")
        self.hotel = Hotel()
        self.build_menu()
        if updater_enabled:
            self.try_update()

    def build_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Welcome to Hotel System").pack(pady=10)
        tk.Button(self, text="Check-in", command=self.checkin_form).pack(fill='x', padx=5, pady=5)
        tk.Button(self, text="Room Service", command=self.room_service_form).pack(fill='x', padx=5, pady=5)
        tk.Button(self, text="View Occupied Rooms", command=self.show_rooms).pack(fill='x', padx=5, pady=5)
        tk.Button(self, text="Check-out", command=self.checkout_form).pack(fill='x', padx=5, pady=5)
        tk.Button(self, text="Exit", command=self.quit).pack(fill='x', padx=5, pady=5)

    def checkin_form(self):
        form = tk.Toplevel(self)
        form.title("Check-in")
        tk.Label(form, text="Name:").grid(row=0, column=0)
        name_entry = tk.Entry(form)
        name_entry.grid(row=0, column=1)
        tk.Label(form, text="Adhar:").grid(row=1, column=0)
        adhar_entry = tk.Entry(form)
        adhar_entry.grid(row=1, column=1)
        tk.Label(form, text="Phone:").grid(row=2, column=0)
        phone_entry = tk.Entry(form)
        phone_entry.grid(row=2, column=1)
        tk.Label(form, text="Room Type:").grid(row=3, column=0)
        room_type_var = tk.StringVar(form)
        room_type_var.set("Standard")
        tk.OptionMenu(form, room_type_var, *self.hotel.available_rooms.keys()).grid(row=3, column=1)
        tk.Label(form, text="Check-in date (YYYY-MM-DD):").grid(row=4, column=0)
        checkin_entry = tk.Entry(form)
        checkin_entry.grid(row=4, column=1)
        def submit():
            try:
                dt_parts = [int(x) for x in checkin_entry.get().split('-')]
                checkin_date = date(*dt_parts)
                room_number = self.hotel.checkin([
                    name_entry.get(),
                    adhar_entry.get(),
                    phone_entry.get(),
                    room_type_var.get(),
                    checkin_date,
                ])
                if room_number:
                    messagebox.showinfo("Success", f"Checked in {name_entry.get()} to room {room_number} on {checkin_date}")
                    form.destroy()
                else:
                    messagebox.showerror("Error", "Selected room not available.")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
        tk.Button(form, text="Submit", command=submit).grid(row=5, column=1)

    def room_service_form(self):
        room_number = simpledialog.askinteger("Room Service", "Enter room number:")
        if room_number not in self.hotel.rooms:
            messagebox.showerror("Error", "Invalid room number.")
            return
        menu = [("Poha", 30), ("Kachori", 25), ("Samosa", 25), ("Veg-Thali", 100), ("Coffee", 30), ("Tea", 10)]
        choices = []
        top = tk.Toplevel(self)
        top.title("Room Service")
        for i, (item, price) in enumerate(menu):
            var = tk.IntVar(top)
            tk.Checkbutton(top, text=f"{item} {price}", variable=var).grid(row=i, column=0, sticky='w')
            qty = tk.Entry(top)
            qty.grid(row=i, column=1)
            choices.append((var, qty, price))
        def submit():
            total = 0
            for var, qty, price in choices:
                if var.get():
                    try:
                        count = int(qty.get())
                        total += price * count
                    except:
                        pass
            self.hotel.roomservice(room_number, total)
            messagebox.showinfo("Bill", f"Room service bill: {total}")
            top.destroy()
        tk.Button(top, text="Submit", command=submit).grid(row=len(menu), column=1)

    def show_rooms(self):
        rooms = self.hotel.display_rooms()
        msg = ""
        if not rooms:
            msg = "No rooms occupied."
        else:
            for r, d in rooms.items():
                msg += f"Room {r}: {d['name']} ({d['phone']})\n"
        messagebox.showinfo("Occupied Rooms", msg)

    def checkout_form(self):
        room_number = simpledialog.askinteger("Checkout", "Enter room number:")
        receipt = self.hotel.checkout(room_number)
        if receipt is None:
            messagebox.showerror("Error", "Room not occupied or invalid number.")
        else:
            msg = (
                "--------- Receipt ---------\n"
                f"Name: {receipt['name']}\n"
                f"Adhar: {receipt['Adhar']}\n"
                f"Phone: {receipt['phone']}\n"
                f"Room No.: {receipt['roomnumber']}\n"
                f"Check-in: {receipt['checkin']}\n"
                f"Check-out: {receipt['checkout']}\n"
                f"Days Stayed: {receipt['days']}\n"
                f"Room Bill: {receipt['roombill']}\n"
                f"Service Bill: {receipt['servicebill']}\n"
                f"Total Bill: {receipt['total']}\n"
            )
            messagebox.showinfo("Receipt", msg)

    def try_update(self):
        # Auto-update feature disabled
        # To enable: pip install auto-update and uncomment the code below
        pass
        # try:
        #     updater = Updater('yourusername/yourrepo/latest')  # Change to your repo
        #     if updater.check_update():
        #         updater.perform_update()
        #         messagebox.showinfo("Update", "App updated to latest version!")
        # except Exception as e:
        #     print(f"Auto-update error: {e}")

if __name__ == '__main__':
    app = HotelApp()
    app.mainloop()
