import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re


# ---------------- DATABASE ----------------

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysqlmansib@14",
        database="college"
    )

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Contact (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            phone VARCHAR(20),
            category VARCHAR(50),
            notes TEXT,
            INDEX idx_name (name),
            INDEX idx_email (email),
            INDEX idx_phone (phone)
        )
    """)

    conn.commit()

except mysql.connector.Error as e:
    print("Database Error:", e)
    exit()


# ---------------- FUNCTIONS ----------------

def valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email) is not None


def clear_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    category_combo.set("Friend")
    notes_text.delete("1.0", tk.END)


def add_contact():

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    category = category_combo.get()
    notes = notes_text.get("1.0", tk.END).strip()

    if not name or not email:
        messagebox.showwarning(
            "Validation Error",
            "Name and email are required."
        )
        return

    if not valid_email(email):
        messagebox.showerror(
            "Invalid Email",
            "Enter a valid email address."
        )
        return

    try:
        cursor.execute("""
            INSERT INTO Contact
            (name, email, phone, category, notes)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, phone, category, notes))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Record inserted successfully."
        )

        clear_fields()
        load_contacts()

    except mysql.connector.IntegrityError:
        messagebox.showerror(
            "Duplicate Email",
            "This email already exists."
        )

    except mysql.connector.Error as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


def delete_contact():

    selected = contact_list.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a contact first."
        )
        return

    contact_id = contact_list.get(selected[0]).split("|")[0].strip()

    try:
        cursor.execute(
            "DELETE FROM Contact WHERE id = %s",
            (contact_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Contact deleted."
        )

        load_contacts()

    except mysql.connector.Error as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


def update_contact():

    selected = contact_list.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a contact first."
        )
        return

    contact_id = contact_list.get(selected[0]).split("|")[0].strip()

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    category = category_combo.get()
    notes = notes_text.get("1.0", tk.END).strip()

    if not name or not email:
        messagebox.showwarning(
            "Validation Error",
            "Name and email are required."
        )
        return

    if not valid_email(email):
        messagebox.showerror(
            "Invalid Email",
            "Enter a valid email address."
        )
        return

    try:
        cursor.execute("""
            UPDATE Contact
            SET name=%s,
                email=%s,
                phone=%s,
                category=%s,
                notes=%s
            WHERE id=%s
        """, (
            name,
            email,
            phone,
            category,
            notes,
            contact_id
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Contact updated."
        )

        load_contacts()

    except mysql.connector.IntegrityError:
        messagebox.showerror(
            "Duplicate Email",
            "This email already belongs to another contact."
        )

    except mysql.connector.Error as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


def search_contacts():

    search_value = search_entry.get().strip()

    contact_list.delete(0, tk.END)

    try:
        cursor.execute("""
            SELECT id, name, email, phone, category
            FROM Contact
            WHERE name LIKE %s
               OR email LIKE %s
               OR phone LIKE %s
            ORDER BY name ASC
        """, (
            "%" + search_value + "%",
            "%" + search_value + "%",
            "%" + search_value + "%"
        ))

        rows = cursor.fetchall()

        for row in rows:
            contact_list.insert(
                tk.END,
                f"{row[0]} | {row[1]} | {row[2]} | "
                f"{row[3]} | {row[4]}"
            )

    except mysql.connector.Error as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


def load_contacts():

    contact_list.delete(0, tk.END)

    try:
        cursor.execute("""
            SELECT id, name, email, phone, category
            FROM Contact
            ORDER BY name ASC
        """)

        rows = cursor.fetchall()

        for row in rows:
            contact_list.insert(
                tk.END,
                f"{row[0]} | {row[1]} | {row[2]} | "
                f"{row[3]} | {row[4]}"
            )

    except mysql.connector.Error as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


def select_contact(event):

    selected = contact_list.curselection()

    if not selected:
        return

    contact_id = contact_list.get(
        selected[0]
    ).split("|")[0].strip()

    try:
        cursor.execute("""
            SELECT name, email, phone, category, notes
            FROM Contact
            WHERE id=%s
        """, (contact_id,))

        row = cursor.fetchone()

        if row:
            clear_fields()

            name_entry.insert(0, row[0])
            email_entry.insert(0, row[1])
            phone_entry.insert(0, row[2] or "")
            category_combo.set(row[3])

            notes_text.insert(
                "1.0",
                row[4] or ""
            )

    except mysql.connector.Error as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


# ---------------- GUI ----------------

root = tk.Tk()
root.title("MySQL Contact Manager")
root.geometry("850x600")


# Name
tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root, width=50)
name_entry.pack()


# Email
tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root, width=50)
email_entry.pack()


# Phone
tk.Label(root, text="Phone").pack()
phone_entry = tk.Entry(root, width=50)
phone_entry.pack()


# Category - Combobox
tk.Label(root, text="Category").pack()

category_combo = ttk.Combobox(
    root,
    values=[
        "Friend",
        "Family",
        "Faculty",
        "Work",
        "Other"
    ],
    state="readonly",
    width=47
)

category_combo.set("Friend")
category_combo.pack()


# Notes - Text
tk.Label(root, text="Notes").pack()

notes_text = tk.Text(
    root,
    width=50,
    height=4
)

notes_text.pack()


# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Add",
    command=add_contact
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Update",
    command=update_contact
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Delete",
    command=delete_contact
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields
).grid(row=0, column=3, padx=5)


# Search
tk.Label(root, text="Search Name / Email / Phone").pack()

search_frame = tk.Frame(root)
search_frame.pack()

search_entry = tk.Entry(
    search_frame,
    width=40
)

search_entry.pack(side=tk.LEFT)

tk.Button(
    search_frame,
    text="Search",
    command=search_contacts
).pack(side=tk.LEFT, padx=5)

tk.Button(
    search_frame,
    text="Show All",
    command=load_contacts
).pack(side=tk.LEFT)


# Listbox
contact_list = tk.Listbox(
    root,
    width=100,
    height=15
)

contact_list.pack(pady=15)

contact_list.bind(
    "<<ListboxSelect>>",
    select_contact
)


# Load existing contacts
load_contacts()

root.mainloop()


# Close database connection
cursor.close()
conn.close()