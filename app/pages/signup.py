import tkinter as tk
import menu_page

def create_signup(parent):
    # Δημιουργία του frame για τη σελίδα εγγραφής
    signup_frame = tk.Frame(parent)
    signup_frame.pack(padx=10, pady=10)

    # Τίτλος
    label1 = tk.Label(signup_frame, text="Sign-up", font=("Bookman Old Style", 16))
    label1.grid(row=0, column=0, columnspan=2, pady=10)

    # Label και Entry για "Όνομα"
    tk.Label(signup_frame, text="Όνομα:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry1 = tk.Entry(signup_frame)
    entry1.grid(row=1, column=1, padx=10, pady=5)

    # Label και Entry για "Κωδικός"
    tk.Label(signup_frame, text="Κωδικός:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry2 = tk.Entry(signup_frame, show="*")  # Το "show='*'" κρύβει τον κωδικό
    entry2.grid(row=2, column=1, padx=10, pady=5)

    # Label και Entry για Επιβεβαίωση κωδικού
    tk.Label(signup_frame, text="Eπιβεβαίωση Κωδικού:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry3 = tk.Entry(signup_frame, show="*")  # Το "show='*'" κρύβει τον κωδικό
    entry3.grid(row=3, column=1, padx=10, pady=5)

    # Button για sign up
    signup_btn = tk.Button(signup_frame, text="Sign up", cursor="hand2", padx=20, pady=5)
    signup_btn.grid(row=4, column=0, columnspan=2, pady=5)


