# CEL Event Scheduler

Simple event scheduler, that uses FastAPI, Postgresql and SqlAlchemy to do basic operations.

## Running the project

You can choose to debug the project or run from Docker (the recommended approach)

### Using Docker (recommended)

Docker compose will download all the required images and start them installing all dependencies.
They can be viewed in the __docker-compose.yaml__ file.

```
docker-compose up
```

### Debug

Create a virtual environment

```
python -m venv .venv
```

Activate the environment

```
source .venv/bin/activate
```

Install the required dependencies, run:

```
pip install -r requirements.txt
```

### Making API Requests

You may Curl

#### Get all events

```
curl -H "Content-Type: application/json" http://localhost:8000/events/
```

#### Create a new event

```
curl -X POST -H "Content-Type: application/json" -d '{"name": "my event", "email": "y@me.com", "start_time": "2025-10-01T22:00:00-07:00", "end_time": "2025-10-01T22:30:00-07:00"}' http://localhost:8000/events
```

#### Patch an event

```
curl -X PUT -H "Content-Type: application/json" -d '{"name": "my event", "email": "y@me.com", "start_time": "2025-10-04T22:00:00-07:00"}' http://localhost:8000/events/{event_id}
```