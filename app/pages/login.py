import tkinter as tk
import signup

root = tk.Tk()
root.title("Ημερολόγιο")
root.geometry("300x220")

# Δημιουργία του login frame
login_frame = tk.Frame(root)

# Τίτλος
label1 = tk.Label(login_frame, text="Ημερολόγιο", font=("Bookman Old Style", 16))
label1.grid(row=0, column=0, columnspan=2, pady=10)

# Label και Entry για "Όνομα"
tk.Label(login_frame, text="Όνομα:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry1 = tk.Entry(login_frame)
entry1.grid(row=1, column=1, padx=10, pady=5)

# Label και Entry για "Κωδικός"
tk.Label(login_frame, text="Κωδικός:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry2 = tk.Entry(login_frame, show="*")  # Το "show='*'" κρύβει τον κωδικό
entry2.grid(row=2, column=1, padx=10, pady=5)

# Κουμπί Log in
login_btn = tk.Button(login_frame, text="Log in", cursor="hand2", padx=20, pady=5)
login_btn.grid(row=3, column=0, columnspan=2, pady=5)

# Γραμμή "or"
label3 = tk.Label(login_frame, text="or", font=("Arial", 8))
label3.grid(row=4, column=0, columnspan=2, pady=2)

# Κουμπί Sign Up (Υπογραμμισμένο, σαν link)
signup_btn = tk.Button(login_frame, text="Sign Up", font=("Arial", 10, "underline"),
                       borderwidth=0, highlightthickness=0, cursor="hand2", fg="blue", command=lambda: show_signup())
signup_btn.grid(row=5, column=0, columnspan=2, pady=0)

# Εμφάνιση του login frame
login_frame.pack(padx=10, pady=10)

# Συνάρτηση για να μεταβείς στην σελίδα signup
def show_signup():
    # Κλείνουμε το παράθυρο login και ανοίγουμε το signup
    login_frame.pack_forget()  # Κρύβουμε το login frame
    signup_page.create_signup(root)  # Υποθέτουμε ότι η συνάρτηση create_signup δημιουργεί το signup interface

root.mainloop()
