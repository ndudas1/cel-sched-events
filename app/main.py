from fastapi import FastAPI
from app.services.event_service import EventService

app = FastAPI()
service = EventService()

@app.get("/events/")
def get_events():
    return service.get_all_events()

@app.get("/events/{event_id}")
def get_event_by_id(event_id: int):
    return service.get_event_by_id(event_id)

@app.post("/events")
def create_item(item: dict):
    return service.create_event(item)

@app.put("/events/{event_id}")
def update_item(event_id: int, item: dict):
    return {"item_id": event_id, "item": item}


