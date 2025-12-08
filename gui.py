import tkinter as tk
from tkinter import ttk, messagebox
import models


class BudgetGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Budge It - Budget Tracking System")
        self.root.geometry("950x650")
        self.root.config(bg="#F2F2F7")

        ### ---------- COLORS ----------
        self.card_bg = "#FFFFFF"
        self.text_color = "#1C1C1E"
        self.accent = "#0A84FF"
        self.border = "#D1D1D6"

        ### ---------- INPUT VARIABLES ----------
        self.amount_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.notes_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()

        ### ---------- TOP TITLE BAR ----------
        title = tk.Label(
            root,
            text="Budge It — Budget Tracking System",
            font=("Helvetica", 22, "bold"),
            bg="#F2F2F7",
            fg=self.text_color,
            pady=20
        )
        title.pack(fill="x")

        ### ---------- INPUT CARD ----------
        form_frame = tk.Frame(root, bg=self.card_bg, bd=1, relief="solid")
        form_frame.pack(fill="x", padx=20, pady=(0,15))
        form_frame.configure(highlightbackground=self.border, highlightthickness=1)

        padding = {"padx":15, "pady":8}

        tk.Label(form_frame, text="Amount", bg=self.card_bg).grid(row=0, column=0, sticky="w", **padding)
        tk.Entry(form_frame, textvariable=self.amount_var, width=20).grid(row=0, column=1, **padding)

        tk.Label(form_frame, text="Type", bg=self.card_bg).grid(row=0, column=2, sticky="w", **padding)
        type_box = ttk.Combobox(form_frame, textvariable=self.type_var, values=["Income","Expense"], width=18)
        type_box.grid(row=0, column=3, **padding)

        tk.Label(form_frame, text="Category", bg=self.card_bg).grid(row=1, column=0, sticky="w", **padding)
        self.category_cb = ttk.Combobox(form_frame, textvariable=self.category_var, width=20)
        self.category_cb.grid(row=1, column=1, **padding)

        tk.Label(form_frame, text="Date (YYYY-MM-DD)", bg=self.card_bg).grid(row=1, column=2, sticky="w", **padding)
        tk.Entry(form_frame, textvariable=self.date_var, width=18).grid(row=1, column=3, **padding)

        tk.Label(form_frame, text="Notes", bg=self.card_bg).grid(row=2, column=0, sticky="w", **padding)
        tk.Entry(form_frame, textvariable=self.notes_var, width=45).grid(row=2, column=1, columnspan=3, sticky="w", **padding)

        ### ---------- BUTTON STYLE ----------
        style = {
            "font": ("Helvetica", 11),
            "width": 12,
            "bd": 0,
            "padx": 10,
            "pady": 6
        }

        tk.Button(form_frame, text="Add", command=self.add, bg=self.accent, fg="white", **style).grid(row=3, column=0, pady=10)
        tk.Button(form_frame, text="Update", command=self.update, bg="#5E5CE6", fg="white", **style).grid(row=3, column=1)
        tk.Button(form_frame, text="Delete", command=self.delete, bg="#FF453A", fg="white", **style).grid(row=3, column=2)
        tk.Button(form_frame, text="Show All", command=self.load, bg="#8E8E93", fg="white", **style).grid(row=3, column=3)

        ### ---------- FILTER CARD ----------
        filter_frame = tk.Frame(root, bg=self.card_bg, bd=1, relief="solid")
        filter_frame.pack(fill="x", padx=20, pady=(0,15))
        filter_frame.configure(highlightbackground=self.border, highlightthickness=1)

        tk.Label(filter_frame, text="Start Date", bg=self.card_bg).grid(row=0, column=0, **padding)
        tk.Entry(filter_frame, textvariable=self.start_date_var, width=15).grid(row=0, column=1, **padding)

        tk.Label(filter_frame, text="End Date", bg=self.card_bg).grid(row=0, column=2, **padding)
        tk.Entry(filter_frame, textvariable=self.end_date_var, width=15).grid(row=0, column=3, **padding)

        tk.Button(filter_frame, text="Filter", command=self.filter, bg="#64D2FF", fg=self.text_color, **style).grid(row=0, column=4, padx=20)

        ### ---------- BALANCE CARD ----------
        balance_frame = tk.Frame(root, bg=self.card_bg, bd=1, relief="solid")
        balance_frame.pack(fill="x", padx=20, pady=(0,15))
        balance_frame.configure(highlightbackground=self.border, highlightthickness=1)

        self.balance_label = tk.Label(
            balance_frame,
            text="TOTAL BALANCE: ₱ 0.00",
            font=("Helvetica", 18, "bold"),
            bg=self.card_bg,
            fg=self.text_color,
            pady=10
        )
        self.balance_label.pack()

        ### ---------- TABLE CARD ----------
        table_frame = tk.Frame(root, bg=self.card_bg, bd=1, relief="solid")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))
        table_frame.configure(highlightbackground=self.border, highlightthickness=1)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id","category","type","amount","date","notes"),
            show="headings"
        )
        self.tree.pack(fill="both", expand=True)

        for col in ("id","category","type","amount","date","notes"):
            self.tree.heading(col, text=col)

        ### ---------- LOAD INITIAL DATA ----------
        self.load_categories()
        self.load()

    ### ---------- DATA FUNCTIONS ----------

    def load_categories(self):
        rows = models.get_categories()
        self.category_cb['values'] = [row[0] for row in rows]

    def clear_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def load(self):
        self.clear_table()
        rows = models.get_all_transactions()
        for r in rows:
            self.tree.insert("", tk.END, values=r)
        self.update_balance()

    def add(self):
        models.add_transaction(
            self.category_var.get(),
            self.amount_var.get(),
            self.type_var.get(),
            self.date_var.get(),
            self.notes_var.get()
        )
        self.load()
        messagebox.showinfo("Success", "Transaction Added")

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            return
        tid = self.tree.item(selected)["values"][0]
        models.delete_transaction(tid)
        self.load()
        messagebox.showinfo("Deleted", "Transaction Removed")

    def update(self):
        selected = self.tree.selection()
        if not selected:
            return
        tid = self.tree.item(selected)["values"][0]
        models.update_transaction(tid, self.amount_var.get(), self.notes_var.get())
        self.load()
        messagebox.showinfo("Updated", "Transaction Updated")

    def filter(self):
        start = self.start_date_var.get()
        end = self.end_date_var.get()

        if not start or not end:
            messagebox.showwarning("Invalid", "Enter both start AND end date")
            return

        self.clear_table()
        rows = models.get_filtered_transactions(start, end)
        for r in rows:
            self.tree.insert("", tk.END, values=r)

        self.update_balance(start, end)

    def update_balance(self, start=None, end=None):
        balance = models.get_total_balance(start, end)
        self.balance_label.config(text=f"TOTAL BALANCE: ₱ {balance:,.2f}")
