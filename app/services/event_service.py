from app.repository.event_repo import EventRepository

class EventService:
    def __init__(self):
        self.event_repository = EventRepository()

    def get_all_events(self):
        return self.event_repository.get_all_events()

    def get_event_by_id(self, event_id):
        return self.event_repository.get_event_by_id(event_id)

    def create_event(self, event):
        return self.event_repository.create_event(event)

    def update_event(self, event_id, updated_event):
        return self.event_repository.update_event(event_id, updated_event)

    def delete_event(self, event_id):
        return self.event_repository.delete_event(event_id)