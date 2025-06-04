import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import controllers
from app.models import Base, Event, Recurrence
from datetime import date, time

@pytest.fixture
def db_session(monkeypatch):
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()
    monkeypatch.setattr(controllers, 'session', session)
    yield session
    session.close()


def test_create_event_overlap(db_session):
    """Creating an overlapping event should raise ValueError."""
    controllers.create_event(
        title='A',
        description='first',
        date_=date(2024, 1, 1),
        start_time_=time(9, 0),
        end_time_=time(10, 0),
    )
    with pytest.raises(ValueError):
        controllers.create_event(
            title='B',
            description='overlap',
            date_=date(2024, 1, 1),
            start_time_=time(9, 30),
            end_time_=time(10, 30),
        )

    events = db_session.query(Event).all()
    assert len(events) == 1
    assert events[0].title == 'A'


def test_create_event_with_recurrence(db_session):
    """Events should store recurrence information correctly."""
    ev = controllers.create_event(
        title='R',
        description='recurring',
        date_=date(2024, 1, 2),
        start_time_=time(10, 0),
        end_time_=time(11, 0),
        recurrence=Recurrence.DAILY,
        recurrence_end=date(2024, 1, 5),
    )
    stored = db_session.query(Event).get(ev.id)
    assert stored.recurrence == Recurrence.DAILY
    assert stored.recurrence_end == date(2024, 1, 5)
    assert stored.title == 'R'
    assert stored.date == date(2024, 1, 2)
