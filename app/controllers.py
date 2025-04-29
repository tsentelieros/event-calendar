from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import User, Base

# Setup υποδομής βάσης
engine = create_engine('sqlite:///events.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Δημιουργία πινάκων αν δεν υπάρχουν
Base.metadata.create_all(engine)


def check_user(username: str, password: str) -> bool:
    """
    Ελέγχει αν τα credentials αντιστοιχούν σε εγγεγραμμένο χρήστη.
    Επιστρέφει True σε επιτυχή ταυτοποίηση, αλλιώς False.
    """
    user = session.query(User).filter_by(user_name=username).first()
    if user is None:
        return False
    return user.check_password(password)


def create_user(username: str, password: str) -> bool:
    """
    Δημιουργεί νέο χρήστη με το δοσμένο username και password.
    Επιστρέφει True εάν έγινε επιτυχής δημιουργία, False αν υπάρχει ήδη.
    """
    if session.query(User).filter_by(user_name=username).first():
        return False
    new_user = User(user_name=username)
    new_user.set_password(password)
    session.add(new_user)
    session.commit()
    return True

# Μπορείς να προσθέσεις επιπλέον λειτουργίες CRUD για events εδώ
