import tkinter as tk
import customtkinter as ctk
from datetime import datetime

# Function to calculate total weight and brass
def calculate_total_weight_and_brass():
    try:
        weight_before_load = float(entry_weight_before_load.get())
        weight_after_load = float(entry_weight_after_load.get())
        total_weight_tonnes = (weight_after_load - weight_before_load) / 1000
        brass = (weight_after_load - weight_before_load) / 4

        entry_total_weight_tonnes.configure(state='normal')
        entry_total_weight_tonnes.delete(0, tk.END)
        entry_total_weight_tonnes.insert(0, f"{total_weight_tonnes:.2f} tonnes")
        entry_total_weight_tonnes.configure(state='disabled')

        entry_brass.configure(state='normal')
        entry_brass.delete(0, tk.END)
        entry_brass.insert(0, f"{brass:.2f}")
        entry_brass.configure(state='disabled')
    except ValueError:
        entry_total_weight_tonnes.configure(state='normal')
        entry_total_weight_tonnes.delete(0, tk.END)
        entry_total_weight_tonnes.insert(0, "Error")
        entry_total_weight_tonnes.configure(state='disabled')

        entry_brass.configure(state='normal')
        entry_brass.delete(0, tk.END)
        entry_brass.insert(0, "Error")
        entry_brass.configure(state='disabled')

# Function to submit the form
def submit_form():
    bill_no = entry_bill_no.get()
    name = entry_name.get()
    driver_name = entry_driver_name.get()
    time = entry_time.get()
    date = entry_date.get()
    vehicle_number = entry_vehicle_number.get()
    weight_before_load = entry_weight_before_load.get()
    weight_after_load = entry_weight_after_load.get()
    total_weight_tonnes = entry_total_weight_tonnes.get()
    brass = entry_brass.get()
    sizes_selected = [size.get() for size in size_vars if size.get()]

    # Here you can add code to handle the submitted data, like saving it to a file or database
    print("Form Submitted:")
    print(f"Bill No.: {bill_no}")
    print(f"Name: {name}")
    print(f"Driver Name: {driver_name}")
    print(f"Time: {time}")
    print(f"Date: {date}")
    print(f"Vehicle Number: {vehicle_number}")
    print(f"Weight Before Load: {weight_before_load}")
    print(f"Weight After Load: {weight_after_load}")
    print(f"Total Weight in tonnes: {total_weight_tonnes}")
    print(f"Total Weight in Brass: {brass}")
    print(f"Selected Sizes: {', '.join(map(str, sizes_selected))} mm")

# Function to print the receipt
def print_receipt():
    print("Receipt Printed")

# Function to generate a report
def generate_report():
    print("Report Generated")

# Function to refresh the form
def refresh_form():
    entry_bill_no.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_vehicle_number.delete(0, tk.END)
    entry_driver_name.delete(0, tk.END)
    entry_weight_before_load.delete(0, tk.END)
    entry_weight_after_load.delete(0, tk.END)
    entry_total_weight_tonnes.configure(state='normal')
    entry_total_weight_tonnes.delete(0, tk.END)
    entry_total_weight_tonnes.configure(state='disabled')
    entry_brass.configure(state='normal')
    entry_brass.delete(0, tk.END)
    entry_brass.configure(state='disabled')
    for size_var in size_vars:
        size_var.set(0)
    refresh_date_time()

# Function to refresh the date and time
def refresh_date_time():
    current_time = datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.now().strftime("%d/%m/%Y")
    entry_time.configure(state='normal')
    entry_time.delete(0, tk.END)
    entry_time.insert(0, current_time)
    entry_time.configure(state='disabled')
    entry_date.configure(state='normal')
    entry_date.delete(0, tk.END)
    entry_date.insert(0, current_date)
    entry_date.configure(state='disabled')

# Creating the main window
root = ctk.CTk()
root.title("Stone Crusher")
root.geometry("1000x700")

# Set custom tkinter color mode to light
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Title Label
title_label = ctk.CTkLabel(root, text="Ashirwad Stone Crusher, Junner", font=ctk.CTkFont(size=30, weight="bold"))
title_label.pack(pady=10)
quotation_label = ctk.CTkLabel(root, text="Cotation", font=ctk.CTkFont(size=24))
quotation_label.pack(pady=7)

# Navigation Bar
nav_frame = ctk.CTkFrame(root, height=40, bg_color="transparent")
nav_frame.pack(fill='x')

report_button = ctk.CTkButton(nav_frame, text="Report", font=ctk.CTkFont(size=16), command=generate_report)
report_button.pack(side='right', padx=10, pady=5)

print_button = ctk.CTkButton(nav_frame, text="Print Receipt", font=ctk.CTkFont(size=16), command=print_receipt)
print_button.pack(side='right', padx=10, pady=5)

add_vehicle_button = ctk.CTkButton(nav_frame, text="Add Vehicle", font=ctk.CTkFont(size=16))
add_vehicle_button.pack(side='right', padx=10, pady=5)

home_button = ctk.CTkButton(nav_frame, text="Home", font=ctk.CTkFont(size=16), command=refresh_form)
home_button.pack(side='right', padx=10, pady=5)


# Frame for the input fields
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=30, fill="both", expand=True)

# Bill No.
bill_no_label = ctk.CTkLabel(frame, text="Bill No.:", font=ctk.CTkFont(size=18))
bill_no_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_bill_no = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18))
entry_bill_no.grid(row=0, column=1, padx=10, pady=10)

# Time
time_label = ctk.CTkLabel(frame, text="Time:", font=ctk.CTkFont(size=18))
time_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
entry_time = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18), state='disabled')
entry_time.grid(row=0, column=3, padx=10, pady=10)

# Date
date_label = ctk.CTkLabel(frame, text="Date:", font=ctk.CTkFont(size=18))
date_label.grid(row=0, column=4, padx=10, pady=10, sticky="w")
entry_date = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18), state='disabled')
entry_date.grid(row=0, column=5, padx=10, pady=10)
refresh_date_time_button = ctk.CTkButton(frame, text="⟳", width=30, font=ctk.CTkFont(size=18), command=refresh_date_time)
refresh_date_time_button.grid(row=0, column=6, padx=10, pady=10)

# Name
name_label = ctk.CTkLabel(frame, text="Name:", font=ctk.CTkFont(size=18))
name_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_name = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18))
entry_name.grid(row=1, column=1, padx=10, pady=10)

# Vehicle Number
vehicle_number_label = ctk.CTkLabel(frame, text="Vehicle Number:", font=ctk.CTkFont(size=18))
vehicle_number_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")
entry_vehicle_number = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18))
entry_vehicle_number.grid(row=1, column=3, padx=10, pady=10)

# Driver Name
driver_name_label = ctk.CTkLabel(frame, text="Driver Name:", font=ctk.CTkFont(size=18))
driver_name_label.grid(row=1, column=4, padx=10, pady=10, sticky="w")
entry_driver_name = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18))
entry_driver_name.grid(row=1, column=5, padx=10, pady=10)

# Weight Before Load
weight_before_load_label = ctk.CTkLabel(frame, text="Weight Before Load (kg):", font=ctk.CTkFont(size=18))
weight_before_load_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_weight_before_load = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18))
entry_weight_before_load.grid(row=2, column=1, padx=10, pady=10)

# Weight After Load
weight_after_load_label = ctk.CTkLabel(frame, text="Weight After Load (kg):", font=ctk.CTkFont(size=18))
weight_after_load_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")
entry_weight_after_load = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18))
entry_weight_after_load.grid(row=2, column=3, padx=10, pady=10)
calculate_button = ctk.CTkButton(frame, text="=", width=30, font=ctk.CTkFont(size=18), command=calculate_total_weight_and_brass)
calculate_button.grid(row=2, column=4, padx=10, pady=10)

# Total Weight in tonnes
total_weight_label_tonnes = ctk.CTkLabel(frame, text="Total Weight in tonnes:", font=ctk.CTkFont(size=18))
total_weight_label_tonnes.grid(row=3, column=0, padx=10, pady=10, sticky="w")
entry_total_weight_tonnes = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18), state='disabled')
entry_total_weight_tonnes.grid(row=3, column=1, padx=10, pady=10)

# Total Weight in Brass
brass_label = ctk.CTkLabel(frame, text="Total Weight in Brass:", font=ctk.CTkFont(size=18))
brass_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
entry_brass = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18), state='disabled')
entry_brass.grid(row=4, column=1, padx=10, pady=10)

# Checkboxes for Sizes
size_label = ctk.CTkLabel(frame, text="Select Size:", font=ctk.CTkFont(size=18))
size_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
size_vars = []
sizes = [6, 12, 20, 40]
for idx, size in enumerate(sizes):
    size_var = tk.IntVar()
    size_vars.append(size_var)
    size_checkbox = ctk.CTkCheckBox(frame, text=f"{size} mm", variable=size_var, font=ctk.CTkFont(size=18))
    size_checkbox.grid(row=5+idx, column=1, padx=10, pady=5, sticky="w")

# Submit Button
submit_button = ctk.CTkButton(root, text="Submit", font=ctk.CTkFont(size=18), command=submit_form)
submit_button.pack(pady=20)

# Initialize date and time fields
refresh_date_time()

# Start the main loop
root.mainloop()
