import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os

DATA_FILE = "student_submissions.json"

# ---------------------------------------------------
# Data Storage
# ---------------------------------------------------

records = []


def load_data():
    global records

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                records = json.load(file)
        except:
            records = []
    else:
        records = []


def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(records, file, indent=4)


# ---------------------------------------------------
# Validation
# ---------------------------------------------------

def validate_input():
    enrollment = entry_enrollment.get().strip()
    name = entry_name.get().strip()
    assignment = entry_assignment.get().strip()
    marks = entry_marks.get().strip()

    if not enrollment or not name or not assignment:
        messagebox.showerror(
            "Validation Error",
            "Enrollment, Name and Assignment are required."
        )
        return False

    if marks:
        try:
            marks_value = float(marks)

            if marks_value < 0 or marks_value > 100:
                messagebox.showerror(
                    "Validation Error",
                    "Marks must be between 0 and 100."
                )
                return False

        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Marks must be a number."
            )
            return False

    return True


# ---------------------------------------------------
# Add Submission
# ---------------------------------------------------

def add_submission():

    if not validate_input():
        return

    enrollment = entry_enrollment.get().strip()
    name = entry_name.get().strip()
    assignment = entry_assignment.get().strip()
    marks = entry_marks.get().strip()
    remarks = entry_remarks.get("1.0", tk.END).strip()

    status = status_var.get()

    # Check duplicate submission
    for record in records:
        if (record["enrollment"] == enrollment and
                record["assignment"].lower() == assignment.lower()):

            messagebox.showwarning(
                "Duplicate",
                "This student already has this assignment."
            )
            return

    record = {
        "enrollment": enrollment,
        "name": name,
        "assignment": assignment,
        "status": status,
        "marks": marks,
        "remarks": remarks
    }

    records.append(record)

    save_data()
    refresh_table()

    messagebox.showinfo(
        "Success",
        "Submission added successfully."
    )

    clear_fields()


# ---------------------------------------------------
# Update Marks
# ---------------------------------------------------

def update_marks():

    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Selection Required",
            "Please select a record."
        )
        return

    marks = entry_marks.get().strip()

    try:
        marks_value = float(marks)

        if marks_value < 0 or marks_value > 100:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid Marks",
            "Enter marks between 0 and 100."
        )
        return

    index = int(table.item(selected[0], "values")[6])

    records[index]["marks"] = marks
    records[index]["status"] = "Completed"

    save_data()
    refresh_table()

    messagebox.showinfo(
        "Updated",
        "Marks updated successfully."
    )


# ---------------------------------------------------
# Filtering
# ---------------------------------------------------

def filter_records(event=None):

    selected_filter = filter_var.get()

    for item in table.get_children():
        table.delete(item)

    for index, record in enumerate(records):

        if selected_filter == "All":
            show = True

        elif selected_filter == record["status"]:
            show = True

        else:
            show = False

        if show:
            table.insert(
                "",
                tk.END,
                values=(
                    record["enrollment"],
                    record["name"],
                    record["assignment"],
                    record["status"],
                    record["marks"],
                    record["remarks"],
                    index
                )
            )


def refresh_table():
    filter_records()


# ---------------------------------------------------
# Export CSV
# ---------------------------------------------------

def export_csv():

    if not records:
        messagebox.showwarning(
            "No Data",
            "There are no records to export."
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        return

    with open(file_path, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Enrollment",
            "Name",
            "Assignment",
            "Status",
            "Marks",
            "Remarks"
        ])

        for record in records:
            writer.writerow([
                record["enrollment"],
                record["name"],
                record["assignment"],
                record["status"],
                record["marks"],
                record["remarks"]
            ])

    messagebox.showinfo(
        "Export Successful",
        "CSV report exported successfully."
    )


# ---------------------------------------------------
# Clear Fields
# ---------------------------------------------------

def clear_fields():

    entry_enrollment.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_assignment.delete(0, tk.END)
    entry_marks.delete(0, tk.END)
    entry_remarks.delete("1.0", tk.END)

    status_var.set("Pending")


# ---------------------------------------------------
# Select Record
# ---------------------------------------------------

def select_record(event):

    selected = table.selection()

    if not selected:
        return

    values = table.item(selected[0], "values")

    clear_fields()

    entry_enrollment.insert(0, values[0])
    entry_name.insert(0, values[1])
    entry_assignment.insert(0, values[2])
    entry_marks.insert(0, values[4])
    entry_remarks.insert("1.0", values[5])

    status_var.set(values[3])


# ===================================================
# GUI
# ===================================================

root = tk.Tk()
root.title("Student Assignment Submission Manager")
root.geometry("1100x650")

# ---------------- Title ----------------

title = tk.Label(
    root,
    text="Student Assignment Submission Manager",
    font=("Arial", 20, "bold")
)

title.pack(pady=10)


# ---------------- Input Frame ----------------

input_frame = tk.Frame(root)
input_frame.pack(pady=5)


# Enrollment
tk.Label(input_frame, text="Enrollment:").grid(
    row=0, column=0, padx=5, pady=5
)

entry_enrollment = tk.Entry(input_frame, width=20)
entry_enrollment.grid(row=0, column=1)


# Name
tk.Label(input_frame, text="Name:").grid(
    row=0, column=2, padx=5
)

entry_name = tk.Entry(input_frame, width=20)
entry_name.grid(row=0, column=3)


# Assignment
tk.Label(input_frame, text="Assignment:").grid(
    row=1, column=0, padx=5, pady=5
)

entry_assignment = tk.Entry(input_frame, width=20)
entry_assignment.grid(row=1, column=1)


# Marks
tk.Label(input_frame, text="Marks:").grid(
    row=1, column=2, padx=5
)

entry_marks = tk.Entry(input_frame, width=20)
entry_marks.grid(row=1, column=3)


# Status
tk.Label(input_frame, text="Status:").grid(
    row=2, column=0, padx=5, pady=5
)

status_var = tk.StringVar(value="Pending")

tk.Radiobutton(
    input_frame,
    text="Pending",
    variable=status_var,
    value="Pending"
).grid(row=2, column=1, sticky="w")

tk.Radiobutton(
    input_frame,
    text="Completed",
    variable=status_var,
    value="Completed"
).grid(row=2, column=2, sticky="w")


# Remarks
tk.Label(input_frame, text="Remarks:").grid(
    row=3, column=0, padx=5, pady=5
)

entry_remarks = tk.Text(
    input_frame,
    width=50,
    height=3
)

entry_remarks.grid(
    row=3,
    column=1,
    columnspan=3
)


# ---------------- Buttons ----------------

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Add Submission",
    command=add_submission
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Update Marks",
    command=update_marks
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="Export CSV",
    command=export_csv
).grid(row=0, column=3, padx=5)


# ---------------- Filter ----------------

filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

tk.Label(
    filter_frame,
    text="Filter:"
).pack(side=tk.LEFT, padx=5)

filter_var = tk.StringVar(value="All")

filter_menu = ttk.Combobox(
    filter_frame,
    textvariable=filter_var,
    values=["All", "Pending", "Completed"],
    state="readonly",
    width=15
)

filter_menu.pack(side=tk.LEFT)
filter_menu.bind("<<ComboboxSelected>>", filter_records)


# ---------------- Table ----------------

table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

columns = (
    "Enrollment",
    "Name",
    "Assignment",
    "Status",
    "Marks",
    "Remarks",
    "Index"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for column in columns:

    table.heading(
        column,
        text=column
    )

    table.column(
        column,
        width=120
    )

# Hide internal index column
table.column("Index", width=0, stretch=False)
table.heading("Index", text="")

table.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True
)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient=tk.VERTICAL,
    command=table.yview
)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

table.configure(
    yscrollcommand=scrollbar.set
)

table.bind(
    "<<TreeviewSelect>>",
    select_record
)


# ---------------------------------------------------
# Start Application
# ---------------------------------------------------

load_data()
refresh_table()

root.mainloop()