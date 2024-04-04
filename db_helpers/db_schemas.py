from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, relationship, DeclarativeBase
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = 'calendar_events'
    event_id = Column(Integer(), primary_key=True, autoincrement=True)
    host_id = Column(Integer(), ForeignKey('event_hosts.host_id'))
    host_event_id = Column(String(100))
    event_name = Column(String(100))
    event_description = Column(String(300))
    event_price = Column(Integer())
    event_start_date = Column(DateTime())
    event_end_date = Column(DateTime())
    event_location = Column(String(100))


class EventHosts(Base):
    __tablename__ = 'event_hosts'
    host_id = Column(Integer(), primary_key=True,  autoincrement=True)
    host_calendar_id = Column(String(100))
    host_name = Column(String(100))
    host_description = Column(String(300))
    host_website = Column(String(100))
    host_email = Column(String(100))
    events = relationship('Event', backref='host')
