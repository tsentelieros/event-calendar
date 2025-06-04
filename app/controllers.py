# app/controllers.py

from datetime import datetime, date, time
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Event, Recurrence

# ————————————
# Setup βάσης δεδομένων
# ————————————
engine = create_engine('sqlite:///events.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


def check_user(username: str, password: str) -> bool:
    user = session.query(User).filter_by(user_name=username).first()
    if user is None:
        return False
    return user.check_password(password)


def get_user_by_username(username: str):
    return session.query(User).filter_by(user_name=username).first()


def create_user(username: str, password: str) -> bool:
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
    recurrence_end: date = None,
    owner: User = None,
    existing_event: Event = None
) -> Event:
    """
    Δημιουργεί ή ενημερώνει ένα event:
    • Αν υπάρχει existing_event, κάνουμε UPDATE σε αυτό.
    • Αλλιώς, κάνουμε INSERT με τον owner (υποχρεωτικό).
    Ελέγχουμε overlap μόνο αν δημιουργούμε _νέο_ event.
    """

    # 1) Εάν είμαστε σε "edit mode" (υπάρχει existing_event):
    if existing_event:
        # Έλεγχος εγκυρου διαστήματος, αν αλλάζει ώρα
        if start_time_ >= end_time_:
            raise ValueError("Η ώρα έναρξης πρέπει να είναι πριν την ώρα λήξης.")

        # Αν αλλάζει ημερομηνία ή ώρες, ενδεχομένως να χρειάζεται έλεγχος overlap:
        #   (για απλότητα εδώ δεν ξανα-ελέγχουμε overlap, υποθέτουμε ότι είναι αποδεκτό να
        #    μετακινηθεί σε μη επικαλυπτόμενο slot—μπορείτε να προσθέσετε παραπάνω έλεγχο
        #    εάν επιθυμείτε)
        existing_event.title = title
        existing_event.description = description
        existing_event.date = date_
        existing_event.start_time = start_time_
        existing_event.end_time = end_time_
        existing_event.location = location
        existing_event.recurrence = recurrence
        existing_event.recurrence_end = recurrence_end
        existing_event.updated_at = datetime.utcnow()
        session.commit()
        return existing_event

    # 2) Διαφορετικά, είμαστε σε "create new" mode:
    if not owner:
        raise ValueError("Πρέπει να είσαι συνδεδεμένος για να δημιουργήσεις event.")

    # α) Έλεγχος έγκυρου διαστήματος
    if start_time_ >= end_time_:
        raise ValueError("Η ώρα έναρξης πρέπει να είναι πριν την ώρα λήξης.")

    # β) Έλεγχος overlap για νέα events (ίδια ημερομηνία + επικαλυπτόμενες ώρες)
    overlapping = session.query(Event).filter(
        Event.date == date_,
        or_(
            and_(Event.start_time <= start_time_, Event.end_time > start_time_),
            and_(Event.start_time < end_time_,    Event.end_time >= end_time_),
            and_(Event.start_time >= start_time_, Event.end_time <= end_time_)
        ),
        Event.user_id == owner.id   # Φροντίζουμε να ελέγξουμε μόνο τα δικά του events
    ).first()

    if overlapping:
        raise ValueError(
            f"Υπάρχει ήδη γεγονός «{overlapping.title}» "
            f"που επικαλύπτεται χρονικά."
        )

    # γ) Δημιουργούμε καινούριο event
    now = datetime.utcnow()
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
        updated_at=now,
        owner=owner
    )
    session.add(ev)
    session.commit()
    return ev


def get_events_on(owner: User, date_: date):
    """
    Επιστρέφει λίστα με όλα τα events του συγκεκριμένου owner που “τρέχουν” τη date_.
    • Είτε επειδή date == date_
    • Είτε επειδή date < date_ <= recurrence_end και ταιριάζει pattern επανάληψης
    """
    # 1) Όσα έχουν date == date_ και ανήκουν στον owner:
    q1 = session.query(Event).filter(
        Event.date == date_,
        Event.user_id == owner.id
    ).all()

    # 2) Επαναληπτικά events που ανήκουν στον owner
    events_recurring = session.query(Event).filter(
        Event.user_id == owner.id,
        Event.recurrence != Recurrence.NONE,
        Event.date < date_,
        Event.recurrence_end != None,
        Event.recurrence_end >= date_
    ).all()

    matching = []
    for ev in events_recurring:
        start = ev.date
        end_repeat = ev.recurrence_end
        diff_days = (date_ - start).days

        if ev.recurrence == Recurrence.DAILY:
            if 0 <= diff_days <= (end_repeat - start).days:
                matching.append(ev)

        elif ev.recurrence == Recurrence.WEEKLY:
            if 0 <= diff_days <= (end_repeat - start).days and diff_days % 7 == 0:
                matching.append(ev)

        elif ev.recurrence == Recurrence.MONTHLY:
            if 0 <= diff_days <= (end_repeat - start).days and date_.day == start.day:
                matching.append(ev)

        elif ev.recurrence == Recurrence.YEARLY:
            if (
                0 <= diff_days <= (end_repeat - start).days
                and date_.month == start.month
                and date_.day == start.day
            ):
                matching.append(ev)

    # Ενώσουμε τα “στατικά” (q1) με τα επαναληπτικά (matching) και τα ταξινομούμε
    results = q1 + matching
    results.sort(key=lambda e: e.start_time)
    return results


def update_event(event_id: int, **kwargs) -> Event:
    ev = session.query(Event).get(event_id)
    if not ev:
        raise ValueError("Το γεγονός δεν βρέθηκε.")
    # (όμοιο validation με create_event, αν χρειάζεται)
    for field, val in kwargs.items():
        if hasattr(ev, field):
            setattr(ev, field, val)
    ev.updated_at = datetime.utcnow()
    session.commit()
    return ev


def delete_event(event_id: int) -> bool:
    ev = session.query(Event).get(event_id)
    if not ev:
        return False
    session.delete(ev)
    session.commit()
    return True
