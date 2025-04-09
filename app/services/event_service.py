from dateutil import parser
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.repository.event_repo import EventRepository
from app.repository.models.event import has_required_fields

def _do_event_validation(event: dict, ignore_required_fields: bool = False):
    if not event:
        raise HTTPException(
          status_code=400,
          detail="Invalid event ID or event data."
        )
    if not ignore_required_fields and not has_required_fields(event):
        raise HTTPException(
          status_code=400,
          detail=f"Event is missing some required fields."
        )
    if not ignore_required_fields and not event['start_time'] < event['end_time']:
        raise HTTPException(
          status_code=400,
          detail="Start time must be before end time."
        )

class EventService:
    def __init__(self):
        self.event_repository = EventRepository()

    def get_all_events(self):
        return self.event_repository.get_all_events()

    def get_event_by_id(self, event_id):
        return self.event_repository.get_event_by_id(event_id)

    def create_event(self, event: dict):
        _do_event_validation(event)
        date = (event['start_time'], event['end_time'])
        interfering_event = self.event_repository.get_event_by_date_and_freq(date, event.get('frequency', 0))
        if interfering_event:
            raise HTTPException(
              status_code=400,
              detail=f"There is an Event whose schedule interfers."
            )
        new_event = self.event_repository.create_event(event)
        return JSONResponse(
            status_code=201,
            content={"message": "Event created successfully.", "event_id": new_event.id}
        )

    def update_event(self, event_id, updated_event: dict):
        _do_event_validation(updated_event, ignore_required_fields=True)
        existing_event = self.event_repository.get_event_by_id(event_id)
        start = parser.parse(updated_event.get('start_time')) if updated_event.get('start_time') else existing_event.start_time
        end = parser.parse(updated_event.get('end_time')) if updated_event.get('end_time') else existing_event.end_time
        if start > end:
            raise HTTPException(
              status_code=400,
              detail="Start time must be before end time."
            )
        date = (start, end)
        interfering_event = self.event_repository.get_event_by_date_and_freq(date, existing_event.frequency)
        if interfering_event and interfering_event.id != event_id:
            raise HTTPException(
              status_code=400,
              detail=f"There is an Event whose schedule interfers."
            )
        event = self.event_repository.update_event(event_id, updated_event)
        return JSONResponse(
            status_code=200,
            content={"message": "Event updated successfully.", "event_id": event.id}
        )