from tkinter import END, messagebox, ttk

class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20, style="Card.TFrame")
        self.controller = controller

        # Στήσιμο 2 στηλών: η πρώτη για labels (weight=1), η δεύτερη για entries (weight=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        # Τίτλος
        self.title_label = ttk.Label(self, text="EventCalendar", style="Header.TLabel")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0,20))

        # Username
        ttk.Label(self, text="Όνομα:", style="TLabel").grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        self.username_entry = ttk.Entry(self, style="TEntry")
        self.username_entry.insert(0, "Όνομα χρήστη")
        self.username_entry.bind("<FocusIn>", self.clear_username_placeholder)
        self.username_entry.grid(row=1, column=1, sticky="we", padx=5, pady=5)

        # Password
        ttk.Label(self, text="Κωδικός:", style="TLabel").grid(
            row=2, column=0, sticky="e", padx=5, pady=5
        )
        self.password_entry = ttk.Entry(self, show="", style="TEntry")
        self.password_entry.insert(0, "Κωδικός")
        self.password_entry.bind("<FocusIn>", self.clear_password_placeholder)
        self.password_entry.grid(row=2, column=1, sticky="we", padx=5, pady=5)

        # Log in button (απενεργοποιημένο μέχρι να συμπληρωθούν τα πεδία)
        self.login_btn = ttk.Button(
            self,
            text="Log in",
            style="Primary.TButton",
            state="disabled",
            cursor="hand2",
            command=self.attempt_login
        )
        self.login_btn.grid(row=3, column=0, columnspan=2, sticky="we", pady=(15,5))

        # "or"
        self.or_label = ttk.Label(self, text="or", style="TLabel")
        self.or_label.grid(row=4, column=0, columnspan=2, pady=(5,5))

        # Sign up button
        self.signup_btn = ttk.Button(
            self,
            text="Sign Up",
            style="Link.TButton",
            cursor="hand2",
            command=lambda: controller.show_frame("SignupPage")
        )
        self.signup_btn.grid(row=5, column=0, columnspan=2, sticky="we", pady=(5,0))
        # Test comment
        # Παρακολούθηση αλλαγών για ενεργοποίηση κουμπιού
        self.username_entry.bind("<KeyRelease>", self.update_login_state)
        self.password_entry.bind("<KeyRelease>", self.update_login_state)

        

    def clear_username_placeholder(self, event):
        if self.username_entry.get() == "Όνομα χρήστη":
            self.username_entry.delete(0, END)

    def clear_password_placeholder(self, event):
        if self.password_entry.get() == "Κωδικός":
            self.password_entry.delete(0, END)
            self.password_entry.config(show="*")

    def update_login_state(self, event=None):
        """Ενεργοποιεί το κουμπί όταν υπάρχουν κείμενα και στα δύο πεδία."""
        user = self.username_entry.get().strip()
        pwd = self.password_entry.get().strip()
        if user and pwd and user != "Όνομα χρήστη" and pwd != "Κωδικός":
            self.login_btn.state(["!disabled"])
        else:
            self.login_btn.state(["disabled"])

    def attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        from app.controllers import check_user
        if check_user(username, password):
            messagebox.showinfo("Success", f"Welcome {username}!")
            self.controller.show_frame("CalendarPage")
        else:
            messagebox.showerror("Error", "Λανθασμένο όνομα ή κωδικός.")