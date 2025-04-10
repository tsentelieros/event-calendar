import tkinter as tk
import calendar
import datetime

root = tk.Tk()
root.title("Ημερολόγιο Μήνα")
root.geometry("300x250")

# Δημιουργία Menu Bar
menu_bar = tk.Menu(root)

# Δημιουργία του "Αρχείο" μενού
year_menu = tk.Menu(menu_bar, tearoff=0)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Νέο event")
file_menu.add_command(label="Διαγραφή event")

# Προσθήκη του "Αρχείο" στο menu bar
menu_bar.add_cascade(label="Επιλέξτε έτος", menu=year_menu)
menu_bar.add_cascade(label="Events", menu=file_menu)

# Προσθήκη του Menu Bar στο παράθυρο
root.config(menu=menu_bar)

# ----- Προσθήκη του μήνα και των ημερών -----
today = datetime.date.today()
month_name = today.strftime("%B")  # Όνομα τρέχοντος μήνα
current_year = today.year
current_month = today.month
current_day = today.day  # Σημερινή ημέρα

# Λήψη ημερών του μήνα
days = calendar.monthcalendar(current_year, current_month)

# Ετικέτα για τον μήνα
month_label = tk.Label(root, text=f"{month_name} {current_year}", font=("Arial", 14, "bold"))
month_label.pack(pady=10)

# Πλαίσιο για τις ημέρες
frame = tk.Frame(root)
frame.pack()

# Εμφάνιση ημερών της εβδομάδας
weekdays = ["Δε", "Τρ", "Τε", "Πε", "Πα", "Σα", "Κυ"]
header = tk.Frame(frame)
header.pack()
for day in weekdays:
    day_label = tk.Label(header, text=day, width=4, font=("Arial", 10, "bold"))
    day_label.pack(side="left")

# Προσθήκη ημερών σε πίνακα
for week in days:
    row_frame = tk.Frame(frame)
    row_frame.pack()
    for day in week:
        if day == current_day:
            font_style = ("Arial", 12, "bold")  # Η σημερινή ημερομηνία με bold
            fg_color = "red"
        else:
            font_style = ("Arial", 12)
            fg_color = "black"

        day_text = str(day) if day != 0 else ""  # Αν είναι 0, σημαίνει ότι δεν ανήκει στον μήνα
        day_label = tk.Label(row_frame, text=day_text, width=4, font=font_style, fg=fg_color, borderwidth=1, relief="solid")
        day_label.pack(side="left", padx=2, pady=2)

root.mainloop()
