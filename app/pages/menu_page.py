import tkinter as tk
import calendar
import datetime
from tkinter import messagebox

root = tk.Tk()
root.title("Ημερολόγιο Μήνα")
root.geometry("300x300")

# Μεταβλητές για επιλεγμένο έτος και μήνα
selected_year = datetime.date.today().year
selected_month = datetime.date.today().month

# --------- Συνάρτηση για ανανέωση του ημερολογίου ----------
def update_calendar(year, month):
    global selected_year, selected_month
    selected_year = year
    selected_month = month

    month_label.config(text=f"{calendar.month_name[month]} {year}")

    # Καθαρισμός προηγούμενων ημερών
    for widget in frame.winfo_children():
        widget.destroy()

    # Επικεφαλίδα ημερών
    header = tk.Frame(frame)
    header.pack()
    for day in weekdays:
        day_label = tk.Label(header, text=day, width=4, font=("Arial", 10, "bold"))
        day_label.pack(side="left")

    # Ημέρες του μήνα
    days = calendar.monthcalendar(year, month)
    today = datetime.date.today()

    for week in days:
        row_frame = tk.Frame(frame)
        row_frame.pack()
        for day in week:
            if day == today.day and year == today.year and month == today.month:
                font_style = ("Arial", 12, "bold")
                fg_color = "red"
            else:
                font_style = ("Arial", 12)
                fg_color = "black"
            day_text = str(day) if day != 0 else ""
            day_label = tk.Label(row_frame, text=day_text, width=4, font=font_style, fg=fg_color, borderwidth=1, relief="solid")
            day_label.pack(side="left", padx=2, pady=2)

# --------- Συνάρτηση για την αλλαγή μήνα (δεξιά ή αριστερά) ----------
def change_month(increment):
    global selected_year, selected_month
    new_month = selected_month + increment
    if new_month < 1:  # Αν πάμε πριν τον Ιανουάριο, πάμε στο Δεκέμβριο του προηγούμενου έτους
        new_month = 12
        selected_year -= 1
    elif new_month > 12:  # Αν πάμε μετά τον Δεκέμβριο, πάμε στον Ιανουάριο του επόμενου έτους
        new_month = 1
        selected_year += 1

    update_calendar(selected_year, new_month)

# --------- Συνάρτηση για το άνοιγμα του input για το έτος ---------
def open_year_input():
    def set_year(event=None):  # Επέκταση για να δέχεται και το event του Enter
        try:
            y = int(year_entry.get())
            if 1930 <= y <= 2125:
                update_calendar(y, selected_month)
                popup.destroy()  # Κλείνει ΜΟΝΟ αν η είσοδος είναι σωστή
            else:
                messagebox.showerror("Σφάλμα", "Εισάγετε έτος από 1930 έως 2125.")
        except ValueError:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε έναν αριθμό.")

    popup = tk.Toplevel(root)
    popup.title("Επιλογή Έτους")
    popup.geometry("250x100")
    popup.resizable(False, False)

    popup.transient(root)
    popup.grab_set()
    popup.focus_force()

    tk.Label(popup, text="Εισάγετε έτος (1930-2125):").pack(pady=5)
    year_entry = tk.Entry(popup, justify="center")
    year_entry.pack(pady=5)
    year_entry.focus()

    # Σύνδεση Enter με την υποβολή
    year_entry.bind("<Return>", set_year)

    tk.Button(popup, text="OK", command=set_year).pack(pady=5)


# --------- Συνάρτηση για την επιστροφή στο σήμερα ---------
def go_to_today():
    today = datetime.date.today()
    update_calendar(today.year, today.month)

# -------- Menu Bar --------
menu_bar = tk.Menu(root)

# Προσθήκη της επιλογής "Σήμερα"
menu_bar.add_command(label="Σήμερα", command=go_to_today)

# Αντί για υπομενού, κατευθείαν εντολή για "Επιλέξτε έτος"
menu_bar.add_command(label="Επιλέξτε έτος", command=open_year_input)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="All events")
file_menu.add_command(label="Νέο event")
file_menu.add_command(label="Διαγραφή event")
menu_bar.add_cascade(label="Events", menu=file_menu)

root.config(menu=menu_bar)

# -------- Μήνας και κουμπιά αλλαγής μήνα --------
month_frame = tk.Frame(root)
month_frame.pack(pady=10)

left_arrow = tk.Button(month_frame, text="<", command=lambda: change_month(-1))
left_arrow.pack(side="left")

month_label = tk.Label(month_frame, text="", font=("Arial", 14, "bold"))
month_label.pack(side="left", padx=10)

right_arrow = tk.Button(month_frame, text=">", command=lambda: change_month(1))
right_arrow.pack(side="left")

frame = tk.Frame(root)
frame.pack()

weekdays = ["Δε", "Τρ", "Τε", "Πε", "Πα", "Σα", "Κυ"]

update_calendar(selected_year, selected_month)

root.mainloop()
