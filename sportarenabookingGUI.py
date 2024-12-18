import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Data Storage
facilities = {}

# Functions
def create_facility():
    facility_name = facility_name_entry.get()
    if not facility_name:
        messagebox.showerror("Error", "Facility name cannot be empty.")
        return

    if facility_name in facilities:
        messagebox.showerror("Error", f"Facility '{facility_name}' already exists.")
    else:
        facilities[facility_name] = {"hourly_rate": 0, "bookings": []}
        messagebox.showinfo("Success", f"Facility '{facility_name}' created successfully.")
        facility_name_entry.delete(0, tk.END)

def view_facilities():
    if not facilities:
        messagebox.showinfo("Facilities", "No facilities available.")
        return

    facilities_list = "\n".join(facilities.keys())
    messagebox.showinfo("Facilities", f"Available Facilities:\n{facilities_list}")

def set_hourly_rate():
    facility_name = facility_name_entry.get()
    hourly_rate = hourly_rate_entry.get()

    if not facility_name or not hourly_rate:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    if facility_name not in facilities:
        messagebox.showerror("Error", f"Facility '{facility_name}' does not exist.")
    else:
        try:
            hourly_rate = float(hourly_rate)
            facilities[facility_name]["hourly_rate"] = hourly_rate
            messagebox.showinfo("Success", f"Hourly rate for '{facility_name}' set to RM {hourly_rate:.2f}.")
            hourly_rate_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Hourly rate must be a number.")

def create_booking():
    facility_name = facility_name_entry.get()
    user = user_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()

    if not facility_name or not user or not start_time or not end_time:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    if facility_name not in facilities:
        messagebox.showerror("Error", f"Facility '{facility_name}' does not exist.")
        return

    try:
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
        if end_time <= start_time:
            messagebox.showerror("Error", "End time must be after start time.")
            return
    except ValueError:
        messagebox.showerror("Error", "Invalid date/time format. Use 'YYYY-MM-DD HH:MM'.")
        return

    # Check for overlapping bookings
    for booking in facilities[facility_name]["bookings"]:
        if not (end_time <= booking["start_time"] or start_time >= booking["end_time"]):
            messagebox.showerror("Error", f"Time slot overlaps with an existing booking by {booking['user']}.")
            return

    # Calculate cost
    hours = (end_time - start_time).total_seconds() / 3600
    cost = hours * facilities[facility_name]["hourly_rate"]

    # Add booking
    facilities[facility_name]["bookings"].append({
        "user": user,
        "start_time": start_time,
        "end_time": end_time,
        "cost": cost,
    })

    messagebox.showinfo(
        "Success",
        f"Booking confirmed for '{facility_name}' from {start_time} to {end_time} by {user}. Cost: RM {cost:.2f}."
    )
    user_entry.delete(0, tk.END)
    start_time_entry.delete(0, tk.END)
    end_time_entry.delete(0, tk.END)

def view_bookings():
    facility_name = facility_name_entry.get()
    if not facility_name:
        messagebox.showerror("Error", "Please enter the facility name.")
        return

    if facility_name not in facilities:
        messagebox.showerror("Error", f"Facility '{facility_name}' does not exist.")
        return

    bookings = facilities[facility_name]["bookings"]
    if not bookings:
        messagebox.showinfo("Bookings", f"No bookings for facility '{facility_name}'.")
        return

    bookings_list = "\n".join([
        f"User: {b['user']}, Start: {b['start_time']}, End: {b['end_time']}, Cost: RM {b['cost']:.2f}"
        for b in bookings
    ])
    messagebox.showinfo("Bookings", f"Bookings for '{facility_name}':\n{bookings_list}")

def update_booking():
    facility_name = facility_name_entry.get()
    user = user_entry.get()
    new_start_time = new_start_time_entry.get()
    new_end_time = new_end_time_entry.get()

    if not facility_name or not user or not new_start_time or not new_end_time:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    if facility_name not in facilities:
        messagebox.showerror("Error", f"Facility '{facility_name}' does not exist.")
        return

    try:
        new_start_time = datetime.strptime(new_start_time, "%Y-%m-%d %H:%M")
        new_end_time = datetime.strptime(new_end_time, "%Y-%m-%d %H:%M")
        if new_end_time <= new_start_time:
            messagebox.showerror("Error", "End time must be after start time.")
            return
    except ValueError:
        messagebox.showerror("Error", "Invalid date/time format. Use 'YYYY-MM-DD HH:MM'.")
        return

    for booking in facilities[facility_name]["bookings"]:
        if booking["user"] == user:
            # Update booking
            booking["start_time"] = new_start_time
            booking["end_time"] = new_end_time
            hours = (new_end_time - new_start_time).total_seconds() / 3600
            booking["cost"] = hours * facilities[facility_name]["hourly_rate"]
            messagebox.showinfo("Success", f"Booking updated successfully for '{user}'.")
            new_start_time_entry.delete(0, tk.END)
            new_end_time_entry.delete(0, tk.END)
            return

    messagebox.showerror("Error", "No matching booking found.")

def delete_booking():
    facility_name = facility_name_entry.get()
    user = user_entry.get()
    start_time = start_time_entry.get()

    if not facility_name or not user or not start_time:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    if facility_name not in facilities:
        messagebox.showerror("Error", f"Facility '{facility_name}' does not exist.")
        return

    try:
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    except ValueError:
        messagebox.showerror("Error", "Invalid date/time format. Use 'YYYY-MM-DD HH:MM'.")
        return

    for booking in facilities[facility_name]["bookings"]:
        if booking["user"] == user and booking["start_time"] == start_time:
            facilities[facility_name]["bookings"].remove(booking)
            messagebox.showinfo("Success", f"Booking deleted successfully for '{user}'.")
            return

    messagebox.showerror("Error", "No matching booking found.")

def delete_facility():
    facility_name = facility_name_entry.get()
    if not facility_name:
        messagebox.showerror("Error", "Please enter the facility name.")
        return

    if facility_name not in facilities:
        messagebox.showerror("Error", f"Facility '{facility_name}' does not exist.")
    else:
        del facilities[facility_name]
        messagebox.showinfo("Success", f"Facility '{facility_name}' deleted successfully.")
        facility_name_entry.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Sports Arena Booking System")

# Input Fields
tk.Label(root, text="Facility Name:").grid(row=0, column=0)
facility_name_entry = tk.Entry(root)
facility_name_entry.grid(row=0, column=1)

tk.Label(root, text="Hourly Rate (RM):").grid(row=1, column=0)
hourly_rate_entry = tk.Entry(root)
hourly_rate_entry.grid(row=1, column=1)

tk.Label(root, text="User:").grid(row=2, column=0)
user_entry = tk.Entry(root)
user_entry.grid(row=2, column=1)

tk.Label(root, text="Start Time (YYYY-MM-DD HH:MM):").grid(row=3, column=0)
start_time_entry = tk.Entry(root)
start_time_entry.grid(row=3, column=1)

tk.Label(root, text="End Time (YYYY-MM-DD HH:MM):").grid(row=4, column=0)
end_time_entry = tk.Entry(root)
end_time_entry.grid(row=4, column=1)

tk.Label(root, text="New Start Time (YYYY-MM-DD HH:MM):").grid(row=5, column=0)
new_start_time_entry = tk.Entry(root)
new_start_time_entry.grid(row=5, column=1)

tk.Label(root, text="New End Time (YYYY-MM-DD HH:MM):").grid(row=6, column=0)
new_end_time_entry = tk.Entry(root)
new_end_time_entry.grid(row=6, column=1)

# Buttons
tk.Button(root, text="Create Facility", command=create_facility).grid(row=7, column=0)
tk.Button(root, text="View Facilities", command=view_facilities).grid(row=7, column=1)
tk.Button(root, text="Set Hourly Rate", command=set_hourly_rate).grid(row=8, column=0)
tk.Button(root, text="Create Booking", command=create_booking).grid(row=8, column=1)
tk.Button(root, text="View Bookings", command=view_bookings).grid(row=9, column=0)
tk.Button(root, text="Update Booking", command=update_booking).grid(row=9, column=1)
tk.Button(root, text="Delete Booking", command=delete_booking).grid(row=10, column=0)
tk.Button(root, text="Delete Facility", command=delete_facility).grid(row=10, column=1)

# Run the GUI
root.mainloop()







