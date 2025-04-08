# Project Title

A brief description of what this project does and its purpose.

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

Provide examples of how to use the project. For instance:

```bash
python src/main.py
```

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Making Requests

You may Curl

# Get all events

```curl -H "Content-Type: application/json" http://localhost:8000/events/```

# Create a new event

```
curl -X POST -H "Content-Type: application/json" -d '{"name": "my event", "email": "y@me.com", "start_time": "2025-10-01T22:00:00-07:00", "end_time": "2025-10-01T22:30:00-07:00"}' http://localhost:8000/events
```

# Patch an event

```
curl -X PUT -H "Content-Type: application/json" -d '{"name": "my event", "email": "y@me.com", "start_time": "2025-10-04T22:00:00-07:00"}' http://localhost:8000/events
```