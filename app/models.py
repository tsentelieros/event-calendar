from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    Date,
    Time,
    DateTime,
    Enum as SAEnum,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.hash import pbkdf2_sha256
import enum
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    def set_password(self, password):
        """Ορίζει το password κάνοντας hash με το pbkdf2_sha256."""
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        """Επαληθεύει το password συγκρίνοντας το δοσμένο με το αποθηκευμένο hash."""
        return pbkdf2_sha256.verify(password, self.password_hash)

    def __repr__(self):
        return f"<User(user_name={self.user_name})>"



class Recurrence(enum.Enum):
    NONE    = "None"
    DAILY   = "Daily"
    WEEKLY  = "Weekly"
    MONTHLY = "Monthly"
    YEARLY  = "Yearly"
    
class Event(Base):
    __tablename__ = 'events'
    
    id             = Column(Integer, primary_key=True)
    title          = Column(String(200), nullable=False)
    description    = Column(Text, nullable=True)
    date           = Column(Date, nullable=False)
    start_time     = Column(Time, nullable=False)
    end_time       = Column(Time, nullable=False)
    location       = Column(String(200), nullable=True)

    recurrence     = Column(SAEnum(Recurrence), default=Recurrence.NONE, nullable=False)
    recurrence_end = Column(Date, nullable=True)  # μέχρι πότε επαναλαμβάνεται

    created_at     = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at     = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return (
            f"<Event(title={self.title!r}, date={self.date}, "
            f"start={self.start_time}, end={self.end_time})>"
        )
        


# Δημιουργία engine για SQLite (αρχείο events.db στον φάκελο του project)
engine = create_engine('sqlite:///events.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)
