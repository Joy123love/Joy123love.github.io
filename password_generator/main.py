import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import sqlite3
import datetime

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("450x650")
        self.root.configure(bg="#f0f0f0")

        # Database Setup
        self.conn = sqlite3.connect("passwords.db")
        self.create_table()

        # Fonts
        self.title_font = ("Helvetica", 20, "bold")
        self.label_font = ("Helvetica", 12)
        self.result_font = ("Courier New", 14, "bold")

        # Title
        tk.Label(self.root, text="Password Generator", font=self.title_font, bg="#f0f0f0", fg="#333").pack(pady=20)

        # Result Display
        self.password_var = tk.StringVar()
        self.result_entry = tk.Entry(self.root, textvariable=self.password_var, font=self.result_font, justify="center", state="readonly")
        self.result_entry.pack(fill="x", padx=40, pady=10)

        # Copy Button
        tk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard, bg="#2196F3", fg="white", font=("Helvetica", 10)).pack(pady=5)

        # Settings Frame
        settings_frame = tk.Frame(self.root, bg="#f0f0f0")
        settings_frame.pack(pady=20)

        # Length Slider
        tk.Label(settings_frame, text="Password Length:", font=self.label_font, bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=5)
        self.length_var = tk.IntVar(value=12)
        self.length_scale = tk.Scale(settings_frame, from_=4, to=32, orient="horizontal", variable=self.length_var, bg="#f0f0f0", length=200)
        self.length_scale.grid(row=1, column=0, columnspan=2, pady=5)

        # Options
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_numbers = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        tk.Checkbutton(settings_frame, text="Uppercase (A-Z)", variable=self.use_uppercase, bg="#f0f0f0", font=self.label_font).grid(row=2, column=0, sticky="w", padx=10, pady=2)
        tk.Checkbutton(settings_frame, text="Lowercase (a-z)", variable=self.use_lowercase, bg="#f0f0f0", font=self.label_font).grid(row=3, column=0, sticky="w", padx=10, pady=2)
        tk.Checkbutton(settings_frame, text="Numbers (0-9)", variable=self.use_numbers, bg="#f0f0f0", font=self.label_font).grid(row=2, column=1, sticky="w", padx=10, pady=2)
        tk.Checkbutton(settings_frame, text="Symbols (!@#$)", variable=self.use_symbols, bg="#f0f0f0", font=self.label_font).grid(row=3, column=1, sticky="w", padx=10, pady=2)

        # Generate Button
        tk.Button(self.root, text="Generate Password", command=self.generate_password, bg="#4CAF50", fg="white", font=("Helvetica", 14, "bold"), padx=20, pady=10).pack(pady=10)

        # Save Section
        save_frame = tk.Frame(self.root, bg="#f0f0f0")
        save_frame.pack(pady=10, fill="x", padx=40)

        tk.Label(save_frame, text="Account Name:", font=self.label_font, bg="#f0f0f0").pack(anchor="w")
        self.account_var = tk.StringVar()
        tk.Entry(save_frame, textvariable=self.account_var, font=("Helvetica", 12)).pack(fill="x", pady=5)

        btn_frame = tk.Frame(save_frame, bg="#f0f0f0")
        btn_frame.pack(fill="x", pady=5)

        tk.Button(btn_frame, text="Save Password", command=self.save_password, bg="#FF9800", fg="white", font=("Helvetica", 10, "bold")).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(btn_frame, text="View Saved", command=self.view_passwords, bg="#607D8B", fg="white", font=("Helvetica", 10, "bold")).pack(side="right", expand=True, fill="x", padx=2)

        # Initial Generation
        self.generate_password()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account TEXT NOT NULL,
                password TEXT NOT NULL,
                date TEXT
            )
        ''')
        self.conn.commit()

    def save_password(self):
        password = self.password_var.get()
        account = self.account_var.get().strip()

        if not password or password == "Select options!":
            messagebox.showwarning("Error", "No password to save!")
            return
        
        if not account:
            messagebox.showwarning("Error", "Please enter an Account Name.")
            return

        cursor = self.conn.cursor()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO passwords (account, password, date) VALUES (?, ?, ?)", (account, password, date))
        self.conn.commit()
        
        messagebox.showinfo("Success", f"Password for '{account}' saved!")
        self.account_var.set("") # Clear input

    def view_passwords(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("Saved Passwords")
        view_window.geometry("600x400")

        # Treeview
        columns = ("Account", "Password", "Date")
        tree = ttk.Treeview(view_window, columns=columns, show="headings")
        
        tree.heading("Account", text="Account")
        tree.heading("Password", text="Password")
        tree.heading("Date", text="Date Saved")
        
        tree.column("Account", width=150)
        tree.column("Password", width=250)
        tree.column("Date", width=150)

        tree.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Load Data
        cursor = self.conn.cursor()
        cursor.execute("SELECT account, password, date FROM passwords ORDER BY id DESC")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    def generate_password(self):
        length = self.length_var.get()
        chars = ""
        
        if self.use_uppercase.get():
            chars += string.ascii_uppercase
        if self.use_lowercase.get():
            chars += string.ascii_lowercase
        if self.use_numbers.get():
            chars += string.digits
        if self.use_symbols.get():
            chars += string.punctuation

        if not chars:
            self.password_var.set("Select options!")
            return

        password = "".join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password and password != "Select options!":
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
