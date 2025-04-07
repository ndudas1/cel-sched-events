from fastapi import FastAPI
from app.services.event_service import EventService

app = FastAPI()
service = EventService()

@app.get("/events/")
def get_events():
    return service.get_all_events()

@app.post("/events")
def create_item(item: dict):
    return {"item": item}

@app.put("/events/{event_id}")
def update_item(event_id: int, item: dict):
    return {"item_id": event_id, "item": item}

@app.delete("/events/{event_id}")
def delete_item(event_id: int):
    return {"message": f"Item with id {event_id} deleted"}

