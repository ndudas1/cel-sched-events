from app.repository.models.event import Event
from app.repository import db_engine

class EventRepository:
    def __init__(self):
        self.db = db_engine

    def get_all_events(self):
        return self.db.query(Event).all()

    def get_event_by_id(self, event_id):
        return self.db.query(Event).filter(Event.id == event_id).first()

    def create_event(self, event):
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def update_event(self, event_id, updated_event):
        event = self.get_event_by_id(event_id)
        if event:
            for key, value in updated_event.items():
                setattr(event, key, value)
            self.db.commit()
            self.db.refresh(event)
            return event
        return None

    def delete_event(self, event_id):
        event = self.get_event_by_id(event_id)
        if event:
            self.db.delete(event)
            self.db.commit()
            return True
        return False


