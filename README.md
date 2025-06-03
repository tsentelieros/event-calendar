# EventCalendar

Ένα desktop application γραμμένο σε Python/​tkinter για καταγραφή, προγραμματισμό και προβολή γεγονότων σε ημερολόγιο.

---

## 📋 Περιεχόμενα

- [Χαρακτηριστικά](#-χαρακτηριστικά)  
- [Προαπαιτούμενα](#-προαπαιτούμενα)  
- [Εγκατάσταση](#-εγκατάσταση)  
- [Εκτέλεση](#-εκτέλεση)  
- [Δομή Project](#-δομή-project)  
- [Τεχνολογίες](#-τεχνολογίες)  
- [License](#license)  

---

## ✨ Χαρακτηριστικά

- **Login / Sign-up** με hashed passwords (Passlib pbkdf2_sha256).  
- **Προβολή μηνιαίου ημερολογίου** με επιλογή μήνα/έτους και highlight της σημερινής ημέρας.  
- **Scrollable χρονοδιάγραμμα** 24 ωρών για κάθε ημέρα.  
- **Δημιουργία**, **Διαγραφή** και **Επεξεργασία** γεγονότων (βάση SQLite μέσω SQLAlchemy ORM).  
- **Ομαλή πλοήγηση** μεταξύ σελίδων (login, signup, calendar) με frames.  
- **Custom ttk-theme** (“clam”) και ομοιόμορφο styling (buttons, labels, frames).

---

## 🚀 Προαπαιτούμενα

 - Python 3.9+
- Git  
- (Προτείνεται) Virtual environment  

---

## ⚙️ Εγκατάσταση

   Κλωνοποίηση του repo:  
   ```bash
   git clone https://github.com/tsentelieros/EventCalendar.git
   cd event-calendar
   ```

## ▶️ Εγκατάσταση βιβλιοθηκών
pip install -r requirements.txt   

## ▶️ Εκτέλεση
   python -m app.main


## 📂 Δομή Project

event-calendar/
├── app/
│   ├── __init__.py
│   ├── main.py            ← entry-point (Tk application)
│   ├── controllers.py     ← CRUD logic, user/event management
│   ├── models.py          ← SQLAlchemy ORM models (User, Event)
│   └── pages/             ← UI frames
│       ├── __init__.py
│       ├── login.py
│       ├── signup.py
│       ├── menu.py
│       └── calendar_page.py
├── requirements.txt       ← Python dependencies
├── .gitignore
└── LICENSE                ← MIT License


## 🛠 Τεχνολογίες

Python 3.9+

tkinter/ttk για GUI

SQLAlchemy ORM με SQLite

Passlib (pbkdf2_sha256) για hashing κωδικών

git για version control


## 📝 License

This project is licensed under the MIT License – see the LICENSE file for details.