from datetime import datetime, date, time
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Event, Recurrence
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

# ——————————————
# Event management
# ——————————————
def create_event(
    title: str,
    description: str,
    date_: date,
    start_time_: time,
    end_time_: time,
    location: str = "",
    recurrence: Recurrence = Recurrence.NONE,
    recurrence_end: date = None
) -> Event:
    """
    Δημιουργεί ένα νέο event μετά από έλεγχο επικαλύψεων.
    Επιστρέφει το αντικείμενο Event ή ρίχνει ValueError.
    """
    # Basic time validation
    if start_time_ >= end_time_:
        raise ValueError("Η ώρα έναρξης πρέπει να είναι πριν την ώρα λήξης.")

    # Overlap check: same date, any overlapping interval
    overlapping = session.query(Event).filter(
        Event.date == date_,
        or_(
            and_(Event.start_time <= start_time_, Event.end_time > start_time_),
            and_(Event.start_time < end_time_,    Event.end_time >= end_time_),
            and_(Event.start_time >= start_time_, Event.end_time <= end_time_)
        )
    ).first()

    if overlapping:
        raise ValueError(
            f"Υπάρχει ήδη γεγονός «{overlapping.title}» "
            f"που επικαλύπτεται χρονικά."
        )

    now = datetime.now()
    ev = Event(
        title=title,
        description=description,
        date=date_,
        start_time=start_time_,
        end_time=end_time_,
        location=location,
        recurrence=recurrence,
        recurrence_end=recurrence_end,
        created_at=now,
        updated_at=now
    )
    session.add(ev)
    session.commit()
    return ev


def get_events_on(date_: date):
    """
    Επιστρέφει λίστα με όλα τα events για συγκεκριμένη ημερομηνία,
    ταξινομημένα κατά ώρα έναρξης.
    """
    return session.query(Event)\
        .filter_by(date=date_)\
        .order_by(Event.start_time)\
        .all()


def update_event(event_id: int, **kwargs) -> Event:
    """
    Ενημερώνει ένα event. Δέχεται πεδία όπως title, date, start_time, end_time, κλπ.
    Επιστρέφει το ενημερωμένο αντικείμενο ή ρίχνει ValueError αν δεν υπάρχει.
    """
    ev = session.query(Event).get(event_id)
    if not ev:
        raise ValueError("Το γεγονός δεν βρέθηκε.")

    # If times are changing, validate interval
    if 'start_time' in kwargs or 'end_time' in kwargs:
        new_start = kwargs.get('start_time', ev.start_time)
        new_end   = kwargs.get('end_time',   ev.end_time)
        if new_start >= new_end:
            raise ValueError("Η ώρα έναρξης πρέπει να είναι πριν τη λήξη.")

    # Apply updates
    for field, val in kwargs.items():
        if hasattr(ev, field):
            setattr(ev, field, val)

    ev.updated_at = datetime.now()
    session.commit()
    return ev


def delete_event(event_id: int) -> bool:
    """
    Διαγράφει το event με το δοσμένο ID.
    Επιστρέφει True αν διαγράφηκε, False αν δεν βρέθηκε.
    """
    ev = session.query(Event).get(event_id)
    if not ev:
        return False
    session.delete(ev)
    session.commit()
    return True
