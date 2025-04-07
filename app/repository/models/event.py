from sqlalchemy import Column, Integer, String, TIMESTAMP as Timestamp
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    notes = Column(String)
    created_at = Column(Timestamp)
    start_time = Column(Timestamp)
    end_time = Column(Timestamp)
    frequency = Column(Integer, nullable=True)