# CEL Event Scheduler

Simple event scheduler, that uses FastAPI, Postgresql and SqlAlchemy to do basic operations.

Basic event structure is as follows
{
  "name": string,
  "notes": string,
  "start_date": datetime,
  "end_date": datetime,
  "frequency": int
}
If the frequency value is 0 the event is treated as a one time event. If the frequency value is 
greater than zero then it is treated as a recurring event. Recurring date operations are a bit mask
put and placed into a single integer.
Monday = 0x1
Tuesday = 0x2
Wedesday = 0x4
Thursday = 0x8
Friday = 0x10
Saturday 0x20
Sumday = 0x40

For POST and PUT api handling the service layer will check for conflicting dates using the frequency field.
If there are invalid fields or a conflict the api will return a 400 Bad Request with some details.

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

You can use Curl commands to interact with the API; common use cases follow.

#### Get all events

```
curl -H "Content-Type: application/json" http://localhost:8000/events/
```

### Get event by id

```
curl -H "Content-Type: application/json" http://localhost:8000/events/{event_id}
```

#### Create a new event

```
curl -X POST -H "Content-Type: application/json" -d '{"name": "my event", "email": "y@me.com", "start_time": "2025-10-01T22:00:00-07:00", "end_time": "2025-10-01T22:30:00-07:00", "frequency": 4}' http://localhost:8000/events
```

#### Patch an event

```
curl -X PUT -H "Content-Type: application/json" -d '{"name": "my event", "email": "y@me.com", "start_time": "2025-10-04T22:00:00-07:00"}' http://localhost:8000/events/{event_id}
```