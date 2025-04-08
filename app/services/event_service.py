from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.repository.event_repo import EventRepository
from app.repository.models.event import Event, has_required_fields

class EventService:
    def __init__(self):
        self.event_repository = EventRepository()

    def get_all_events(self):
        return self.event_repository.get_all_events()

    def get_event_by_id(self, event_id):
        return self.event_repository.get_event_by_id(event_id)

    def create_event(self, event: dict):
        # Here you can add any business logic before creating an event
        # For example, validating the event data
        # or checking for duplicates
        if not has_required_fields(event):
            raise HTTPException(
              status_code=400,
              detail=f"Event with the same date and frequency already exists."
            )
        existing_events = self.event_repository.get_events_by_date_and_freq((event['start_time'], event['end_time']))
        if len(existing_events) > 0:
            raise HTTPException(
              status_code=400,
              detail=f"Event with the same date and frequency already exists."
            )
        new_event = self.event_repository.create_event(event)
        return JSONResponse(
            status_code=201,
            content={"message": "Event created successfully.", "event_id": new_event.id}
        )

    def update_event(self, event_id, updated_event):
        event = self.event_repository.get_event_by_id(event_id)
        if not event:
            raise HTTPException(
              status_code=404,
              detail=f"Event with id {event_id} not found."
            )
        if not updated_event['start_time'] and not updated_event['end_time']:
            raise HTTPException(
              status_code=400,
              detail="Start time and end time are required."
            )
        start = updated_event['start_time']
        end = None
        if not start:
            start = event.start_time
        if not end:
            end = event.end_time
        if start > end:
            raise HTTPException(
              status_code=400,
              detail="Start time must be before end time."
            )
        date = (start, end)
        existing_events = self.event_repository.get_events_by_date_and_freq(date)
        if len(existing_events) > 0:
            raise HTTPException(
              status_code=400,
              detail=f"Event with the same date and frequency already exists."
            )
        updated_event = self.event_repository.update_event(event_id, updated_event)
        return JSONResponse(
            status_code=200,
            content={"message": "Event updated successfully.", "event_id": updated_event.id}
        )