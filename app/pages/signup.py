import tkinter as tk

root = tk.Tk()
root.title("Ημερολόγιο")
root.geometry("300x220")

label1 = tk.Label(root, text="Sign-up", font=("Bookman Old Style", 16))
label1.grid(row=0, column=0, columnspan=2, pady=10)

# Label και Entry για "Όνομα"
tk.Label(root, text="Όνομα:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry1 = tk.Entry(root)
entry1.grid(row=1, column=1, padx=10, pady=5)

# Label και Entry για "Κωδικός"
tk.Label(root, text="Κωδικός:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry2 = tk.Entry(root, show="*")  # Το "show='*'" κρύβει τον κωδικό
entry2.grid(row=2, column=1, padx=10, pady=5)

# Label και Entry για Επιβεβαίωση κωδικού
tk.Label(root, text="Eπιβεβαίωση Κωδικού:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry3 = tk.Entry(root, show="*")  # Το "show='*'" κρύβει τον κωδικό
entry3.grid(row=3, column=1, padx=10, pady=5)

# Button για sign up
signup_btn = tk.Button(root, text="Sign up", cursor="hand2", padx=20, pady=5)
signup_btn.grid(row=4, column=0, columnspan=2, pady=5)


root.mainloop()
