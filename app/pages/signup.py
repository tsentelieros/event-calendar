import tkinter as tk
from tkinter import ttk, messagebox, END
from app.controllers import create_user

class SignupPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Τίτλος σελίδας
        title_label = ttk.Label(self, text="Sign-up", style="Header.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Username field
        ttk.Label(self, text="Όνομα:", style="TLabel").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)
        self.username_entry.insert(0, "Όνομα χρήστη")
        self.username_entry.bind("<FocusIn>", self.clear_username_placeholder)

        # Password field
        ttk.Label(self, text="Κωδικός:", style="TLabel").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)
        self.password_entry.insert(0, "Κωδικός")
        self.password_entry.bind("<FocusIn>", self.clear_password_placeholder)

        # Confirm password field
        ttk.Label(self, text="Επιβεβαίωση Κωδικού:", style="TLabel").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.confirm_entry = ttk.Entry(self, show="*")
        self.confirm_entry.grid(row=3, column=1, padx=10, pady=5)
        self.confirm_entry.insert(0, "Επιβεβαιώστε κωδικό")
        self.confirm_entry.bind("<FocusIn>", self.clear_confirm_placeholder)

        # Sign up button (disabled until valid input)
        self.signup_btn = ttk.Button(
            self,
            text="Sign up",
            style="Primary.TButton",
            state="disabled",
            cursor="hand2",
            command=self.attempt_signup,
        )
        self.signup_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Back to Login
        back_btn = ttk.Button(
            self, text="Back to Login",cursor="hand2",
            command=lambda: controller.show_frame("LoginPage")
        )
        back_btn.grid(row=5, column=0, columnspan=2)

        # Παρακολούθηση αλλαγών για ενεργοποίηση κουμπιού
        self.username_entry.bind("<KeyRelease>", self.update_signup_state)
        self.password_entry.bind("<KeyRelease>", self.update_signup_state)
        self.confirm_entry.bind("<KeyRelease>", self.update_signup_state)



    def clear_username_placeholder(self, event):
        if self.username_entry.get() == "Όνομα χρήστη":
            self.username_entry.delete(0, END)

    def clear_password_placeholder(self, event):
        if self.password_entry.get() == "Κωδικός":
            self.password_entry.delete(0, END)
            self.password_entry.config(show="*")

    def clear_confirm_placeholder(self, event):
        if self.confirm_entry.get() == "Επιβεβαιώστε κωδικό":
            self.confirm_entry.delete(0, END)
            self.confirm_entry.config(show="*")

    def update_signup_state(self, event=None):
        user = self.username_entry.get().strip()
        pwd = self.password_entry.get().strip()
        conf = self.confirm_entry.get().strip()
        if (user and pwd and conf and pwd == conf
                and user != "Όνομα χρήστη"
                and pwd != "Κωδικός"
                and conf != "Επιβεβαιώστε κωδικό"):
            self.signup_btn.config(state="normal")
        else:
            self.signup_btn.config(state="disabled")

    def attempt_signup(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if create_user(username, password):
            messagebox.showinfo("Success", f"Ο χρήστης {username} δημιουργήθηκε!")
            self.controller.show_frame("LoginPage")
        else:
            messagebox.showerror("Error", "Το όνομα χρήστη υπάρχει ήδη.")
