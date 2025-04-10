from dateutil import parser
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.repository.event_repo import EventRepository
from app.repository.models.event import has_required_fields

def check_all(event: dict):
    check_not_null(event)
    check_event_fields(event)
    check_event_time(event)

def check_not_null(event: dict):
    if not event:
        raise HTTPException(
          status_code=400,
          detail="Invalid event ID or event data."
        )
def check_event_fields(event: dict): 
    if not has_required_fields(event):
        raise HTTPException(
          status_code=400,
          detail=f"Event is missing some required fields."
        )
def check_event_time(event: dict):
    if event['start_time'] > event['end_time']:
        raise HTTPException(
          status_code=400,
          detail="Start time must be before end time."
        )
def complete_frequency(event: dict):
    if 'frequency' not in event:
        event['frequency'] = 0
        return
    if event.get('frequency', 0) > 0:
        start_day = parser.parse(event['start_time']).weekday()
        end_day = parser.parse(event['end_time']).weekday()
        event['frequency'] = event.get('frequency', 0) | ( 1 << start_day) | (1 << end_day)

# Monday = 1
# Tuesday = 2
# Wednesday = 4
# Thursday = 8
# Friday = 16
# Saturday = 32
# Sunday = 64

class EventService:
    def __init__(self):
        self.event_repository = EventRepository()

    def get_all_events(self):
        return self.event_repository.get_all_events()

    def get_event_by_id(self, event_id):
        return self.event_repository.get_event_by_id(event_id)

    def create_event(self, event: dict):
        check_all(event)
        complete_frequency(event)
        start = parser.parse(event['start_time'])
        end = parser.parse(event['end_time'])
        date = (start, end)
        interfering_event = self.event_repository.get_first_event_by_date_and_freq(date, event.get('frequency'))
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
        check_not_null(updated_event)
        existing_event = self.event_repository.get_event_by_id(event_id)
        start = parser.parse(updated_event.get('start_time')) if updated_event.get('start_time') else existing_event.start_time
        end = parser.parse(updated_event.get('end_time')) if updated_event.get('end_time') else existing_event.end_time
        updated_event['start_time'] = start
        updated_event['end_time'] = end
        check_event_time(updated_event)
        date = (start, end)
        interfering_event = self.event_repository.get_first_event_by_date_and_freq(date, existing_event.frequency)
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