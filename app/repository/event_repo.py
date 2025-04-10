from datetime import datetime, timedelta
from dateutil import parser
from typing import Tuple
from app.repository.models.event import Event
from app.repository import db_engine
from sqlalchemy import or_ as _or, and_ as _and, func

def calculate_occurence_on_day(event_start_end: Tuple[datetime, datetime], pending_Event_Start: datetime):
    start, end = event_start_end
    duration = end - start
    offset = timedelta(days=(pending_Event_Start - start).days)
    return (start + offset, start + offset + duration)

class EventRepository:
    def __init__(self):
        self.db = db_engine

    def get_all_events(self):
        return self.db.query(Event).all()

    def get_event_by_id(self, event_id):
        return self.db.query(Event).filter(Event.id == event_id).first()
    
    def get_first_event_by_date_and_freq(self, date: Tuple[datetime, datetime], frequency: int):
        start, end = date
        # See if there is an exact match first
        exact_match = self.db.query(Event).filter(
            _or(
                _and(Event.start_time <= start, start <= Event.end_time),
                _and(Event.start_time <= end, end <= Event.end_time),
            )).first()
        if exact_match is not None:
            return exact_match
        
        # If no exact match, check for recurring events
        recurring = self.db.query(Event).filter(Event.frequency > 0).all()
        if len(recurring) > 0:
            for event in recurring:
                # Bitwise check for the frequency
                if event.frequency & frequency > 0:
                    _start, _end = calculate_occurence_on_day((event.start_time, event.end_time), start)
                    if _start <= start <= _end or _start <= end <= _end:
                        return event

    def create_event(self, event):
        new_event = Event(
            name=event['name'],
            email=event['email'],
            notes=event.get('notes'),
            created_at=datetime.now(),
            start_time=event['start_time'],
            end_time=event['end_time'],
            frequency=event.get('frequency')
        )
        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)
        return new_event

    def update_event(self, event_id, updated_event):
        event = self.get_event_by_id(event_id)
        if event:
            for key, value in updated_event.items():
                setattr(event, key, value)
            self.db.commit()
            self.db.refresh(event)
            return event
        return None