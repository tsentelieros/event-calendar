import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

class EventForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Προσθήκη Γεγονότος")
        self.master.geometry("400x650")

        self.events = []
        self.time_slots = [f"{hour:02d}:00" for hour in range(24)]

        self.start_var = tk.StringVar()
        self.end_var = tk.StringVar()
        self.repeat_var = tk.StringVar(value="Καμία")

        self.build_form()

    def build_form(self):
        tk.Label(self.master, text="Τίτλος:").pack()
        self.title_entry = tk.Entry(self.master, width=50)
        self.title_entry.pack()

        tk.Label(self.master, text="Περιγραφή:").pack()
        self.desc_text = tk.Text(self.master, height=4, width=50)
        self.desc_text.pack()

        tk.Label(self.master, text="Ημερομηνία:").pack()
        self.date_entry = DateEntry(self.master, width=30, date_pattern="yyyy-mm-dd")
        self.date_entry.pack()

        tk.Label(self.master, text="Ώρα Έναρξης:").pack()
        self.start_var.set(self.time_slots[0])
        tk.OptionMenu(self.master, self.start_var, *self.time_slots).pack()

        tk.Label(self.master, text="Ώρα Λήξης:").pack()
        self.end_var.set(self.time_slots[1])
        self.end_menu = tk.OptionMenu(self.master, self.end_var, *self.time_slots[1:])
        self.end_menu.pack()

        self.start_var.trace_add("write", self.update_end_time_options)

        tk.Label(self.master, text="Χώρος:").pack()
        self.location_entry = tk.Entry(self.master, width=50)
        self.location_entry.pack()

        tk.Label(self.master, text="Επανάληψη:").pack()
        repeat_options = ["Καμία", "Ημερήσια", "Εβδομαδιαία", "Μηνιαία", "Ετήσια"]
        tk.OptionMenu(self.master, self.repeat_var, *repeat_options).pack()
        self.repeat_var.trace_add("write", self.toggle_repeat_until)

        tk.Label(self.master, text="Μέχρι Πότε (αν επαναλαμβάνεται):").pack()
        self.repeat_until_entry = DateEntry(self.master, width=30, date_pattern="yyyy-mm-dd", state="disabled")
        self.repeat_until_entry.pack()

        tk.Button(self.master, text="Αποθήκευση", command=self.save_event).pack(pady=10)

    def update_end_time_options(self, *args):
        selected_start = self.start_var.get()
        start_index = self.time_slots.index(selected_start)
        allowed_times = self.time_slots[start_index + 1:] or [selected_start]
        self.end_var.set(allowed_times[0])

        menu = self.end_menu["menu"]
        menu.delete(0, "end")
        for t in allowed_times:
            menu.add_command(label=t, command=lambda value=t: self.end_var.set(value))

    def toggle_repeat_until(self, *args):
        if self.repeat_var.get() == "Καμία":
            self.repeat_until_entry.config(state="disabled")
        else:
            self.repeat_until_entry.config(state="normal")

    def save_event(self):
        title = self.title_entry.get()
        description = self.desc_text.get("1.0", "end").strip()
        date_str = self.date_entry.get_date().strftime("%Y-%m-%d")
        start_time = self.start_var.get()
        end_time = self.end_var.get()
        location = self.location_entry.get()
        repeat = self.repeat_var.get()

        if not title or not date_str or not start_time or not end_time:
            messagebox.showwarning("Σφάλμα", "Τα πεδία τίτλος, ημερομηνία, ώρα έναρξης και λήξης είναι υποχρεωτικά.")
            return

        try:
            start_dt = datetime.strptime(f"{date_str} {start_time}", "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(f"{date_str} {end_time}", "%Y-%m-%d %H:%M")
            if end_dt <= start_dt:
                raise ValueError("Η λήξη πρέπει να είναι μετά την έναρξη.")
            duration = int((end_dt - start_dt).total_seconds() / 60)
        except ValueError as e:
            messagebox.showerror("Σφάλμα", str(e))
            return

        repeat_until = None
        if repeat != "Καμία":
            repeat_until = self.repeat_until_entry.get_date().strftime("%Y-%m-%d")

        event = {
            "title": title,
            "description": description,
            "start": start_dt.strftime("%Y-%m-%d %H:%M"),
            "end": end_dt.strftime("%Y-%m-%d %H:%M"),
            "duration_minutes": duration,
            "location": location,
            "repeat": repeat,
            "repeat_until": repeat_until
        }

        self.events.append(event)
        messagebox.showinfo("Επιτυχία", "Το γεγονός προστέθηκε!")
        self.master.destroy()
