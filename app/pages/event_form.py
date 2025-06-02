import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from app.controllers import create_event
from app.models import Recurrence

class EventForm:
    def __init__(self, master, on_success=None):
        """
        master: tk.Toplevel ή tk.Frame όπου θα “πέσει” η φόρμα
        on_success: προαιρετικό callback μετά την επιτυχία (π.χ. ανανέωση UI)
        """
        self.master = master
        self.on_success = on_success

        self.master.title("Προσθήκη Γεγονότος")
        self.master.geometry("400x650")

        # Διαθέσιμα slots ώρας (κάθε ώρα της ημέρας)
        self.time_slots = [f"{h:02d}:00" for h in range(24)]
        self.start_var  = tk.StringVar(value=self.time_slots[0])
        self.end_var    = tk.StringVar(value=self.time_slots[1])
        self.repeat_var = tk.StringVar(value="Καμία")

        self.build_form()

    def build_form(self):
        # Πεδίο τίτλου
        tk.Label(self.master, text="Τίτλος:").pack(anchor="w", padx=10, pady=(10, 0))
        self.title_entry = tk.Entry(self.master, width=50)
        self.title_entry.pack(padx=10, pady=5)

        # Πεδίο περιγραφής
        tk.Label(self.master, text="Περιγραφή:").pack(anchor="w", padx=10, pady=(10, 0))
        self.desc_text = tk.Text(self.master, height=4, width=50)
        self.desc_text.pack(padx=10, pady=5)

        # Επιλογή ημερομηνίας
        tk.Label(self.master, text="Ημερομηνία:").pack(anchor="w", padx=10, pady=(10, 0))
        self.date_entry = DateEntry(self.master, width=30, date_pattern="yyyy-mm-dd")
        self.date_entry.pack(padx=10, pady=5)

        # Επιλογή ώρας έναρξης
        tk.Label(self.master, text="Ώρα Έναρξης:").pack(anchor="w", padx=10, pady=(10, 0))
        tk.OptionMenu(self.master, self.start_var, *self.time_slots).pack(padx=10, pady=5, fill="x")

        # Επιλογή ώρας λήξης
        tk.Label(self.master, text="Ώρα Λήξης:").pack(anchor="w", padx=10, pady=(10, 0))
        self.end_menu = tk.OptionMenu(self.master, self.end_var, *self.time_slots[1:])
        self.end_menu.pack(padx=10, pady=5, fill="x")

        # Ενημέρωση διαθέσιμων ωρών λήξης όταν αλλάζει η ώρα έναρξης
        self.start_var.trace_add("write", self.update_end_time_options)

        # Πεδίο τοποθεσίας
        tk.Label(self.master, text="Χώρος:").pack(anchor="w", padx=10, pady=(10, 0))
        self.location_entry = tk.Entry(self.master, width=50)
        self.location_entry.pack(padx=10, pady=5)

        # Επιλογή επανάληψης
        tk.Label(self.master, text="Επανάληψη:").pack(anchor="w", padx=10, pady=(10, 0))
        repeat_opts = ["Καμία", "Ημερήσια", "Εβδομαδιαία", "Μηνιαία", "Ετήσια"]
        tk.OptionMenu(self.master, self.repeat_var, *repeat_opts).pack(padx=10, pady=5, fill="x")
        self.repeat_var.trace_add("write", self.toggle_repeat_until)

        # Ημερομηνία λήξης επανάληψης (αν ισχύει)
        tk.Label(self.master, text="Μέχρι Πότε (αν επαναλαμβάνεται):").pack(anchor="w", padx=10, pady=(10, 0))
        self.repeat_until_entry = DateEntry(
            self.master,
            width=30,
            date_pattern="yyyy-mm-dd",
            state="disabled"
        )
        self.repeat_until_entry.pack(padx=10, pady=5)

        # Κουμπί αποθήκευσης
        tk.Button(self.master, text="Αποθήκευση", command=self.save_event).pack(pady=20)

    def update_end_time_options(self, *args):
        """
        Ενημέρωση διαθέσιμων ωρών λήξης με βάση την επιλεγμένη ώρα έναρξης.
        """
        selected = self.start_var.get()
        idx = self.time_slots.index(selected)
        allowed = self.time_slots[idx + 1:] or [selected]
        self.end_var.set(allowed[0])

        menu = self.end_menu["menu"]
        menu.delete(0, "end")
        for t in allowed:
            menu.add_command(label=t, command=lambda v=t: self.end_var.set(v))

    def toggle_repeat_until(self, *args):
        """
        Ενεργοποίηση/Απενεργοποίηση του πεδίου 'Μέχρι Πότε' βάσει επιλογής επανάληψης.
        """
        state = "normal" if self.repeat_var.get() != "Καμία" else "disabled"
        self.repeat_until_entry.config(state=state)

    def save_event(self):
        """
        Διαβάζει τα δεδομένα από τη φόρμα και τα αποθηκεύει στη βάση μέσω του controller.
        """
        title       = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", "end").strip()
        date_       = self.date_entry.get_date()  # datetime.date
        start_tm    = datetime.strptime(self.start_var.get(), "%H:%M").time()
        end_tm      = datetime.strptime(self.end_var.get(),   "%H:%M").time()
        location    = self.location_entry.get().strip()

        # Mapping επανάληψης στο Recurrence Enum
        rec_map = {
            "Καμία":      Recurrence.NONE,
            "Ημερήσια":   Recurrence.DAILY,
            "Εβδομαδιαία": Recurrence.WEEKLY,
            "Μηνιαία":    Recurrence.MONTHLY,
            "Ετήσια":     Recurrence.YEARLY
        }
        rec     = rec_map[self.repeat_var.get()]
        rec_end = None
        if rec != Recurrence.NONE:
            rec_end = self.repeat_until_entry.get_date()

        # Έλεγχος υποχρεωτικών πεδίων
        if not title:
            messagebox.showwarning("Σφάλμα", "Ο τίτλος είναι υποχρεωτικός.")
            return

        try:
            # Κλήση στον controller για δημιουργία event
            ev = create_event(
                title=title,
                description=description,
                date_=date_,
                start_time_=start_tm,
                end_time_=end_tm,
                location=location,
                recurrence=rec,
                recurrence_end=rec_end
            )
        except ValueError as e:
            messagebox.showerror("Σφάλμα", str(e))
            return

        messagebox.showinfo("Επιτυχία", f"Αποθηκεύτηκε: {ev.title}")
        # Κλείσιμο παραθύρου και callback αν υπάρχει
        if self.on_success:
            self.on_success(ev)
        self.master.destroy()
