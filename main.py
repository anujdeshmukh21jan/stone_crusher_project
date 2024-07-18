import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Function to initialize the database
def initialize_db():
    conn = sqlite3.connect('crusher.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY,
            bill_no TEXT,
            name TEXT,
            driver_name TEXT,
            time TEXT,
            date TEXT,
            vehicle_number TEXT,
            weight_before_load REAL,
            weight_after_load REAL,
            total_weight_tonnes REAL,
            brass REAL,
            sizes TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
def generate_unique_bill_no():
    conn = sqlite3.connect('crusher.db')
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(bill_no) FROM records')
    highest_bill_no = cursor.fetchone()[0]

    if highest_bill_no is None:
        new_bill_no = 1
    else:
        new_bill_no = int(highest_bill_no) + 1

    conn.close()
    return str(new_bill_no)
bill_no = generate_unique_bill_no()


# Function to calculate total weight and brass
def calculate_total_weight_and_brass():
    try:
        weight_before_load = 0.0
        if entry_weight_before_load.get():
            weight_before_load = float(entry_weight_before_load.get())
        
        weight_after_load = 0.0
        if entry_weight_after_load.get():
            weight_after_load = float(entry_weight_after_load.get())
        
        total_weight_tonnes = (weight_after_load - weight_before_load) / 1000
        brass = (weight_after_load - weight_before_load) / 4
        
        entry_total_weight_tonnes.configure(state='normal')
        entry_total_weight_tonnes.delete(0, tk.END)
        if total_weight_tonnes <= 0:
            entry_total_weight_tonnes.insert(0, f"0.0 tonnes")
        else:
            entry_total_weight_tonnes.insert(0, f"{total_weight_tonnes:.2f} tonnes")
        entry_total_weight_tonnes.configure(state='disabled')

        entry_brass.configure(state='normal')
        entry_brass.delete(0, tk.END)
        if brass <= 0:
            entry_brass.insert(0, f"0.0 kg")
        else:
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

def submit_form(event=None):
    # Get values from entries
    bill_no = entry_bill_no.get()
    name = entry_name.get()
    driver_name = entry_driver_name.get()
    time = entry_time.get()
    date = entry_date.get()
    vehicle_number = entry_vehicle_number.get()
    weight_before_load = entry_weight_before_load.get()
    weight_after_load = entry_weight_after_load.get()

    # Validate required fields
    required_fields = [
        (entry_name, "Name"),
        (entry_driver_name, "Driver Name"),
        (entry_vehicle_number, "Vehicle Number"),
        (entry_weight_before_load, "Weight Before Load"),
        (entry_weight_after_load, "Weight After Load")
    ]
    
    
    for entry, field_name in required_fields:
        if not entry.get():
            tk.messagebox.showerror("Error", f"{field_name} is required.")
            return

    # Convert weights to float
    try:
        weight_before_load = float(weight_before_load)
        weight_after_load = float(weight_after_load)
    except ValueError:
        tk.messagebox.showerror("Error", "Weight fields must be numeric.")
        return

    # Calculate total weight and brass
    total_weight_tonnes = (weight_after_load - weight_before_load) / 1000
    brass = (weight_after_load - weight_before_load) / 4

    # Get selected sizes
    sizes_selected = [str(size) for size, var in zip([6, 12, 20, 40], size_vars) if var.get()]

    # Insert data into the database
    conn = sqlite3.connect('crusher.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO records (bill_no, name, driver_name, time, date, vehicle_number, weight_before_load, weight_after_load, total_weight_tonnes, brass, sizes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (bill_no, name, driver_name, time, date, vehicle_number, weight_before_load, weight_after_load, total_weight_tonnes, brass, ', '.join(sizes_selected)))
    conn.commit()
    conn.close()

    # Print confirmation
    print("Form Submitted:")
    print(f"Bill No.: {bill_no}")
    print(f"Name: {name}")
    print(f"Driver Name: {driver_name}")
    print(f"Time: {time}")
    print(f"Date: {date}")
    print(f"Vehicle Number: {vehicle_number}")
    print(f"Weight Before Load: {weight_before_load}")
    print(f"Weight After Load: {weight_after_load}")
    print(f"Total Weight in tonnes: {total_weight_tonnes:.2f}")
    print(f"Total Weight in Brass: {brass:.2f}")
    print(f"Selected Sizes: {', '.join(sizes_selected)} mm")

    # Refresh the form fields
    refresh_form()
    refresh_date_time()

    # Generate PDF receipt
    generate_receipt(bill_no, name, driver_name, time, date, vehicle_number, weight_before_load, weight_after_load, total_weight_tonnes, brass, sizes_selected)

def generate_receipt(bill_no, name, driver_name, time, date, vehicle_number, weight_before_load, weight_after_load, total_weight_tonnes, brass, sizes_selected):
    file_name = f"receipt_{bill_no}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)

    # Set font and size
    c.setFont("Helvetica", 12)

    # Title
    c.drawString(50, 750, "Ashirwad Stone Crusher, Junner")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 730, "Receipt")
    c.line(50, 725, 200, 725)

    # Content
    c.setFont("Helvetica", 12)
    c.drawString(50, 710, f"Bill No.: {bill_no}")
    c.drawString(50, 690, f"Name: {name}")
    c.drawString(50, 670, f"Driver Name: {driver_name}")
    c.drawString(50, 650, f"Time: {time}")
    c.drawString(50, 630, f"Date: {date}")
    c.drawString(50, 610, f"Vehicle Number: {vehicle_number}")
    c.drawString(50, 590, f"Weight Before Load: {weight_before_load}")
    c.drawString(50, 570, f"Weight After Load: {weight_after_load}")
    c.drawString(50, 550, f"Total Weight in tonnes: {total_weight_tonnes:.2f}")
    c.drawString(50, 530, f"Total Weight in Brass: {brass:.2f}")
    
    # Selected Sizes
    sizes_str = ", ".join([f"{size} mm" for size in sizes_selected])
    c.drawString(50, 510, f"Selected Sizes: {sizes_str}")

    # Footer
    c.line(50, 500, 200, 500)
    c.drawString(50, 490, "Thank you for your business!")

    # Save the PDF
    c.save()

    print(f"Receipt generated: {file_name}")

# Function to print the receipt
def print_receipt():
    tk.messagebox.showinfo("Print Receipt", "Receipt Printed")

# Function to generate a report
def generate_report():
    tk.messagebox.showinfo("Generate Report", "Report Generated")


# Function to refresh the form
def refresh_form():
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
    entry_bill_no.configure(state='normal')
    entry_bill_no.delete(0, tk.END)
    entry_bill_no.insert(0, generate_unique_bill_no())
    entry_bill_no.configure(state='disabled')
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
root.attributes('-fullscreen', True)  # Open in full screen mode
root.geometry("1000x800")  
root.bind('<Return>', submit_form)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def toggle_dark_light_mode():
    current_mode = ctk.get_appearance_mode()
    print(current_mode)
    new_mode = "Dark" if current_mode == "Light" else "Light"
    ctk.set_appearance_mode(new_mode)

toggle_button = ctk.CTkButton(root, text="Toggle Dark/Light Mode", font=ctk.CTkFont(size=16), command=toggle_dark_light_mode)
toggle_button.pack(side='top', anchor='ne', padx=10, pady=10)  # Place at top right corner

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
entry_bill_no = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18), state='disabled')
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
name_label = ctk.CTkLabel(frame, text="Name: *", font=ctk.CTkFont(size=18))
name_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_name = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18))
entry_name.grid(row=1, column=1, padx=10, pady=10)

# Vehicle Number
vehicle_number_label = ctk.CTkLabel(frame, text="Vehicle Number: *", font=ctk.CTkFont(size=18))
vehicle_number_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")
entry_vehicle_number = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18))
entry_vehicle_number.grid(row=1, column=3, padx=10, pady=10)

# Driver Name
driver_name_label = ctk.CTkLabel(frame, text="Driver Name: *", font=ctk.CTkFont(size=18))
driver_name_label.grid(row=1, column=4, padx=10, pady=10, sticky="w")
entry_driver_name = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18))
entry_driver_name.grid(row=1, column=5, padx=10, pady=10)

# Weight Before Load
weight_before_load_label = ctk.CTkLabel(frame, text="Weight Before Load (kg): *", font=ctk.CTkFont(size=18))
weight_before_load_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_weight_before_load = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18))
entry_weight_before_load.grid(row=2, column=1, padx=10, pady=10)

# Weight After Load
weight_after_load_label = ctk.CTkLabel(frame, text="Weight After Load (kg): *", font=ctk.CTkFont(size=18))
weight_after_load_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")
entry_weight_after_load = ctk.CTkEntry(frame, width=200, font=ctk.CTkFont(size=18))
entry_weight_after_load.grid(row=2, column=3, padx=10, pady=10)

# Bind the KeyRelease event to the weight entry fields
entry_weight_before_load.bind("<KeyRelease>", lambda event: calculate_total_weight_and_brass())
entry_weight_after_load.bind("<KeyRelease>", lambda event: calculate_total_weight_and_brass())

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
initialize_db()
refresh_date_time()

# Start the main loop
root.mainloop()
