import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as font

# DAO imports
from transaction_dao import add_transaction, get_all_transactions, update_transaction, delete_transaction
from category_dao import get_all_categories, add_category, delete_category


class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("1000x600")
        self.root.configure(bg="white")

        # GLOBAL FONTS
        self.title_font = ("SF Pro Text", 22, "bold")
        self.heading_font = ("SF Pro Text", 18, "bold")
        self.text_font = ("SF Pro Text", 14)
        self.sidebar_font = ("SF Pro Text", 14, "bold")

        # COLORS
        self.sidebar_bg = "#E9ECEF"
        self.btn_bg = "#CED4DA"
        self.btn_fg = "#212529"
        self.btn_hover = "#ADB5BD"
        self.main_bg = "white"

        # --- SIDEBAR ---
        self.sidebar = tk.Frame(self.root, width=250, bg=self.sidebar_bg, padx=20, pady=20)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(
            self.sidebar, text="Budget Tracker", bg=self.sidebar_bg, fg="#212529",
            font=("SF Pro Text", 20, "bold")
        ).pack(pady=(0, 20))

        # Sidebar Buttons
        self.create_sidebar_button("Dashboard", self.show_dashboard)
        self.create_sidebar_button("Add Transaction", self.show_add_transaction)
        self.create_sidebar_button("View Transactions", self.show_transactions)
        self.create_sidebar_button("Manage Categories", self.show_categories)

        # --- MAIN CONTENT ---
        self.content = tk.Frame(self.root, bg=self.main_bg)
        self.content.pack(side="right", expand=True, fill="both")

        self.show_dashboard()

    # ------------------------------------------------------------------
    # Sidebar button with hover effects
    # ------------------------------------------------------------------
    def create_sidebar_button(self, text, command):
        btn = tk.Button(
            self.sidebar,
            text=text,
            font=self.sidebar_font,
            bg=self.btn_bg,
            fg=self.btn_fg,
            relief="flat",
            command=command,
            padx=10,
            pady=10,
        )
        btn.pack(fill="x", pady=5)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.btn_hover))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.btn_bg))

    # ------------------------------------------------------------------
    # DASHBOARD
    # ------------------------------------------------------------------
    def show_dashboard(self):
        self.clear_content()

        tk.Label(self.content, text="Dashboard Overview",
                 font=self.title_font, bg=self.main_bg).pack(pady=20)

        data = get_all_transactions()
        total_income = sum(t[3] for t in data if t[1] == "income")
        total_expense = sum(t[3] for t in data if t[1] == "expense")
        balance = total_income - total_expense

        # Card Container
        card_frame = tk.Frame(self.content, bg=self.main_bg)
        card_frame.pack(pady=20)

        def create_card(parent, title, value, color):
            card = tk.Frame(parent, bg="white", padx=30, pady=25,
                            highlightbackground="#CED4DA", highlightthickness=1)
            card.pack(side="left", padx=20)

            tk.Label(card, text=title, font=("SF Pro Text", 14), bg="white",
                     fg="#6C757D").pack()
            tk.Label(card, text=f"₱{value:.2f}", font=("SF Pro Text", 20, "bold"),
                     fg=color, bg="white").pack(pady=10)

        create_card(card_frame, "Total Income", total_income, "#2E8B57")
        create_card(card_frame, "Total Expense", total_expense, "#C0392B")
        balance_color = "#2E8B57" if balance >= 0 else "#C0392B"
        create_card(card_frame, "Balance", balance, balance_color)

        tk.Label(self.content, text="(Charts coming soon...)",
                 font=("SF Pro Text", 14, "italic"),
                 bg=self.main_bg, fg="#6C757D").pack(pady=20)

    # ------------------------------------------------------------------
    # ADD TRANSACTION
    # ------------------------------------------------------------------
    def show_add_transaction(self):
        self.transaction_form(title="Add Transaction", submit_text="Save Transaction",
                              submit_callback=self.save_new_transaction)

    def save_new_transaction(self, entries):
        type_val = entries["Type"].get()
        cat_val = entries["Category"].get()
        amount_val = entries["Amount"].get()
        date_val = entries["Date (YYYY-MM-DD)"].get()
        note_val = entries["Note"].get()

        if not type_val or not cat_val or not amount_val or not date_val:
            messagebox.showerror("Error", "Fill all required fields.")
            return

        try:
            amount = float(amount_val)
        except:
            messagebox.showerror("Error", "Amount must be numeric.")
            return

        for c in get_all_categories():
            if c[1] == cat_val:
                cat_id = c[0]

        add_transaction(type_val, cat_id, amount, date_val, note_val)
        messagebox.showinfo("Success", "Transaction added!")
        self.show_dashboard()

    # ------------------------------------------------------------------
    # VIEW TRANSACTIONS
    # ------------------------------------------------------------------
    def show_transactions(self):
        self.clear_content()

        tk.Label(self.content, text="Transaction Records",
                 font=self.title_font, bg=self.main_bg).pack(pady=20)

        columns = ("ID", "Type", "Category", "Amount", "Date", "Note")
        tree = ttk.Treeview(self.content, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)

        tree.pack(fill="both", expand=True, padx=20, pady=10)

        def load():
            for row in tree.get_children():
                tree.delete(row)
            for r in get_all_transactions():
                tree.insert("", "end", values=r)

        load()

        tk.Button(self.content, text="Delete Selected", bg="#FF6B6B", fg="white",
                  font=self.sidebar_font, padx=15, pady=8,
                  relief="flat", command=lambda: self.delete_transaction(tree, load))\
            .pack(pady=10)

        tk.Button(self.content, text="Update Selected", bg="#4CAF50", fg="white",
                  font=self.sidebar_font, padx=15, pady=8,
                  relief="flat", command=lambda: self.update_transaction(tree))\
            .pack(pady=5)

    def delete_transaction(self, tree, reload_func):
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a record.")
            return
        trans_id = tree.item(sel[0])["values"][0]
        delete_transaction(trans_id)
        reload_func()
        messagebox.showinfo("Success", "Deleted!")

    # ------------------------------------------------------------------
    # UPDATE TRANSACTION (in main content)
    # ------------------------------------------------------------------
    def update_transaction(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a record to update.")
            return

        trans = tree.item(sel[0])["values"]
        self.transaction_form(title="Update Transaction", submit_text="Update Transaction",
                              submit_callback=lambda entries: self.save_updated_transaction(entries, trans[0]),
                              existing_data=trans)

    def save_updated_transaction(self, entries, trans_id):
        type_val = entries["Type"].get()
        cat_val = entries["Category"].get()
        amount_val = entries["Amount"].get()
        date_val = entries["Date (YYYY-MM-DD)"].get()
        note_val = entries["Note"].get()

        if not type_val or not cat_val or not amount_val or not date_val:
            messagebox.showerror("Error", "Fill all required fields.")
            return

        try:
            amount = float(amount_val)
        except:
            messagebox.showerror("Error", "Amount must be numeric.")
            return

        for c in get_all_categories():
            if c[1] == cat_val:
                cat_id = c[0]

        update_transaction(trans_id, type_val, cat_id, amount, date_val, note_val)
        messagebox.showinfo("Success", "Transaction updated!")
        self.show_transactions()

    # ------------------------------------------------------------------
    # MANAGE CATEGORIES
    # ------------------------------------------------------------------
    def show_categories(self):
        self.clear_content()

        tk.Label(self.content, text="Manage Categories",
                 font=self.title_font, bg=self.main_bg).pack(pady=20)

        form = tk.Frame(self.content, bg=self.main_bg)
        form.pack()

        tk.Label(form, text="New Category:", font=self.text_font, bg=self.main_bg)\
            .grid(row=0, column=0, padx=5)

        cat_entry = tk.Entry(form, font=self.text_font, width=22)
        cat_entry.grid(row=0, column=1)

        tk.Button(form, text="Add", font=self.sidebar_font, bg=self.btn_bg,
                  fg=self.btn_fg, relief="flat", padx=10, pady=5,
                  command=lambda: self.add_cat(cat_entry))\
            .grid(row=0, column=2, padx=10)

        # category list
        tree = ttk.Treeview(self.content, columns=("ID", "Name"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.pack(fill="both", expand=True, padx=20, pady=10)

        def refresh():
            for row in tree.get_children():
                tree.delete(row)
            for c in get_all_categories():
                tree.insert("", "end", values=c)

        refresh()

        tk.Button(self.content, text="Delete Selected", bg="#FF6B6B", fg="white",
                  font=self.sidebar_font, padx=15, pady=8, relief="flat",
                  command=lambda: self.delete_category(tree, refresh))\
            .pack(pady=10)

    def add_cat(self, entry):
        name = entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Category name required.")
            return
        add_category(name)
        messagebox.showinfo("Success", "Category added!")

    def delete_category(self, tree, refresh):
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a category.")
            return
        cat_id = tree.item(sel[0])["values"][0]
        delete_category(cat_id)
        refresh()
        messagebox.showinfo("Success", "Deleted!")

    # ------------------------------------------------------------------
    # TRANSACTION FORM (Reusable for Add / Update in main content)
    # ------------------------------------------------------------------
    def transaction_form(self, title, submit_text, submit_callback, existing_data=None):
        self.clear_content()  # Clear content to render form

        tk.Label(self.content, text=title, font=self.title_font, bg=self.main_bg).pack(pady=20)

        form = tk.Frame(self.content, bg=self.main_bg)
        form.pack(pady=10)

        fields = ["Type", "Category", "Amount", "Date (YYYY-MM-DD)", "Note"]
        entries = {}

        prefill = {}
        if existing_data:
            prefill = {
                "Type": existing_data[1],
                "Category": existing_data[2],
                "Amount": existing_data[3],
                "Date (YYYY-MM-DD)": existing_data[4],
                "Note": existing_data[5]
            }

        for i, field in enumerate(fields):
            tk.Label(form, text=field, font=self.text_font, bg=self.main_bg).grid(row=i, column=0, sticky="w", pady=8, padx=5)

            if field == "Type":
                var = tk.StringVar(value=prefill.get(field, ""))
                box = ttk.Combobox(form, textvariable=var, font=self.text_font,
                                   values=["income", "expense"], width=20)
                entries[field] = var
            elif field == "Category":
                categories = get_all_categories()
                names = [c[1] for c in categories]
                var = tk.StringVar(value=prefill.get(field, ""))
                box = ttk.Combobox(form, textvariable=var, font=self.text_font,
                                   values=names, width=20)
                entries[field] = var
            else:
                ent = tk.Entry(form, font=self.text_font, width=22)
                if prefill.get(field):
                    ent.insert(0, prefill[field])
                entries[field] = ent
                box = ent

            box.grid(row=i, column=1)

        tk.Button(self.content, text=submit_text, bg=self.btn_bg, fg=self.btn_fg,
                  font=self.sidebar_font, relief="flat", padx=20, pady=10,
                  command=lambda: submit_callback(entries))\
            .pack(pady=20)

    # ------------------------------------------------------------------
    # CLEAR CONTENT
    # ------------------------------------------------------------------
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()


# RUN APP
root = tk.Tk()
app = BudgetApp(root)
root.mainloop()
