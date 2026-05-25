import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

DATA_FILE = "finances.csv"


# ---------- Data functions ----------

def initialize_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["type", "amount", "description", "category", "date"])


def read_data():
    initialize_file()
    rows = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def write_row(type_, amount, description, category):
    initialize_file()
    date = datetime.now().strftime("%Y-%m-%d")
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([type_, amount, description, category, date])


def calculate_totals():
    data = read_data()
    income = sum(float(r["amount"]) for r in data if r["type"] == "income")
    expenses = sum(float(r["amount"]) for r in data if r["type"] == "expense")
    return income, expenses, income - expenses


# ---------- GUI ----------

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("720x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f2f5")

        self._build_header()
        self._build_form()
        self._build_table()
        self._build_summary()

        self.refresh()

    # --- Header ---

    def _build_header(self):
        frame = tk.Frame(self.root, bg="#2d6a4f", pady=14)
        frame.pack(fill="x")
        tk.Label(frame, text="💰 Personal Finance Tracker",
                 font=("Helvetica", 16, "bold"), fg="white", bg="#2d6a4f").pack()

    # --- Input form ---

    def _build_form(self):
        frame = tk.LabelFrame(self.root, text="New Transaction",
                              font=("Helvetica", 10, "bold"),
                              bg="#f0f2f5", fg="#333", padx=12, pady=10)
        frame.pack(fill="x", padx=16, pady=(12, 6))

        # Row 1: Amount + Description
        tk.Label(frame, text="Amount (€):", bg="#f0f2f5").grid(row=0, column=0, sticky="w")
        self.amount_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.amount_var, width=12).grid(row=0, column=1, padx=(4, 16), sticky="w")

        tk.Label(frame, text="Description:", bg="#f0f2f5").grid(row=0, column=2, sticky="w")
        self.desc_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.desc_var, width=22).grid(row=0, column=3, padx=(4, 16), sticky="w")

        tk.Label(frame, text="Category:", bg="#f0f2f5").grid(row=0, column=4, sticky="w")
        self.cat_var = tk.StringVar()
        categories = ["food", "transport", "entertainment", "health", "salary", "other"]
        ttk.Combobox(frame, textvariable=self.cat_var, values=categories,
                     width=14, state="readonly").grid(row=0, column=5, padx=(4, 16), sticky="w")
        self.cat_var.set("other")

        # Row 2: Buttons
        btn_frame = tk.Frame(frame, bg="#f0f2f5")
        btn_frame.grid(row=1, column=0, columnspan=6, pady=(10, 0), sticky="w")

        tk.Button(btn_frame, text="➕ Add Income", font=("Helvetica", 9, "bold"),
                  bg="#2d6a4f", fg="white", relief="flat", padx=12, pady=5,
                  cursor="hand2", command=self.add_income).pack(side="left", padx=(0, 8))

        tk.Button(btn_frame, text="➖ Add Expense", font=("Helvetica", 9, "bold"),
                  bg="#c0392b", fg="white", relief="flat", padx=12, pady=5,
                  cursor="hand2", command=self.add_expense).pack(side="left")

        self.status_var = tk.StringVar()
        tk.Label(btn_frame, textvariable=self.status_var, bg="#f0f2f5",
                 fg="#555", font=("Helvetica", 9)).pack(side="left", padx=14)

    # --- Transactions table ---

    def _build_table(self):
        frame = tk.LabelFrame(self.root, text="Transactions",
                              font=("Helvetica", 10, "bold"),
                              bg="#f0f2f5", fg="#333")
        frame.pack(fill="both", expand=True, padx=16, pady=(0, 6))

        cols = ("Type", "Amount", "Description", "Category", "Date")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)

        widths = [80, 90, 200, 120, 100]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center" if col != "Description" else "w")

        self.tree.tag_configure("income", foreground="#2d6a4f")
        self.tree.tag_configure("expense", foreground="#c0392b")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # --- Summary bar ---

    def _build_summary(self):
        frame = tk.Frame(self.root, bg="#2d6a4f", pady=8)
        frame.pack(fill="x")

        self.income_lbl = tk.Label(frame, text="", bg="#2d6a4f", fg="#b7e4c7",
                                   font=("Helvetica", 10))
        self.income_lbl.pack(side="left", padx=20)

        self.expense_lbl = tk.Label(frame, text="", bg="#2d6a4f", fg="#f4a6a0",
                                    font=("Helvetica", 10))
        self.expense_lbl.pack(side="left", padx=20)

        self.balance_lbl = tk.Label(frame, text="", bg="#2d6a4f", fg="white",
                                    font=("Helvetica", 11, "bold"))
        self.balance_lbl.pack(side="right", padx=20)

    # --- Logic ---

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in read_data():
            sign = "+" if row["type"] == "income" else "-"
            self.tree.insert("", "end",
                             values=(row["type"].capitalize(),
                                     f"{sign}{float(row['amount']):.2f} €",
                                     row["description"],
                                     row["category"],
                                     row["date"]),
                             tags=(row["type"],))

        income, expenses, balance = calculate_totals()
        self.income_lbl.config(text=f"Income: +{income:.2f} €")
        self.expense_lbl.config(text=f"Expenses: -{expenses:.2f} €")
        self.balance_lbl.config(text=f"Balance: {balance:+.2f} €")

    def _get_inputs(self):
        try:
            amount = float(self.amount_var.get())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive amount.")
            return None, None, None

        description = self.desc_var.get().strip()
        if not description:
            messagebox.showerror("Error", "Please enter a description.")
            return None, None, None

        category = self.cat_var.get()
        return amount, description, category

    def add_income(self):
        amount, description, category = self._get_inputs()
        if amount is None:
            return
        write_row("income", amount, description, category)
        self.status_var.set(f"✓ Income +{amount:.2f} € added")
        self._clear_inputs()
        self.refresh()

    def add_expense(self):
        amount, description, category = self._get_inputs()
        if amount is None:
            return
        write_row("expense", amount, description, category)
        self.status_var.set(f"✓ Expense -{amount:.2f} € recorded")
        self._clear_inputs()
        self.refresh()

    def _clear_inputs(self):
        self.amount_var.set("")
        self.desc_var.set("")
        self.cat_var.set("other")


# ---------- Entry point ----------

if __name__ == "__main__":
    initialize_file()
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()