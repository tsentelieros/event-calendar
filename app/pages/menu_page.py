import tkinter as tk
import calendar
import datetime
from tkinter import messagebox

root = tk.Tk()
root.title("Ημερολόγιο Μήνα + Χρονοδιάγραμμα")
root.geometry("400x500")  # πιο λογικό μέγεθος

selected_year = datetime.date.today().year
selected_month = datetime.date.today().month

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

    # Ημέρες
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
            if day != 0:
                day_label.bind("<Enter>", lambda e, lbl=day_label: lbl.config(cursor="hand2"))
                day_label.bind("<Leave>", lambda e, lbl=day_label: lbl.config(cursor="arrow"))
                day_label.bind("<Button-1>", lambda e, d=day: open_schedule_for_day(d))


def change_month(increment):
    global selected_year, selected_month
    new_month = selected_month + increment
    if new_month < 1:
        new_month = 12
        selected_year -= 1
    elif new_month > 12:
        new_month = 1
        selected_year += 1

    update_calendar(selected_year, new_month)

def open_year_input():
    def set_year(event=None):
        try:
            y = int(year_entry.get())
            if 1930 <= y <= 2125:
                update_calendar(y, selected_month)
                popup.destroy()
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
    year_entry.bind("<Return>", set_year)

    tk.Button(popup, text="OK", command=set_year).pack(pady=5)

def go_to_today():
    today = datetime.date.today()
    update_calendar(today.year, today.month)

# Menu
menu_bar = tk.Menu(root)
menu_bar.add_command(label="Σήμερα", command=go_to_today)
menu_bar.add_command(label="Επιλέξτε έτος", command=open_year_input)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Όλα τα events")
file_menu.add_command(label="Νέο event")
file_menu.add_command(label="Διαγραφή event")
menu_bar.add_cascade(label="Events", menu=file_menu)

root.config(menu=menu_bar)

# Πάνω μέρος - Ημερολόγιο
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
# Frame για το χρονοδιάγραμμα
schedule_frame = tk.Frame(root)
schedule_frame.pack(pady=10, fill="both", expand=True)


weekdays = ["Δε", "Τρ", "Τε", "Πε", "Πα", "Σα", "Κυ"]

update_calendar(selected_year, selected_month)


# Τρέχουσα Ώρα κάτω δεξιά
def update_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    time_label.config(text=now)
    root.after(1000, update_time)  # ανανέωση κάθε 1000ms = 1 δευτερόλεπτο

bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom", fill="x", pady=5, padx=5)

time_label = tk.Label(bottom_frame, font=("Arial", 10))
time_label.pack(side="right")

update_time()

def open_schedule_for_day(day):
    # Καθαρίζουμε το παλιό χρονοδιάγραμμα
    for widget in schedule_frame.winfo_children():
        widget.destroy()

    # Τίτλος
    tk.Label(schedule_frame, text=f"Χρονοδιάγραμμα {day}/{selected_month}/{selected_year}", font=("Arial", 12, "bold")).pack(pady=5)

    # Container με Canvas για Scroll
    container = tk.Frame(schedule_frame)
    container.pack(pady=5, fill="both", expand=True)

    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Ώρες
    for hour in range(24):
        hour_str = f"{hour:02d}:00"
        row = tk.Frame(scrollable_frame)
        row.pack(fill="x", padx=5, pady=2)

        hour_label = tk.Label(row, text=hour_str, width=8, anchor="w")
        hour_label.pack(side="left")

        event_label = tk.Label(row, text="(Καμία καταχώρηση)", fg="gray")
        event_label.pack(side="left", padx=10)


root.mainloop()
