from datetime import datetime
from typing import Tuple
from app.repository.models.event import Event
from app.repository import db_engine
from sqlalchemy import or_ as _or, and_ as _and

class EventRepository:
    def __init__(self):
        self.db = db_engine

    def get_all_events(self):
        return self.db.query(Event).all()

    def get_event_by_id(self, event_id):
        return self.db.query(Event).filter(Event.id == event_id).first()
    
    def get_events_by_date_and_freq(self, date: Tuple[datetime, datetime]):
        return self.db.query(Event).filter(
            _or(
                _and(Event.start_time >= date[0], Event.start_time <= date[0]),
                _and(Event.end_time >= date[1], Event.end_time <= date[1])
            )).all()

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