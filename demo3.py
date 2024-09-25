import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import sqlite3
import pandas as pd
import os
from constant import DB_PATH, BASE_DIR, EXCEL_PATH
from tkinter import messagebox
# Fetch data from the database
def fetch_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT bill_no, name, driver_name, date, vehicle_number, total_weight_tonnes, brass, sizes FROM records")
    data = cursor.fetchall()
    conn.close()
    return data

class VehicleDataApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Stone Crusher")
        ctk.set_appearance_mode("light")
        self.geometry("800x500")

        self.sort_column = None
        self.sort_reverse = False

        self.create_widgets()
        self.populate_table(fetch_data())

    def create_widgets(self):
        # Central container frame
        central_frame = ctk.CTkFrame(self, width=2000, height=1000)
        central_frame.pack(pady=5, fill=tk.NONE, expand=False)


        # Horizontal frame for search and filter fields
        top_frame = ctk.CTkFrame(central_frame)
        top_frame.pack(pady=5, fill=tk.X)

        # Search bar
        search_label = ctk.CTkLabel(top_frame, text="Search:", font=("Arial", 14))
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.search_entry = ctk.CTkEntry(top_frame, font=("Arial", 14), width=170)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.search_entry.bind("<KeyRelease>", self.update_table)

        # Filter by Bill No
        filter_bill_no_label = ctk.CTkLabel(top_frame, text="Bill No:", font=("Arial", 14))
        filter_bill_no_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.bill_no_entry = ctk.CTkEntry(top_frame, font=("Arial", 14))
        self.bill_no_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Filter by Name
        filter_name_label = ctk.CTkLabel(top_frame, text="Name:", font=("Arial", 14))
        filter_name_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.name_entry = ctk.CTkEntry(top_frame, font=("Arial", 14))
        self.name_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

        # Filter by Driver Name
        filter_driver_name_label = ctk.CTkLabel(top_frame, text="Driver Name:", font=("Arial", 14))
        filter_driver_name_label.grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
        self.driver_name_entry = ctk.CTkEntry(top_frame, font=("Arial", 14))
        self.driver_name_entry.grid(row=1, column=5, padx=5, pady=5, sticky=tk.W)

        # Filter by Vehicle Number
        filter_vehicle_number_label = ctk.CTkLabel(top_frame, text="Vehicle Number:", font=("Arial", 14))
        filter_vehicle_number_label.grid(row=1, column=6, padx=5, pady=5, sticky=tk.W)
        self.vehicle_number_entry = ctk.CTkEntry(top_frame, font=("Arial", 14))
        self.vehicle_number_entry.grid(row=1, column=7, padx=5, pady=5, sticky=tk.W)

        # Filter by Start Date
        filter_start_date_label = ctk.CTkLabel(top_frame, text="Start Date:", font=("Arial", 14))
        filter_start_date_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_date_entry = DateEntry(top_frame, selectmode='day', date_pattern='yyyy-mm-dd', font=("Arial", 14))
        self.start_date_entry.set_date(datetime.now()-timedelta(days=365)) 
        self.start_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # Filter by End Date
        filter_end_date_label = ctk.CTkLabel(top_frame, text="End Date:", font=("Arial", 14))
        filter_end_date_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.end_date_entry = DateEntry(top_frame, selectmode='day', date_pattern='yyyy-mm-dd', font=("Arial", 14))
        self.end_date_entry.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
        
        # Apply Filter Button
        filter_button = ctk.CTkButton(top_frame, text="Apply Filter", command=self.update_table, font=("Arial", 14))
        filter_button.grid(row=2, column=4, padx=5, pady=10, sticky=tk.W)

        # Clear Filter Button
        clear_filter_button = ctk.CTkButton(top_frame, text="Clear Filter", command=self.clear_filters, font=("Arial", 14))
        clear_filter_button.grid(row=2, column=5, padx=5, pady=10, sticky=tk.W)

        download_excel_button = ctk.CTkButton(top_frame, text="Download as Excel", command=self.download_as_excel, font=("Arial", 14))
        download_excel_button.grid(row=2, column=6, padx=5, pady=10, sticky=tk.W)

        # Table
        fields = ['Bill No', 'Name', 'Driver Name', 'Date', 'Vehicle Number', 'Total Weight Tonnes', 'Brass', 'Sizes']
        self.tree = ttk.Treeview(self, columns=fields, show='headings')
        for field in fields:
            self.tree.heading(field, text=field, command=lambda c=field: self.sort_table(c))
            self.tree.column(field, anchor=tk.CENTER, width=150)

        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def populate_table(self, data):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert data into table
        for row in data:
            self.tree.insert("", tk.END, values=row)

    def update_table(self, event=None):
        print("Updating table with filters:")
        search_term = self.search_entry.get().lower()
        bill_no = self.bill_no_entry.get()
        name = self.name_entry.get().lower()
        driver_name = self.driver_name_entry.get().lower()
        vehicle_number = self.vehicle_number_entry.get().lower()
        start_date = self.start_date_entry.get_date().strftime('%Y-%m-%d')
        end_date = self.end_date_entry.get_date().strftime('%Y-%m-%d')

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = '''
            SELECT bill_no, name, driver_name, date, vehicle_number, total_weight_tonnes, brass, sizes
            FROM records 
            WHERE 1=1
        '''
        params = []

        if search_term:
            query += " AND (name LIKE ? OR driver_name LIKE ? OR vehicle_number LIKE ?)"
            params.extend([f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"])
            print("Adding search term filter:", f"%{search_term}%")
        if bill_no:
            query += " AND bill_no LIKE ?"
            params.append(f"%{bill_no}%")
            print("Adding bill no. filter:", f"%{bill_no}%")
        if name:
            query += " AND name LIKE ?"
            params.append(f"%{name}%")
            print("Adding name filter:", f"%{name}%")
        if driver_name:
            query += " AND driver_name LIKE ?"
            params.append(f"%{driver_name}%")
            print("Adding driver name filter:", f"%{driver_name}%")
        if vehicle_number:
            query += " AND vehicle_number LIKE ?"
            params.append(f"%{vehicle_number}%")
            print("Adding vehicle number filter:", f"%{vehicle_number}%")
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
            print("Adding start date filter:", start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
            print("Adding end date filter:", end_date)

        print("Executing query:", query)
        print("With parameters:", params)

        cursor.execute(query, params)
        filtered_data = cursor.fetchall()
        conn.close()

        print("Filtered data:", filtered_data)
        self.populate_table(filtered_data)




    def clear_filters(self):
        self.bill_no_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.driver_name_entry.delete(0, tk.END)
        self.vehicle_number_entry.delete(0, tk.END)
        self.start_date_entry.set_date(datetime.now().date())
        self.end_date_entry.set_date(datetime.now().date())
        self.search_entry.delete(0, tk.END)
        self.populate_table(fetch_data())

    def sort_table(self, column):
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        self.sort_column = column

        data = [(self.tree.set(child, column), child) for child in self.tree.get_children('')]
        data.sort(reverse=self.sort_reverse)

        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)

        self.tree.heading(column, text=column + (' ▲' if self.sort_reverse else ' ▼'))

    def download_as_excel(self):
        search_term = self.search_entry.get().lower()
        bill_no = self.bill_no_entry.get()
        name = self.name_entry.get().lower()
        driver_name = self.driver_name_entry.get().lower()
        vehicle_number = self.vehicle_number_entry.get().lower()
        start_date = self.start_date_entry.get_date().strftime('%Y-%m-%d')
        end_date = self.end_date_entry.get_date().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = '''
            SELECT bill_no, name, driver_name, time, date, vehicle_number, weight_before_load, weight_after_load, total_weight_tonnes, brass, sizes
            FROM records 
            WHERE 1=1
        '''
        params = []

        if search_term:
            query += " AND (name LIKE ? OR driver_name LIKE ? OR vehicle_number LIKE ?)"
            params.extend([f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"])
        if bill_no:
            query += " AND bill_no LIKE ?"
            params.append(f"%{bill_no}%")
        if name:
            query += " AND name LIKE ?"
            params.append(f"%{name}%")
        if driver_name:
            query += " AND driver_name LIKE ?"
            params.append(f"%{driver_name}%")
        if vehicle_number:
            query += " AND vehicle_number LIKE ?"
            params.append(f"%{vehicle_number}%")
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
            print("Adding start date filter:", start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
            print("Adding end date filter:", end_date)

        cursor.execute(query, params)
        filtered_data = cursor.fetchall()
        conn.close()

        # Debug print statements
        print("Filtered data to be exported:", filtered_data)

        if not filtered_data:
            print("No data to export.")
            return

        df = pd.DataFrame(filtered_data, columns=["bill_no", "name", "driver_name", "time", "date", "vehicle_number", "weight_before_load", "weight_after_load", "total_weight_tonnes", "brass", "sizes"])
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_path = os.path.join(EXCEL_PATH, f"report-{timestamp}.xlsx")
        df.to_excel(file_path, index=False)

        # Confirm file saved
        if df.empty:
            print("DataFrame is empty. No data to save.")
        else:
            print(f"Data successfully exported to {file_path}")

        messagebox.showinfo("Success", f"Excel generate successfully at {file_path}")

if __name__ == "__main__":
    app = VehicleDataApp()
    app.mainloop()