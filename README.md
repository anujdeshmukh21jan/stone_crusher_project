# Stone Crusher Project

## Overview

The **Stone Crusher Management System** is designed to streamline the operations and management of stone crusher businesses. It tracks vehicle details, weight before and after load, calculates the total weight, and generates receipts for each transaction.

### Features:
- **Vehicle Management**: Add, update, and manage vehicles used in transportation.
- **Weight Tracking**: Track the weight of vehicles before and after loading.
- **Receipt Generation**: Automatically generate PDF receipts for each transaction, including multiple size options for printing.
- **Filters & Reports**: Search and filter transaction records based on bill numbers, date, name, and other fields.
- **SQLite Integration**: Store and retrieve transaction data in an SQLite database.
- **User-friendly Interface**: A clean and efficient Tkinter-based GUI for ease of use.

---

## Technologies Used

- **Python**: Main programming language used.
- **Tkinter**: For creating a desktop GUI application.
- **SQLite**: For database management.
- **CustomTkinter**: For enhanced UI elements in the Tkinter application.
- **HTML/CSS**: Used in the receipt generation for displaying and printing PDF reports.
- **WeasyPrint**: To convert HTML to PDF for receipt generation.
- **Jinja2**: For rendering dynamic HTML templates for receipts.

---

## Installation

### Prerequisites

- Python 3.x
- Required Python libraries: Install via pip
    ```bash
    pip install requirements.txt
    ```

### Steps to Setup

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/anujdeshmukh21jan/stone_crusher_project.git
    ```

2. Navigate to the project directory:
    ```bash
    cd stone_crusher_project
    ```

3. Initialize the SQLite database (ensure that the database path is correctly set in the `DB_PATH` variable in the code).

4. Run the application:
    ```bash
    python main.py
    ```

---

## Database Structure

- **vehicles table**: Stores information about the vehicles.
  - `id`: Primary key
  - `manufacturer`: Name of the vehicle manufacturer
  - `model`: Model name of the vehicle
  - `registration_number`: Unique vehicle number
  - `date_of_purchase`: Date when the vehicle was purchased
  - `weight`: The weight of the vehicle

- **records table**: Stores transaction data for each load.
  - `id`: Primary key
  - `bill_no`: Unique bill number
  - `name`: Customer name
  - `vehicle_number`: Associated vehicle
  - `date`: Transaction date
  - `weight_before_load`: Weight before loading
  - `weight_after_load`: Weight after loading
  - `net_weight`: Net weight of the load
  - `total_weight_tonnes`: Weight in tonnes
  - `brass`: Measurement in brass
  - `sizes_selected`: List of sizes selected for the load

---

## Contact

For any questions, reach out to:
- **Name**: Anuj Deshmukh
- **Email**: anujdeshmukh21jan@gmail.com
- **GitHub**: [Anuj Deshmukh](https://github.com/anujdeshmukh21jan)

---

