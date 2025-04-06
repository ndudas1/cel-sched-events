from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}

@app.post("/items/")
def create_item(item: dict):
    return {"item": item}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    return {"item_id": item_id, "item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item with id {item_id} deleted"}

@app.patch("/items/{item_id}")
def partial_update_item(item_id: int, item: dict):
    return {"item_id": item_id, "updated_item": item}
