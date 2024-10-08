import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from datetime import datetime
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from tkinter import messagebox
from tkinter.ttk import Combobox
from constant import DB_PATH, BASE_DIR, RECIEPT_PATH
import platform
import sys


if platform.system() == "Windows":
    import win32print
    import win32api
else:
    import cups
    
from jinja2 import Environment, FileSystemLoader
import pdfkit

import pdfkit


# Set the path to wkhtmltopdf executable file
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" 
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


def convert_html_to_pdf(html_template):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_name = os.path.join(RECIEPT_PATH, f"receipt{timestamp}.pdf")
    try:
        # Convert HTML string to PDF
        pdfkit.from_string(str(html_template), file_name, configuration=config)
        print(f"PDF file generated: {file_name}")
    except Exception as e:
        print(f"Error generating PDF: {e}")

    return file_name

def render_template(filepath, data):
    # Setup Jinja2 environment
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)

    # Load the template
    try:
        template = env.get_template('reciept.html')
    except Exception as e:
        print(f"Error loading template: {e}")
        exit()

    # Render the template with data
    try:
        html_output = template.render(data=data)
        if not html_output.strip():
            print("Rendered HTML is empty.")
        else:
            # Save the rendered HTML to a file
            with open(BASE_DIR+'receipt_output.html', 'w') as file:
                file.write(html_output)
            with open(BASE_DIR+"receipt_output.html", 'r') as f:
                html_content = f.read()
            # print("HTML file generated: receipt_output.html")
            return html_content
    except Exception as e:
        print(f"Error rendering template: {e}")
        
def print_receipt(file_path):
    if platform.system() == "Windows":
        win32api.ShellExecute(
            0,
            "print",
            file_path,
            win32print.GetDefaultPrinter(),
            ".",
            0
        ) 
    else:
        # print("Platform is not Windows")
        conn = cups.Connection()
        # print("CUPS connection established")
        printers = conn.getPrinters()
        # print("Printers retrieved")
        printer_name = list(printers.keys())[0]  # Use the first available printer
        print(f"Printer name: {printer_name}")
        conn.printFile(printer_name, file_path, "Receipt", {})
        # print("File printed")

# Function to initialize the database
def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY,
            bill_no TEXT,
            name TEXT,
            driver_name TEXT,
            time TEXT,
            date DATE,
            vehicle_number TEXT,
            weight_before_load REAL,
            weight_after_load REAL,
            total_weight_tonnes REAL,
            brass REAL,
            sizes TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY,
            manufacuturer TEXT,
            model TEXT,
            registration_number TEXT,
            weight REAL,
            date_of_purchase TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    
def generate_unique_bill_no():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT MAX(id) FROM records')
        highest_bill_no = cursor.fetchone()[0]
    except:
        return "1"
    
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
        brass = total_weight_tonnes / 4
        
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
            messagebox.showerror("Error", f"{field_name} is required.")
            return

    # Convert weights to float
    try:
        weight_before_load = float(weight_before_load)
        weight_after_load = float(weight_after_load)
    except ValueError:
        messagebox.showerror("Error", "Weight fields must be numeric.")
        return

    # Calculate total weight and brass
    total_weight_tonnes = (weight_after_load - weight_before_load) / 1000
    brass = total_weight_tonnes / 4

    # Get selected sizes
    sizes_selected = [str(size) for size, var in zip([6, 12, 20, 40, "GSM"], size_vars) if var.get()]

    # Insert data into the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO records (bill_no, name, driver_name, time, date, vehicle_number, weight_before_load, weight_after_load, total_weight_tonnes, brass, sizes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (bill_no, name, driver_name, time, date, vehicle_number, weight_before_load, weight_after_load, total_weight_tonnes, brass, (', '.join(sizes_selected))))
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
    print(f"Selected Sizes: {', '.join(sizes_selected)}")

    # Refresh the form fields
    refresh_form()
    refresh_date_time()
    messagebox.showinfo("Success", "report added successfully")
    data = {
        "bill_no": bill_no,
        "name": name,
        "driver_name": driver_name,
        "date": date,
        "vehicle_number": vehicle_number,
        "weight_before_load": weight_before_load,
        "weight_after_load": weight_after_load,
        "net_weight": weight_after_load - weight_before_load,
        "total_weight_tonnes": total_weight_tonnes,
        "brass": brass,
        "sizes_selected": ", ".join([i + (" mm" if i != "GSM" else "") for i in sizes_selected])
    }
    html_template = render_template(os.path.join(BASE_DIR, "reciept.html"), data=data)
    # Generate PDF receipt
    file = convert_html_to_pdf(html_template)
    print_receipt(file)
    
def add_vehicle(event=None):
    manufacturer = entry_manufacturer.get()
    model = entry_model.get()
    registration_number = entry_registration_number.get()
    date_of_purchase = entry_date_of_purchase.get()
    weight = entry_weight.get()
    required_fields = [
        (entry_manufacturer, "manufacturer"),
        (entry_model, "Model Name"),
        (entry_registration_number, "Registration Number"),
        (entry_date_of_purchase, "date_of_purchase")
    ]
    
    
    for entry, field_name in required_fields:
        if not entry.get():
            messagebox.showerror("Error", f"{field_name} is required.")
            return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vehicles (manufacturer, model, registration_number, date_of_purchase, weight)
        VALUES (?, ?, ?, ?, ?)
    ''', (manufacturer, model, registration_number, date_of_purchase, weight))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Vehicle added successfully")
    refresh_vehicle_form()
    refresh_vehicle_dropdown()
    
def refresh_vehicle_dropdown():
    updated_vehicle_numbers = get_vehicle_numbers()
    entry_vehicle_number['values'] = updated_vehicle_numbers

def refresh_vehicle_form():
    entry_manufacturer.delete(0, tk.END)
    entry_model.delete(0, tk.END)
    entry_registration_number.delete(0, tk.END)
    entry_date_of_purchase.delete(0, tk.END)
    entry_weight.delete(0, tk.END)
    
    
def generate_receipt(bill_no, name, driver_name, time, date, vehicle_number, weight_before_load, weight_after_load, total_weight_tonnes, brass, sizes_selected):
    file_name = f"receipt_{bill_no}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)

    # Set font and size
    c.setFont("Helvetica", 12)

    # Title
    c.drawString(50, 750, "Stone Crusher")
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
    print("Receipt generated")
    return file_name


def get_vehicle_numbers():
    # This function should return a list of vehicle numbers from the vehicle table
    # Implement this function based on your database setup

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT registration_number FROM vehicles')
        data = cursor.fetchall()
        vehicle_no = []
        for i in data:
            vehicle_no.append(i[0])
        entry_vehicle_number.configure(values=vehicle_no)
        return vehicle_no

    except Exception as e:
        print(f"Error getting vehicle numbers: {e}")
        return []
    
# Function to generate a report
def generate_report():
    import subprocess
    subprocess.run(["python", BASE_DIR+"/demo3.py"])

vehicle_weight_cache = {}

def fill_weight_from_cache(vehicle_number):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # If not in cache, fetch from the database and store in cache
    cursor.execute("SELECT registration_number, weight FROM vehicles")

    # Fetch all the results
    vehicle_data = cursor.fetchall()

    # Iterate over the data and populate the dictionary
    for vehicle_no, weight in vehicle_data:
        vehicle_weight_cache[vehicle_no] = weight
    weight = vehicle_weight_cache[vehicle_number]
    
    entry_weight_before_load.delete(0, tk.END)
    entry_weight_before_load.insert(0, weight)
    # Set the weight in your Tkinter entry or label
    # weight_entry.insert(0, weight)

def autocomplete(event):
    search_term = entry_name.get()
    suggestions = [name for name in dynamic_names if search_term.lower() in name.lower()]
    entry_name.configure(values=suggestions)
    entry_name.event_generate("<<ComboboxEdited>>")

def fetch_dynamic_names():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM records")
        names = cursor.fetchall()
        conn.close()
        names_list = [i[0] for i in names]
        return names_list
    except:
        return []

def fill_weight(event):
    search_term = entry_vehicle_number.get()
    suggestions = [name for name in vehicle_numbers if search_term.lower() in name.lower()]
    entry_vehicle_number.configure(values=suggestions)
    entry_vehicle_number.event_generate("<<ComboboxEdited>>")
    fill_weight_from_cache(entry_vehicle_number.get())
    

# Function to refresh the form
def refresh_form():
    entry_name.set("")
    entry_vehicle_number.set("")
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
    get_vehicle_numbers()

# Function to refresh the date and time
def refresh_date_time():
    entry_bill_no.configure(state='normal')
    entry_bill_no.delete(0, tk.END)
    entry_bill_no.insert(0, generate_unique_bill_no())
    entry_bill_no.configure(state='disabled')
    current_time = datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.now().strftime("%Y-%m-%d")
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
# root.attributes('-fullscreen', True)  # Open in full screen mode
root.geometry("1500x1000")  
root.bind('<Return>', submit_form)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def go_home_and_refresh():
    notebook.select(main_tab)
    refresh_form()



def toggle_dark_light_mode():
    current_mode = ctk.get_appearance_mode()

    new_mode = "Dark" if current_mode == "Light" else "Light"
    ctk.set_appearance_mode(new_mode)

toggle_button = ctk.CTkButton(root, text="Toggle Dark/Light Mode", font=ctk.CTkFont(size=16), command=toggle_dark_light_mode)
toggle_button.pack(side='top', anchor='ne', padx=10, pady=10)  # Place at top right corner

# Title Label
title_label = ctk.CTkLabel(root, text="Stone Crusher", font=ctk.CTkFont(size=30, weight="bold"))
title_label.pack(pady=10)
quotation_label = ctk.CTkLabel(root, text="Cotation", font=ctk.CTkFont(size=24))
quotation_label.pack(pady=7)

# Navigation Bar
nav_frame = ctk.CTkFrame(root, height=40, bg_color="transparent")
nav_frame.pack(fill='x')


def restart_app():
    # This will terminate the current process and relaunch it
    python = sys.executable
    os.execl(python, python, *sys.argv)

refresh_button = ctk.CTkButton(nav_frame, text="Refresh", font=ctk.CTkFont(size=16), command=restart_app)
refresh_button.pack(side='right', padx=10,pady=5)

report_button = ctk.CTkButton(nav_frame, text="Report", font=ctk.CTkFont(size=16), command=generate_report)
report_button.pack(side='right', padx=10, pady=5)

# print_button = ctk.CTkButton(nav_frame, text="Print Receipt", font=ctk.CTkFont(size=16), command=print_receipt)
# print_button.pack(side='right', padx=10, pady=5)

add_vehicle_button = ctk.CTkButton(nav_frame, text="Add Vehicle", font=ctk.CTkFont(size=16), command=lambda: notebook.select(add_vehicle_tab))
add_vehicle_button.pack(side='right', padx=10, pady=5)

home_button = ctk.CTkButton(nav_frame, text="Home", font=ctk.CTkFont(size=16), command=go_home_and_refresh)
home_button.pack(side='right', padx=10, pady=5)
                 
# Notebook for tab management
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Main Tab
main_tab = ctk.CTkFrame(notebook)
notebook.add(main_tab, state='hidden')

# Add Vehicle Tab
add_vehicle_tab = ctk.CTkFrame(notebook)
notebook.add(add_vehicle_tab, state='hidden')

# Frame for the input fields
frame = ctk.CTkFrame(main_tab)
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



# entry_name = AutocompleteEntry(frame, width=200, font=ctk.CTkFont(size=18), field='name')
# entry_name.grid(row=1, column=1, padx=10, pady=10)

# entry_driver_name = AutocompleteEntry(frame, width=200, font=ctk.CTkFont(size=18), field='driver_name')
# entry_driver_name.grid(row=1, column=5, padx=10, pady=10)

# entry_vehicle_number = AutocompleteEntry(frame, width=200, font=ctk.CTkFont(size=18), field='vehicle_number')
# entry_vehicle_number.grid(row=1, column=3, padx=10, pady=10)

# Name
name_label = ctk.CTkLabel(frame, text="Name: *", font=ctk.CTkFont(size=18))
name_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_name = ctk.CTkComboBox(frame, width=200, font=ctk.CTkFont(size=18), hover=True)
entry_name.set("")
entry_name.grid(row=1, column=1, padx=10, pady=10)
entry_name.bind("<KeyRelease>", autocomplete)

# Fetch dynamic names and update the combobox
dynamic_names = fetch_dynamic_names()
entry_name.configure(values=dynamic_names)

# Hide the listbox initially
# listbox_names.grid_forget()
# listbox_names.bind("<ButtonRelease-1>", on_select_name)

# Vehicle Number
vehicle_number_label = ctk.CTkLabel(frame, text="Vehicle Number: *", font=ctk.CTkFont(size=18))
vehicle_number_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")
# Create the combobox for vehicle number
entry_vehicle_number = ctk.CTkComboBox(frame, width=200, font=ctk.CTkFont(size=18), hover=True)
entry_vehicle_number.set("")
entry_vehicle_number.grid(row=1, column=3, padx=10, pady=10)

vehicle_numbers = get_vehicle_numbers()


entry_vehicle_number.bind("<KeyRelease>",fill_weight)


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

# Checkboxes for Sizes
size_label = ctk.CTkLabel(frame, text="Select Size:", font=ctk.CTkFont(size=18))
size_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

size_vars = []
sizes = [6, 12, 20, 40, "GSM"]  # Add GSM to the list of sizes
for idx, size in enumerate(sizes):
    size_var = tk.IntVar()
    size_vars.append(size_var)
    if size == "GSM":
        size_checkbox = ctk.CTkCheckBox(frame, text="GSM", variable=size_var, font=ctk.CTkFont(size=18))
    else:
        size_checkbox = ctk.CTkCheckBox(frame, text=f"{size} mm", variable=size_var, font=ctk.CTkFont(size=18))
    size_checkbox.grid(row=5+idx, column=1, padx=10, pady=5, sticky="w")



# Submit Button (inside the inner frame)
submit_button = ctk.CTkButton(frame, text="Submit", font=ctk.CTkFont(size=18), command=submit_form)
submit_button.grid(row=10, column=3, pady=20)







# Frame for the add vehicle form in the add vehicle tab
add_vehicle_frame = ctk.CTkFrame(add_vehicle_tab)
add_vehicle_frame.pack(pady=40, padx=40, fill="both", expand=True)

# Inner frame to center the fields
inner_frame = ctk.CTkFrame(add_vehicle_frame)
inner_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)  # Adjusted relx and rely for proper centering

# Add Vehicle form fields
# Manufacturer
manufacturer_label = ctk.CTkLabel(inner_frame, text="Manufacturer:", font=ctk.CTkFont(size=18))
manufacturer_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_manufacturer = ctk.CTkEntry(inner_frame, width=200, font=ctk.CTkFont(size=18))
entry_manufacturer.grid(row=0, column=1, padx=10, pady=10)

# Model
model_label = ctk.CTkLabel(inner_frame, text="Model:", font=ctk.CTkFont(size=18))
model_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_model = ctk.CTkEntry(inner_frame, width=200, font=ctk.CTkFont(size=18))
entry_model.grid(row=1, column=1, padx=10, pady=10)

# Registration Number
registration_number_label = ctk.CTkLabel(inner_frame, text="Registration Number:", font=ctk.CTkFont(size=18))
registration_number_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_registration_number = ctk.CTkEntry(inner_frame, width=200, font=ctk.CTkFont(size=18))
entry_registration_number.grid(row=2, column=1, padx=10, pady=10)

# Weight of the vehicle
weight_label = ctk.CTkLabel(inner_frame, text="Weight:", font=ctk.CTkFont(size=18))
weight_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
entry_weight = ctk.CTkEntry(inner_frame, width=200, font=ctk.CTkFont(size=18))
entry_weight.grid(row=3, column=1, padx=10, pady=10)

# Date of Purchase
date_of_purchase_label = ctk.CTkLabel(inner_frame, text="Date of Purchase:", font=ctk.CTkFont(size=18))
date_of_purchase_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
entry_date_of_purchase = ctk.CTkEntry(inner_frame, width=200, font=ctk.CTkFont(size=18))
entry_date_of_purchase.grid(row=4, column=1, padx=10, pady=10)

# Add Button (outside the inner frame)
add_vehicle_button = ctk.CTkButton(add_vehicle_frame, text="Add", font=ctk.CTkFont(size=18), command=add_vehicle)
add_vehicle_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)  # Centered in the outer frame



# Initialize date and time fields
initialize_db()
refresh_date_time()

# Start the main loop
root.mainloop()




